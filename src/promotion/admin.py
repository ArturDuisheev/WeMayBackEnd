from django.contrib import admin
from .models import PromotionCategory, Promotion, PromotionImage, PromotionContact

admin.site.register(Promotion.likes.through)


@admin.register(PromotionCategory)
class PromotionCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'icon', 'parent_category')
    search_fields = ['title']
    list_filter = ['parent_category']


@admin.register(PromotionContact)
class PromotionContactAdmin(admin.ModelAdmin):
    list_display = ('phone', 'promotion')
    search_fields = ['phone']
    list_filter = ['promotion']


class PromotionImageInline(admin.TabularInline):
    model = PromotionImage
    extra = 1


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    inlines = [PromotionImageInline]
    list_display = ('title', 'company', 'category', 'type', 'new_price', 'old_price', 'end_date')
    search_fields = ['title', 'company__name']
