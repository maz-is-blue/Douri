from django.contrib import admin

from core.admin_mixins import ThumbnailAdminMixin

from .models import InstagramPost


@admin.register(InstagramPost)
class InstagramPostAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'image'
    list_display = ('thumbnail', 'caption', 'project', 'featured_on_home', 'order')
    list_editable = ('order', 'featured_on_home')
    list_filter = ('featured_on_home', 'project')
    search_fields = ('caption', 'post_url')
    readonly_fields = ('thumbnail',)
