from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Location, Post


class AdminPost(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'pub_date',
        'author',
        'category',
        'location',
    )
    empty_value_display = 'Не задано'
    save_on_top = True
    list_editable = (
        'is_published',
    )
    list_filter = [
        'is_published',
        'pub_date',
    ]
    search_fields = [
        'title',
        'author__username',
        'location__name',
        'category__title',
    ]
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}"'
                         'style="max-height: 200px;">')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'slug'
    )
    list_editable = (
        'is_published',
    )
    list_filter = [
        'title',
        'is_published',
    ]


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    list_filter = [
        'is_published',
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, AdminPost)
