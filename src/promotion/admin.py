from django.contrib import admin
from .models import PromotionCategory, Promotion, PromotionImage, PromotionContact

admin.site.register(PromotionCategory)
admin.site.register(Promotion.likes.through)
admin.site.register(PromotionContact)


class PromotionImageInline(admin.TabularInline):
    model = PromotionImage
    extra = 1


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    inlines = [PromotionImageInline]
    list_display = ('title', 'company', 'category', 'type', 'new_price', 'old_price', 'end_date')
    search_fields = ['title', 'company__name']
