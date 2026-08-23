"""Seeds the database with Douri's real copy — team bios, project descriptions,
interview text, agenda sessions — pulled from the association's own materials.

Photography is not available in this repo, so every image field is filled
with a locally generated placeholder (see core/placeholder.py); staff replace
these with real photos through the admin exactly as they would for new
content going forward.

Usage:
    python manage.py seed_content            # seed if empty
    python manage.py seed_content --flush     # wipe seeded tables and reseed
"""

import datetime

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from agenda.models import AgendaFeatured, AgendaRecurring
from core.models import HeroSlide, SiteSettings
from core.placeholder import make_placeholder
from interviews.models import Interview
from people.models import Partner, TeamMember
from projects.models import Project, ProjectCTA, ProjectClosingLink, Workshop
from social.models import InstagramPost


def image_for(field, label, width=1200, height=800):
    field.save(f'{label}.jpg', ContentFile(make_placeholder(label, width, height).read()), save=False)


class Command(BaseCommand):
    help = 'Seed the database with Douri’s real content and placeholder photography.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', action='store_true', help='Delete existing seeded content first.'
        )

    def handle(self, *args, **options):
        if options['flush']:
            self.stdout.write('Flushing existing content…')
            for model in [
                InstagramPost, AgendaRecurring, AgendaFeatured, Interview,
                Workshop, ProjectCTA, ProjectClosingLink, Project,
                TeamMember, Partner, HeroSlide,
            ]:
                model.objects.all().delete()

        if Project.objects.exists() and not options['flush']:
            self.stdout.write(self.style.WARNING(
                'Projects already exist — skipping seed. Use --flush to reseed.'
            ))
            return

        self.seed_site_settings()
        self.seed_hero_slides()
        projects_by_slug = self.seed_projects()
        self.seed_workshops(projects_by_slug)
        interviews_by_slug = self.seed_interviews(projects_by_slug)
        self.seed_agenda()
        self.seed_team()
        self.seed_partners()
        self.seed_instagram(projects_by_slug)

        self.stdout.write(self.style.SUCCESS('Douri content seeded.'))

    # ------------------------------------------------------------------

    def seed_site_settings(self):
        settings_obj = SiteSettings.load()
        settings_obj.email = 'info@douri.lu'
        settings_obj.phone = '+(352) 661 158300'
        settings_obj.address = "108, Route d'Esch, L-4450 Belvaux, Sanem, Luxembourg"
        settings_obj.rcs = 'R.C.S Luxembourg F12823'
        settings_obj.iban = 'LU00 0000 0000 0000 0000 (placeholder — replace with the real account)'
        settings_obj.facebook_url = 'https://www.facebook.com/Douri.asbl'
        settings_obj.instagram_url = 'https://www.instagram.com/douri.asbl'
        settings_obj.footer_text = (
            'Join us on this journey of unity, expression and advocacy, as we strive to '
            'transcend boundaries, celebrate diversity and embrace the essence of humanity.'
        )
        settings_obj.save()
        self.stdout.write('Site settings set.')

    def seed_hero_slides(self):
        slides = [
            dict(
                eyebrow='26 & 27 June 2026 · Maison du Savoir, Belval',
                title='Join our Final Forum',
                subtitle='Empowering Creative Minds — exhibition, conferences and performances '
                'closing two years of work across four countries.',
                cta_label='Register now', cta_link='https://forms.gle/Q6WHPFhFiECFsvRv8',
                order=0,
            ),
            dict(
                eyebrow='Welcome to Douri',
                title='Art as a tool for dialogue',
                subtitle='We believe in the power of art and cultural exchange in building more '
                'equal and inclusive societies.',
                cta_label='See our projects', cta_link='/projects/',
                order=1,
            ),
            dict(
                eyebrow='Every week in Soleuvre',
                title='Douri’s Salon',
                subtitle='Movement, theatre and storytelling workshops — open to all levels, '
                'in several languages.',
                cta_label='See the agenda', cta_link='/events/',
                order=2,
            ),
        ]
        for data in slides:
            slide = HeroSlide(**data)
            image_for(slide.image, data['title'], 1600, 900)
            slide.save()
        self.stdout.write(f'Seeded {len(slides)} hero slides.')

    def seed_projects(self):
        projects_data = [
            dict(
                title='Empowering Creative Minds',
                tagline='Art, healing and dialogue across Europe',
                description=(
                    'A European project dedicated to fostering trauma-informed artistic '
                    'practice. Between August and October 2025, three pilot co-creation '
                    'workshops brought artists from Luxembourg, Germany, Poland and Ukraine '
                    'into one shared room.'
                ),
                show_workshops=True, show_film=True,
                film_url='https://youtu.be/qXC6dc_MuW0',
                film_title='A cross-border laboratory',
                film_text=(
                    'Between August and October 2025, Empowering Creative Minds carried out '
                    'three pilot co-creation workshops across Europe, establishing a '
                    'cross-border laboratory for trauma-informed artistic practice.'
                ),
                show_interviews=True, show_social=True, show_closing_cta=True,
                ctas=[
                    ('Explore workshops', '/projects/empowering-creative-minds/#project-workshops'),
                    ('Watch the project film', 'https://youtu.be/qXC6dc_MuW0'),
                    ('Read recommendations', 'https://drive.google.com/file/d/1IFn_NeGDm1LZEDS6wKECSuSpl6kuziqQ/view'),
                ],
                closing_links=[
                    ('Trainer’s activity handbook', 'https://drive.google.com/file/d/1wG2WQbSNRSC6AG9eQgvlxCKc-7eb1n4A/view'),
                    ('Empowering Creative Minds — EU', 'https://empoweringcreativity.eu'),
                ],
            ),
            dict(
                title='L’Art à Partager',
                tagline='Sharing the memories of older people through art',
                description=(
                    'Le passé des personnes âgées constitue une richesse. L’Art à Partager '
                    'brings elders and artists together to turn lived memory into shared work.'
                ),
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=True,
                closing_links=[('Registration form', 'https://douri.lu/projects/lart-a-partager/')],
            ),
            dict(
                title='LEILaw',
                tagline='Movement, dance and film workshops for women',
                description=(
                    'A programme of dance, yoga and film workshops built around women’s '
                    'safety, confidence and joy — from “Dance it Out” to yoga sessions with AVA.'
                ),
                show_workshops=False, show_film=True,
                film_url='https://douri.lu/the-opposite-of-the-riverside/',
                film_title='The Opposite of The Riverside',
                film_text='The Opposite of The Riverside, a film by Nael Nassan, made within the LEILaw programme.',
                show_interviews=False, show_social=False, show_closing_cta=False,
            ),
            dict(
                title='Narration Floraison',
                tagline='An interactive storytelling workshop, in two rounds',
                description=(
                    'Two rounds of a magical interactive storytelling workshop, where '
                    'participants build a story together and watch it bloom.'
                ),
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
            dict(
                title='Porte-Voix',
                tagline='Amplifying voices that are rarely heard',
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
            dict(
                title='Parlez Facil',
                tagline='Language practice as a social space',
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
            dict(
                title='Basics of Video Making',
                tagline='Telling your own story on camera',
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
            dict(
                title='My Voice is My Power',
                tagline='Theatre and testimony with survivors of violence',
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
            dict(
                title='Story Telling',
                tagline='Everything is a story, and everyone is a book',
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
            dict(
                title='Weaving Futures',
                tagline='Craft, work and belonging',
                show_workshops=False, show_film=False, show_interviews=False,
                show_social=False, show_closing_cta=False,
            ),
        ]

        by_slug = {}
        for order, data in enumerate(projects_data):
            ctas = data.pop('ctas', [])
            closing_links = data.pop('closing_links', [])
            project = Project(order=order, **data)
            image_for(project.hero_image, project.title)
            if project.show_film:
                image_for(project.film_poster, f'{project.title} film')
            project.save()
            for i, (label, url) in enumerate(ctas):
                ProjectCTA.objects.create(project=project, label=label, url=url, order=i)
            for label, url in closing_links:
                ProjectClosingLink.objects.create(project=project, label=label, url=url)
            by_slug[project.slug] = project

        self.stdout.write(f'Seeded {len(by_slug)} projects.')
        return by_slug

    def seed_workshops(self, projects_by_slug):
        ecm = projects_by_slug['empowering-creative-minds']
        workshops_data = [
            dict(
                title='Co-Creation Journey Lublin', date_label='October 2025',
                excerpt='The body remembers. The voice carries. The rhythm connects.',
                body_paragraphs=[
                    'The body remembers. The voice carries. The rhythm connects.',
                    'Artists from Luxembourg, Germany, Poland and Ukraine gathered at Teatr '
                    'Wschodni — the Eastern Theater — a place its founder describes as '
                    'existing between the end and renewal.',
                    'Different rhythms. Different wounds. Different ways of carrying what '
                    'cannot be put down. One shared room. Exactly the right one.',
                ],
            ),
            dict(
                title='Co-Creation Journey Berlin', date_label='September 2025',
                excerpt='Creativity meets care. Art becomes voice. Community becomes support.',
                body_paragraphs=[
                    'Creativity meets care. Art becomes voice. Community becomes support.',
                    'Artists from Luxembourg, Germany, Poland and Ukraine gathered at the '
                    'foot of the East Side Gallery — a wall that was once a wound and is '
                    'now a testament.',
                    'Different languages. Different histories. Different ways of carrying '
                    'what cannot be put down. One shared question: what does it mean to '
                    'make something from what has broken you?',
                ],
            ),
            dict(
                title='Co-Creation Journey Luxembourg', date_label='August 2025',
                excerpt='Expression is not a luxury. It never was.',
                body_paragraphs=[
                    'Expression is not a luxury. It never was. A new way of seeing.',
                    'Twelve artists from Luxembourg, Germany, Poland and Ukraine came '
                    'together in a single room. Different languages. Different journeys.',
                    'One shared intention: to find a way of expressing what words alone '
                    'cannot carry.',
                ],
            ),
        ]
        for data in workshops_data:
            paragraphs = data.pop('body_paragraphs')
            workshop = Workshop(
                project=ecm,
                body=''.join(f'<p>{p}</p>' for p in paragraphs),
                **data,
            )
            image_for(workshop.image, workshop.title, 1000, 1400)
            workshop.save()
        self.stdout.write(f'Seeded {len(workshops_data)} workshops.')

    def seed_interviews(self, projects_by_slug):
        ecm = projects_by_slug['empowering-creative-minds']
        interviews_data = [
            dict(
                subject_name='Lourain Alhalabi', quote='“You take a risk as a vulnerable artist”',
                publish_date=datetime.date(2026, 7, 16),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[
                    'Lourain Alhalabi is a young artist whose art is deeply inspired by her '
                    'lived experiences. As a Syrian refugee, Alhalabi processes and shares '
                    'her life back in Syria, as well as the journey that followed.',
                ],
            ),
            dict(
                subject_name='Tarek Al-Nabhan', quote='“When words fall short, movement speaks”',
                publish_date=datetime.date(2026, 6, 3),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[
                    'Tarek Al-Nabhan is passionate about the fluidity of movement and the '
                    'art of connection. After experimenting with different types of Western '
                    'dance, he fell in love with Contact Improvisation (CI) and became a '
                    'teacher of the form.',
                ],
            ),
            dict(
                subject_name='UNO', quote='“If you want diversity, support the roots, not just the flowers”',
                publish_date=datetime.date(2026, 5, 13),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[
                    'Uyi Nosa-Odia, known as UNO, is a Luxembourgish-Nigerian curator and '
                    'painter specialised in Afrocentric contemporary art. His cultural '
                    'heritage as well as his personal history shape his artistic approach.',
                ],
            ),
            dict(
                subject_name='Olga Alexandrova', quote='“Everything is a story, and everyone is a book”',
                publish_date=datetime.date(2026, 2, 16),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[],
            ),
            dict(
                subject_name='Farshad Afsharimehr', quote='“Challenging experiences feed my artistic inspirations”',
                publish_date=datetime.date(2026, 2, 13),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[],
            ),
            dict(
                subject_name='Adham Al-Sayyad', quote='“Collective healing can emerge through sound”',
                publish_date=datetime.date(2026, 2, 6),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[],
            ),
            dict(
                subject_name='Priscila Da Costa', quote='“I used to intentionally seek to impact others, I don’t anymore”',
                publish_date=datetime.date(2026, 1, 3),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[],
            ),
            dict(
                subject_name='Nathalie Lesure', quote='“I don’t really believe in the myth of the isolated artist”',
                publish_date=datetime.date(2025, 11, 11),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[],
            ),
            dict(
                subject_name='Camille Kerger', quote='“Music is the engine and the cure for everything”',
                publish_date=datetime.date(2025, 10, 23),
                prepared_by='Douri’s Empowering Creative Minds team', edited_by='Jang Kapgen',
                body_paragraphs=[],
            ),
        ]
        by_slug = {}
        for data in interviews_data:
            paragraphs = data.pop('body_paragraphs') or [
                'Full interview text coming soon.'
            ]
            interview = Interview(
                body=''.join(f'<p>{p}</p>' for p in paragraphs),
                **data,
            )
            image_for(interview.hero_image, data['subject_name'], 1400, 500)
            interview.save()
            ecm.related_interviews.add(interview)
            by_slug[interview.slug] = interview
        self.stdout.write(f'Seeded {len(by_slug)} interviews.')
        return by_slug

    def seed_agenda(self):
        featured = AgendaFeatured(
            title='Final Forum — Empowering Creative Minds',
            description=(
                'Two years. Four countries. Countless stories turned into art. From '
                'Luxembourg to Germany, Poland and Ukraine, artists and communities came '
                'together to transform experience into form, silence into something '
                'visible. Now we gather one last time to celebrate this journey.'
            ),
            participants=(
                'Exhibition: Walid El-Masri · Farshad Afsharimehr · Nathalie Lesure · Ecran Arslan\n'
                'Performances: Valeria Khipatch · Agnieszka Sikorska · Tarek Al-Nabhan · Margaryta\n'
                'Conferences: Art, trauma & mental well-being · Arts policy & funding in Luxembourg'
            ),
            date_label='26 & 27 June 2026',
            location='Maison du Savoir, University of Luxembourg, Belval, Esch-sur-Alzette',
            entry='Free entry — registration required',
            register_url='https://forms.gle/Q6WHPFhFiECFsvRv8',
        )
        image_for(featured.image, featured.title, 1600, 500)
        featured.save()

        recurring_data = [
            dict(
                title='Contact Improvisation', month='March 2026', date_label='07 March 2026',
                time_label='15:00 – 16:30',
                description='An inclusive Contact Improvisation workshop open to all levels — no dance experience needed.',
                dates_label='07/03 · 21/03 · 28/03 · 18/04 · 25/04',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN',
                info_url='https://www.instagram.com/p/DTY2w6mjGBb/',
                register_url='https://forms.gle/pULJttRKKqJB77Rq7', order=0,
            ),
            dict(
                title='Physical theatre & somatic dance', month='March 2026', date_label='11 March 2026',
                time_label='18:30 – 20:30',
                description='A journey through dance practices inspired by physical theatre, somatic work and martial arts.',
                dates_label='11/03 · 18/03 · 25/03 · 01/04 · 15/04',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN, UK',
                info_url='https://www.instagram.com/p/DTY2w6mjGBb/',
                register_url='https://forms.gle/qV2ESc66Dc7DwW748', order=1,
            ),
            dict(
                title='New Butoh', month='March 2026', date_label='21 March 2026',
                time_label='11:00 – 13:00',
                description='Discover the art of New Butoh, a Japanese expressive dance that transforms inner energy, emotions and memories into movement.',
                dates_label='21/03 · 20/06 · 11/07 · 18/07 · 19/09',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN, UK',
                info_url='https://www.instagram.com/p/DVZI3L9DsYs/',
                register_url='https://forms.gle/2s7FWC2qZxHoVJCB9', order=2,
            ),
            dict(
                title='Contact Improvisation', month='March 2026', date_label='28 March 2026',
                time_label='15:00 – 16:30',
                description='An inclusive Contact Improvisation workshop open to all levels — no dance experience needed.',
                dates_label='07/03 · 21/03 · 28/03 · 18/04 · 25/04',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN',
                info_url='https://www.instagram.com/p/DTY2w6mjGBb/',
                register_url='https://forms.gle/pULJttRKKqJB77Rq7', order=3,
            ),
            dict(
                title='Physical theatre & somatic dance', month='April 2026', date_label='01 April 2026',
                time_label='18:30 – 20:30',
                description='A journey through dance practices inspired by physical theatre, somatic work and martial arts.',
                dates_label='11/03 · 18/03 · 25/03 · 01/04 · 15/04',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN, UK',
                info_url='https://www.instagram.com/p/DTY2w6mjGBb/',
                register_url='https://forms.gle/qV2ESc66Dc7DwW748', order=4,
            ),
            dict(
                title='Contact Improvisation', month='April 2026', date_label='18 April 2026',
                time_label='15:00 – 16:30',
                description='An inclusive Contact Improvisation workshop open to all levels — no dance experience needed.',
                dates_label='07/03 · 21/03 · 28/03 · 18/04 · 25/04',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN',
                info_url='https://www.instagram.com/p/DTY2w6mjGBb/',
                register_url='https://forms.gle/pULJttRKKqJB77Rq7', order=5,
            ),
            dict(
                title='Contact Improvisation', month='April 2026', date_label='25 April 2026',
                time_label='15:00 – 16:30',
                description='An inclusive Contact Improvisation workshop open to all levels — no dance experience needed.',
                dates_label='07/03 · 21/03 · 28/03 · 18/04 · 25/04',
                price_tiers='Drop-in 40€ · 3 sessions 100€ · 5 sessions 145€', languages='FR, EN',
                info_url='https://www.instagram.com/p/DTY2w6mjGBb/',
                register_url='https://forms.gle/pULJttRKKqJB77Rq7', order=6,
            ),
        ]
        location = 'Douri’s Salon, 10 Rue du Château, 4433 Soleuvre'
        for data in recurring_data:
            item = AgendaRecurring(location=location, **data)
            image_for(item.image, f"{data['title']} {data['date_label']}", 800, 900)
            item.save()

        self.stdout.write(f'Seeded featured event and {len(recurring_data)} recurring sessions.')

    def seed_team(self):
        team_data = [
            dict(
                name='Yusra Amounah', role='President',
                short_bio='President of Douri asbl.',
                full_bio_paragraphs=[
                    'Yusra Amounah is the president of Douri asbl and leads the '
                    'association’s strategic direction — from project design and European '
                    'partnerships to the day-to-day of keeping a small non-profit running.',
                    'Her work centres on the question the association was founded around: '
                    'how art can give people displaced by war and violence a way to speak '
                    'for themselves, on their own terms.',
                ],
            ),
            dict(
                name='Fadi Jaafar', role='Member of Administration & Psycho-Social Support',
                short_bio='Administration and psycho-social support.',
                full_bio_paragraphs=[
                    'Fadi Jaafar combines an administrative role at Douri with '
                    'responsibility for psycho-social support, making sure that artistic '
                    'work with people who have lived through trauma is held in a safe, '
                    'trauma-informed frame.',
                    'He works closely with facilitators before, during and after '
                    'workshops, so that participants are never left alone with what a '
                    'session brings up.',
                ],
            ),
            dict(
                name='Lina', role='Member of the Board of Administration',
                short_bio='Board of administration.',
                full_bio_paragraphs=[
                    'Lina sits on Douri’s board of administration and contributes to '
                    'programme planning and the association’s governance.',
                    'Her focus is on making Douri’s activities genuinely reachable — the '
                    'practical questions of language, childcare, cost and location that '
                    'decide who can actually walk through the door.',
                ],
            ),
            dict(
                name='Samah Abdulhamid', role='Member of the Board of Administration',
                short_bio='Board of administration.',
                full_bio_paragraphs=[
                    'Samah Abdulhamid serves on the board of administration, supporting '
                    'Douri’s community work and the relationships that hold it together in '
                    'Luxembourg.',
                    'She helps connect the association with the people and organisations '
                    'it serves, so that projects grow out of real needs rather than '
                    'assumptions.',
                ],
            ),
            dict(
                name='Andy Wintringer', role='Member of the Board of Administration',
                short_bio='Board of administration.',
                full_bio_paragraphs=[
                    'Andy Wintringer is a member of Douri’s board of administration, '
                    'contributing to the association’s work with local institutions, '
                    'communes and cultural venues in Luxembourg.',
                    'That local grounding is what lets a small association place its work '
                    'in front of new audiences.',
                ],
            ),
            dict(
                name='Ola Al-Jari', role='Member of the Board of Administration',
                short_bio='Board of administration.',
                full_bio_paragraphs=[
                    'Ola Al-Jari serves on the board of administration and supports '
                    'Douri’s projects and workshop programme.',
                    'She works on the continuity between one-off events and long-term '
                    'participation — the difference between a workshop someone attended '
                    'and a community someone belongs to.',
                ],
            ),
        ]
        for order, data in enumerate(team_data):
            paragraphs = data.pop('full_bio_paragraphs')
            member = TeamMember(
                full_bio=''.join(f'<p>{p}</p>' for p in paragraphs),
                order=order,
                **data,
            )
            image_for(member.photo, data['name'], 800, 800)
            member.save()
        self.stdout.write(f'Seeded {len(team_data)} team members.')

    def seed_partners(self):
        partners_data = [
            dict(name='European Commission', url='https://commission.europa.eu/index_en'),
            dict(name='Fondation Sommer', url='https://fondation-sommer.lu/en/'),
            dict(name='Commune de Sanem', url='https://www.suessem.lu/fr/'),
        ]
        for order, data in enumerate(partners_data):
            partner = Partner(order=order, **data)
            image_for(partner.logo, data['name'], 600, 360)
            partner.save()
        self.stdout.write(f'Seeded {len(partners_data)} partners.')

    def seed_instagram(self, projects_by_slug):
        ecm = projects_by_slug['empowering-creative-minds']
        posts_data = [
            ('Empowering Creative Minds kick-off meeting in Berlin', True),
            ('What is Empowering Creative Minds?', True),
            ('Have you ever experienced a painful event that left you unable to express yourself?', True),
            ('What is trauma?', True),
            ('Types of psychological trauma and their impacts', True),
            ('Creativity’s role in healing', False),
            ('From trauma to understanding', False),
            ('Creative expression’s role in healing', False),
            ('Art & mental health', False),
            ('The Fluid Line', False),
            ('Expressive writing exercise', False),
        ]
        for order, (caption, featured) in enumerate(posts_data):
            post = InstagramPost(
                caption=caption, featured_on_home=featured, project=ecm, order=order,
                post_url='https://www.instagram.com/douri.asbl',
            )
            image_for(post.image, caption, 900, 1100)
            post.save()
        self.stdout.write(f'Seeded {len(posts_data)} Instagram posts.')
