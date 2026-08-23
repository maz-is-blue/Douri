from django.db import models


class HeroSlide(models.Model):
    """One rotating slide in the homepage hero carousel."""

    image = models.ImageField(
        upload_to='hero/', help_text='Landscape photo, at least 1600px wide.'
    )
    eyebrow = models.CharField(
        max_length=100, help_text='Small line above the title, e.g. the date and place of an event.'
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, help_text='One or two sentences.')
    cta_label = models.CharField(
        max_length=50, default='Learn more', help_text='Text on the button, e.g. "Register now".'
    )
    cta_link = models.CharField(
        max_length=300, blank=True, help_text='Where the button goes, e.g. /projects or a full URL.'
    )
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True, help_text='Untick to hide this slide without deleting it.')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Hero slide'

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Contact details, bank details and footer text used across the whole site. Single row."""

    email = models.EmailField(default='info@douri.lu')
    phone = models.CharField(max_length=50, default='+(352) 661 158300')
    address = models.TextField(default="108, Route d'Esch, L-4450 Belvaux, Sanem, Luxembourg")
    rcs = models.CharField(
        'Registration number', max_length=100, default='R.C.S Luxembourg F12823'
    )
    iban = models.CharField(
        max_length=50,
        default='LU00 0000 0000 0000 0000',
        help_text='Shown on the Support Us page with a copy button.',
    )
    facebook_url = models.URLField('Facebook', blank=True, default='https://www.facebook.com/Douri.asbl')
    instagram_url = models.URLField('Instagram', blank=True, default='https://www.instagram.com/douri.asbl')
    footer_text = models.TextField(
        default='Join us on this journey of unity, expression and advocacy, as we strive to '
        'transcend boundaries, celebrate diversity and embrace the essence of humanity.'
    )

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return 'Site settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FormSubmission(models.Model):
    """A message sent from the Contact, Volunteer or Support Us page."""

    SUBJECT_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('donations', 'Donations'),
        ('food', 'Food Support'),
        ('education', 'Education Support'),
        ('medical', 'Medical Support'),
        ('sports', 'Sports Support'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} · {self.get_subject_display() or "General"}'
