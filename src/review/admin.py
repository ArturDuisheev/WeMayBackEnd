from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'promotion', 'created_time')
    search_fields = ['author__username', 'promotion__title']
    list_filter = ['created_time']


admin.site.register(Review.likes.through)
