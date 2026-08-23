from django.contrib import admin

from .admin_mixins import ThumbnailAdminMixin
from .models import FormSubmission, HeroSlide, SiteSettings


@admin.register(HeroSlide)
class HeroSlideAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'image'
    list_display = ('thumbnail', 'title', 'eyebrow', 'order', 'active')
    list_editable = ('order', 'active')
    list_filter = ('active',)
    search_fields = ('title', 'eyebrow', 'subtitle')
    readonly_fields = ('thumbnail',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact details', {'fields': ('email', 'phone', 'address', 'rcs')}),
        ('Bank details', {'fields': ('iban',)}),
        ('Social links', {'fields': ('facebook_url', 'instagram_url')}),
        ('Footer', {'fields': ('footer_text',)}),
    )

    def has_add_permission(self, request):
        # Singleton: staff can edit the one settings row but never create a second.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'subject')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    actions = ['mark_read', 'mark_archived']

    def mark_read(self, request, queryset):
        queryset.update(status='read')

    mark_read.short_description = 'Mark selected as read'

    def mark_archived(self, request, queryset):
        queryset.update(status='archived')

    mark_archived.short_description = 'Mark selected as archived'
