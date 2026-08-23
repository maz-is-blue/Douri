from django.contrib import admin

from core.admin_mixins import ThumbnailAdminMixin

from .models import Partner, TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'photo'
    list_display = ('thumbnail', 'name', 'role', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'role', 'short_bio')
    readonly_fields = ('thumbnail',)


@admin.register(Partner)
class PartnerAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'logo'
    list_display = ('thumbnail', 'name', 'url', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    readonly_fields = ('thumbnail',)
