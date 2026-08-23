from django.db import models


class InstagramPost(models.Model):
    """A manually curated Instagram post: paste the link, upload a screenshot.

    A live feed (SnapWidget / Elfsight embed) is a fast future upgrade if the
    team wants automatic syncing later — see README.
    """

    image = models.ImageField('Screenshot', upload_to='instagram/')
    caption = models.CharField('What the post is about', max_length=250, blank=True)
    post_url = models.URLField('Instagram link')
    featured_on_home = models.BooleanField(
        'Show in the homepage strip', default=False
    )
    project = models.ForeignKey(
        'projects.Project', null=True, blank=True, related_name='social_highlights',
        on_delete=models.SET_NULL,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']
        verbose_name = 'Instagram post'

    def __str__(self):
        return self.caption or self.post_url
