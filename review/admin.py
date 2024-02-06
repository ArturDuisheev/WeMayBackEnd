from django.contrib import admin
from .models import Review

admin.site.register(Review)
admin.site.register(Review.likes.through)
