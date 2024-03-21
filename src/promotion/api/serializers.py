from rest_framework import serializers

from promotion.models import PromotionAddress, PromotionCategory, Promotion, Contact, PromotionImage
from review.models import Review
from promotion.utils.SearchLonLat import search_lon_lat
from user.models import MyUser


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'
        ref_name = 'contact'


class PromotionCategorySerializer(serializers.ModelSerializer):
    promotions_count = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = PromotionCategory
        fields = ['id', 'title', 'image', 'parent_category', 'subcategories', 'promotions_count', 'icon']

    def get_promotions_count(self, obj):
        return Promotion.objects.filter(category=obj).count()

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        serializer = self.__class__(subcategories, many=True)
        return serializer.data


class PromotionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionImage
        fields = ['title', 'image']


class AddressSerializer(serializers.ModelSerializer):
    street = serializers.SerializerMethodField('get_street')

    class Meta:
        model = PromotionAddress
        fields = (
            'id', 'street'
        )

    def get_street(self, obj):
        street_value = obj.street
        if street_value is not None:
            result = search_lon_lat({'street': street_value})
            if result and 'street' in result:
                return result['street']
        return None


class PromotionSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True)
    reviews_count = serializers.SerializerMethodField()
    images = PromotionImageSerializer(many=True)
    address = AddressSerializer(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ['id', 'category', 'company', 'title', 'image',
                  'old_price', 'new_price', 'discount',
                  'description', 'type', 'contacts',
                  'work_time', 'address', 'likes', 'images',
                  'likes_count', 'end_date', 'is_daily', 'reviews_count']
        
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_reviews_count(self, obj):
        return Review.objects.filter(promotion=obj).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category_name'] = instance.category.title
        return representation
    
    def create(self, validated_data):
        contact_data = validated_data.pop('contacts', [])
        like_data = validated_data.pop('likes', [])
        address_data = validated_data.pop('address', [])

        promotion = Promotion.objects.create(**validated_data)

        for data in contact_data:
            contacts = Contact.objects.filter(**data)
            if contacts.exists():
                contact = contacts.first()
            else:
                contact = Contact.objects.create(**data)
            promotion.contacts.add(contact)

        for like in like_data:
            user, created = MyUser.objects.get_or_create(**like)
            promotion.likes.add(user)

        for address in address_data:
            address_instance = PromotionAddress.objects.create(**address)
            street_value = AddressSerializer().get_street(obj=address_instance)

            if street_value and street_value.get('street'):
                address_instance.street = street_value
                address_instance.save()
                promotion.address.add(address_instance)
                print("адрес: ", address_instance)
        return promotion
            
