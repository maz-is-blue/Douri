from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    """A Douri project. Each one gets its own page at /projects/<slug>/."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, help_text='Auto-filled from the title. This becomes /projects/…')
    tagline = models.CharField(max_length=300, blank=True, help_text='Shown under the title and in the projects grid.')
    description = models.TextField(
        blank=True, help_text='A short introduction paragraph at the top of the page. Leave empty to hide it.'
    )
    hero_image = models.ImageField(upload_to='projects/')

    show_workshops = models.BooleanField(default=True, help_text='Turn off if this project has no workshop recaps yet.')
    show_film = models.BooleanField(default=False)
    film_url = models.URLField(blank=True, help_text='A YouTube link, shown in the project film section.')
    film_title = models.CharField(max_length=200, blank=True)
    film_text = models.TextField(blank=True)
    film_poster = models.ImageField(upload_to='projects/film/', blank=True, null=True)
    show_interviews = models.BooleanField(default=True, help_text='Show interviews related to this project.')
    show_social = models.BooleanField(default=True, help_text='Show Instagram highlights for this project.')
    show_closing_cta = models.BooleanField(default=True, help_text='Show the closing "Join the conversation" block.')

    related_interviews = models.ManyToManyField(
        'interviews.Interview', blank=True, related_name='related_projects'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectCTA(models.Model):
    """A call-to-action button shown in a project's hero banner."""

    project = models.ForeignKey(Project, related_name='ctas', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'CTA button'
        verbose_name_plural = 'CTA buttons'

    def __str__(self):
        return f'{self.label} ({self.project.title})'


class Workshop(models.Model):
    """A co-creation workshop recap that belongs to a project."""

    project = models.ForeignKey(Project, related_name='workshops', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, help_text='Auto-filled from the title.')
    image = models.ImageField(upload_to='workshops/')
    date_label = models.CharField(max_length=100, help_text='e.g. "October 2025"')
    excerpt = models.TextField(help_text='One or two lines, shown on the project page.')
    body = RichTextField(help_text="The full recap text, shown on the workshop's own page.")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectClosingLink(models.Model):
    """A resource link in a project's closing 'Join the conversation' block."""

    project = models.ForeignKey(Project, related_name='closing_links', on_delete=models.CASCADE)
    label = models.CharField(max_length=150)
    url = models.URLField()

    def __str__(self):
        return self.label
