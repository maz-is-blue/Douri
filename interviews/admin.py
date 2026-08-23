from django.contrib import admin

from core.admin_mixins import ThumbnailAdminMixin

from .models import Interview


@admin.register(Interview)
class InterviewAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'hero_image'
    list_display = ('thumbnail', 'subject_name', 'quote', 'publish_date')
    list_filter = ('publish_date',)
    search_fields = ('subject_name', 'quote', 'body')
    date_hierarchy = 'publish_date'
    prepopulated_fields = {'slug': ('subject_name',)}
    readonly_fields = ('thumbnail',)
    fieldsets = (
        (None, {'fields': ('subject_name', 'quote', 'slug', 'title')}),
        ('Credits', {'fields': ('prepared_by', 'edited_by', 'publish_date')}),
        ('Content', {'fields': ('hero_image', 'thumbnail', 'body')}),
    )
