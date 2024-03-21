from django.contrib import admin
from .models import Contact, PromotionCategory, Promotion
# Register your models here.


admin.site.register(PromotionCategory)
admin.site.register(Promotion)
admin.site.register(Contact)
admin.site.register(Promotion.likes.through)
