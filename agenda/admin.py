from django.contrib import admin

from core.admin_mixins import ThumbnailAdminMixin

from .models import AgendaFeatured, AgendaRecurring


@admin.register(AgendaFeatured)
class AgendaFeaturedAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'image'
    list_display = ('thumbnail', 'title', 'date_label', 'active')
    list_filter = ('active',)
    readonly_fields = ('thumbnail',)

    def has_add_permission(self, request):
        # Only one featured event is shown at a time; edit the existing one instead.
        return not AgendaFeatured.objects.exists()


@admin.register(AgendaRecurring)
class AgendaRecurringAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'image'
    list_display = ('thumbnail', 'title', 'month', 'date_label', 'time_label', 'order')
    list_editable = ('order',)
    list_filter = ('month',)
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('thumbnail',)
