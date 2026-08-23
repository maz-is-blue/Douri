from django.contrib import admin

from core.admin_mixins import ThumbnailAdminMixin

from .models import Project, ProjectCTA, ProjectClosingLink, Workshop


class ProjectCTAInline(admin.TabularInline):
    model = ProjectCTA
    extra = 1
    fields = ('label', 'url', 'order')


class ProjectClosingLinkInline(admin.TabularInline):
    model = ProjectClosingLink
    extra = 1
    fields = ('label', 'url')


class WorkshopInline(admin.StackedInline):
    model = Workshop
    extra = 0
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'image', 'date_label', 'excerpt', 'body')
    show_change_link = True


@admin.register(Project)
class ProjectAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'hero_image'
    list_display = ('thumbnail', 'title', 'tagline', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'tagline', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('related_interviews',)
    inlines = [WorkshopInline, ProjectCTAInline, ProjectClosingLinkInline]
    readonly_fields = ('thumbnail',)
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'tagline', 'description', 'hero_image', 'thumbnail', 'order')}),
        (
            'Workshops section',
            {
                'fields': ('show_workshops',),
                'description': 'Workshops themselves are added below, at the bottom of this page.',
            },
        ),
        (
            'Project film',
            {
                'fields': ('show_film', 'film_url', 'film_title', 'film_text', 'film_poster'),
                'classes': ('collapse',),
            },
        ),
        (
            'Related content',
            {'fields': ('show_interviews', 'related_interviews', 'show_social')},
        ),
        ('Closing call to action', {'fields': ('show_closing_cta',)}),
    )


@admin.register(Workshop)
class WorkshopAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    thumbnail_field = 'image'
    list_display = ('thumbnail', 'title', 'project', 'date_label')
    list_filter = ('project',)
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('thumbnail',)
