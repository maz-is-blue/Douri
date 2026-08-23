from ckeditor.fields import RichTextField
from django.db import models


class TeamMember(models.Model):
    """Shown on the homepage and, with the full biography, on the Our Team page."""

    name = models.CharField(max_length=150)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/', help_text='A square photo works best.')
    short_bio = models.CharField(max_length=300, help_text='One line, used on the homepage.')
    full_bio = RichTextField(help_text='The longer biography shown on the Our Team page.')
    social_url = models.URLField('Profile link', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name


class Partner(models.Model):
    """A logo in the 'Supported by' strip."""

    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='partners/')
    url = models.URLField('Website', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name
