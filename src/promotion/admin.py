from django.contrib import admin
from .models import PromotionCategory, Promotion, PromotionImage


admin.site.register(PromotionCategory)
admin.site.register(Promotion)
admin.site.register(Promotion.likes.through)
admin.site.register(PromotionImage)