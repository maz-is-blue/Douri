from django.db import models


class AgendaFeatured(models.Model):
    """The big featured-event block at the top of the Agenda page."""

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='agenda/')
    description = models.TextField()
    participants = models.TextField(help_text='One per line, e.g. "Exhibition: Name1, Name2"')
    date_label = models.CharField('Date', max_length=150)
    location = models.CharField(max_length=250)
    entry = models.CharField(
        max_length=150, blank=True, default='Free entry — registration required'
    )
    register_url = models.URLField('Registration link', help_text='A Google Form link works fine.')
    active = models.BooleanField(default=True, help_text='Untick when the event is over.')

    class Meta:
        verbose_name = 'Featured event'
        ordering = ['-id']

    def __str__(self):
        return self.title

    @property
    def participant_lines(self):
        return [line.strip() for line in self.participants.splitlines() if line.strip()]


class AgendaRecurring(models.Model):
    """A recurring workshop session shown on the Agenda page, grouped by month."""

    image = models.ImageField(upload_to='agenda/')
    title = models.CharField(max_length=200, default='')
    time_label = models.CharField('Time', max_length=100, help_text='e.g. "15:00 – 16:30"')
    description = models.TextField()
    dates_label = models.CharField('All dates', max_length=250, help_text='Separate with a dot or a dash.')
    location = models.CharField(max_length=250)
    price_tiers = models.CharField('Prices', max_length=250)
    languages = models.CharField(max_length=150)
    info_url = models.URLField('Info link', blank=True, help_text='Often an Instagram video.')
    register_url = models.URLField('Registration link')
    month = models.CharField(max_length=20, help_text='e.g. "March 2026" — decides where this appears on the page.')
    date_label = models.CharField('Date shown', max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Recurring workshop'
        ordering = ['month', 'order', 'id']

    def __str__(self):
        return f'{self.title} · {self.month}'
