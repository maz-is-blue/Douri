from django.utils.html import format_html


class ThumbnailAdminMixin:
    """Adds a small image preview to the admin list view and change form.

    Set `thumbnail_field` to the name of the model's ImageField.
    """

    thumbnail_field = 'image'

    def thumbnail(self, obj):
        image = getattr(obj, self.thumbnail_field, None)
        if not image:
            return '—'
        return format_html(
            '<img src="{}" style="height:48px;width:64px;object-fit:cover;border-radius:4px" />',
            image.url,
        )

    thumbnail.short_description = 'Preview'
