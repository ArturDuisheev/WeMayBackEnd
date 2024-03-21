from django.contrib import admin
from .models import Contact, PromotionCategory, Promotion, PromotionAddress, PromotionImage, WorkTime


admin.site.register(PromotionCategory)
admin.site.register(Promotion)
admin.site.register(PromotionAddress)
admin.site.register(Contact)
admin.site.register(Promotion.likes.through)
admin.site.register(PromotionImage)
admin.site.register(WorkTime)
