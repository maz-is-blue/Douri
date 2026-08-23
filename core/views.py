from django.contrib import messages
from django.shortcuts import render

from interviews.models import Interview
from people.models import Partner, TeamMember
from projects.models import Project
from social.models import InstagramPost

from .forms import ContactForm, SupportForm, VolunteerForm
from .models import HeroSlide

ABOUT_EXCERPT = (
    "At Douri, we foster connections among artists, researchers, social workers and activists, "
    "across the diverse tapestry of European society. As a non-profit organization headquartered "
    "in Luxembourg, our sociocultural initiative is dedicated to exploring, experimenting and "
    "advocating for intercultural exchange within Luxembourg and across Europe."
)
ABOUT_EXCERPT_2 = (
    "The name “Douri” derives from Arabic, meaning the sparrow — a resilient bird "
    "that thrives across the globe. Like the sparrow, we champion adaptability and integration, "
    "advocating for freedom of expression while staunchly opposing discrimination, inequality and "
    "violence."
)

ABOUT_BODY = [
    ABOUT_EXCERPT,
    "Our mission revolves around creating tangible impacts within our communities. Through both "
    "physical and digital platforms hosting artistic and sociocultural projects, we aim to "
    "facilitate the integration of various groups and individuals.",
    ABOUT_EXCERPT_2,
    "One of our key missions is to raise awareness about pressing ecological and environmental "
    "challenges in our modern world.",
    "Luxembourg serves as our launchpad for implementing projects using diverse communicative "
    "tools: from visual art, social theatre and music to performances, workshops, books, "
    "qualitative research, conferences and other innovative mediums.",
    "Our goal is to bridge societal gaps, emphasising the core of human existence in a rapidly "
    "changing world. Join us on this journey of unity, expression and advocacy, as we strive to "
    "transcend boundaries, celebrate diversity and embrace the essence of humanity.",
]

FOCUS_AREAS = [
    {
        'title': 'Visual arts',
        'text': 'Exhibitions and art panels that tell the stories of diverse communities.',
    },
    {
        'title': 'Social theatre',
        'text': 'Interactive presentations that spread awareness and social change.',
    },
    {
        'title': 'Music and performance',
        'text': 'Audio experiences that bring different cultures together.',
    },
    {
        'title': 'Publishing and research',
        'text': 'Books and research on pressing social and environmental issues.',
    },
    {
        'title': 'Seminars and conferences',
        'text': 'Platforms where experts and thinkers discuss sustainable solutions.',
    },
]

OUR_MESSAGE = [
    'Promoting cultural exchange through art and social initiatives.',
    'Creating a tangible impact within communities through cultural and field art projects.',
    'Highlighting contemporary environmental issues and ecological challenges.',
    'Connecting diverse individuals and groups through workshops, presentations, research and conferences.',
]

VOLUNTEER_CHARTER = [
    {
        'n': '01',
        'title': 'Dignity first',
        'text': 'Every person we work with is met as a whole person, never as a case or a story to '
        'be used. Nobody is asked to perform their suffering.',
    },
    {
        'n': '02',
        'title': 'Consent, always',
        'text': 'Participation is voluntary at every step. Anyone can stop, leave a session, or ask '
        'for their photo, name or work not to be shared — without explaining why.',
    },
    {
        'n': '03',
        'title': 'Confidentiality',
        'text': 'What is shared in a workshop stays in the workshop. We do not repeat participants’ '
        'stories outside the room, online or to funders.',
    },
    {
        'n': '04',
        'title': 'No discrimination',
        'text': 'We reject discrimination of any kind — on origin, religion, gender, sexuality, '
        'disability, language or status — in our rooms and in our public work.',
    },
    {
        'n': '05',
        'title': 'Care for yourself too',
        'text': 'This work touches difficult material. Volunteers are supported, debriefed and never '
        'expected to hold it alone. Ask for help early.',
    },
    {
        'n': '06',
        'title': 'Show up as agreed',
        'text': 'People plan their week around a session. Come when you said you would, and tell us '
        'in good time when you can’t.',
    },
]

MEMBER_STEPS = [
    {
        'n': '1',
        'title': 'Read the charter',
        'text': 'It sets out how we work together and what we ask of each other.',
    },
    {
        'n': '2',
        'title': 'Fill in the membership form',
        'text': 'Name, contact details and how you would like to be involved.',
    },
    {
        'n': '3',
        'title': 'Pay the annual fee of €15',
        'text': 'By transfer to the IBAN on this page. Membership runs for one calendar year.',
    },
]


def home(request):
    context = {
        'hero_slides': HeroSlide.objects.filter(active=True),
        'about_excerpt': ABOUT_EXCERPT,
        'about_excerpt_2': ABOUT_EXCERPT_2,
        'focus_areas': FOCUS_AREAS,
        'our_message': OUR_MESSAGE,
        'interviews': Interview.objects.all()[:3],
        'projects': Project.objects.all()[:6],
        'team': TeamMember.objects.all()[:6],
        'partners': Partner.objects.all(),
        'instagram_posts': InstagramPost.objects.filter(featured_on_home=True)[:5],
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html', {'about_body': ABOUT_BODY})


def volunteer(request):
    sent = False
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.subject = 'volunteer'
            submission.save()
            messages.success(request, "Thank you — we'll be in touch.")
            sent = True
            form = VolunteerForm()
    else:
        form = VolunteerForm()
    return render(
        request,
        'volunteer.html',
        {'form': form, 'sent': sent, 'charter': VOLUNTEER_CHARTER},
    )


def support_us(request):
    sent = False
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.subject = 'donations'
            submission.save()
            messages.success(request, "Thank you — we'll be in touch.")
            sent = True
            form = SupportForm()
    else:
        form = SupportForm()
    return render(
        request,
        'support_us.html',
        {'form': form, 'sent': sent, 'member_steps': MEMBER_STEPS},
    )


def contact(request):
    sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — we'll be in touch.")
            sent = True
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'sent': sent})


def shop(request):
    return render(request, 'shop.html')
