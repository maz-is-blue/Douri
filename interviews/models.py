from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify


class Interview(models.Model):
    """A long-form interview — 'in their own words'."""

    title = models.CharField(
        max_length=250, blank=True, help_text='Internal title. If left empty, the quote is used.'
    )
    slug = models.SlugField(unique=True, blank=True, help_text='Auto-filled from the subject name.')
    subject_name = models.CharField('Person interviewed', max_length=150)
    quote = models.CharField(max_length=300, help_text='The headline quote, used as the page title.')
    prepared_by = models.CharField(max_length=200, blank=True)
    edited_by = models.CharField(max_length=200, blank=True)
    hero_image = models.ImageField(upload_to='interviews/')
    body = RichTextField(help_text='The full interview text.')
    publish_date = models.DateField()

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.quote

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject_name)
        super().save(*args, **kwargs)
