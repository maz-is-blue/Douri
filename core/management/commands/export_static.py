"""Exports the site as flat HTML for a static preview (e.g. GitHub Pages).

GitHub Pages can only serve static files — it can't run Django, the admin,
or the forms. This command renders every page to disk with all internal
links, static assets and media prefixed for the given base path, so the
result is browsable as a look-alike of the real site. Nothing here should be
treated as the production deployment target — see README "Going to
production" for that.

Usage:
    python manage.py export_static                  # writes to docs/, prefix /Douri/
    python manage.py export_static --base-path /foo/
    python manage.py export_static --out-dir dist
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test import RequestFactory, override_settings
from django.urls import resolve, reverse, set_script_prefix

from agenda.models import AgendaFeatured, AgendaRecurring  # noqa: F401 (imported for completeness)
from interviews.models import Interview
from projects.models import Project, Workshop


class Command(BaseCommand):
    help = 'Render every page to static HTML for a GitHub Pages preview.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--base-path', default='/Douri/',
            help='Path the site will be served under, e.g. /Douri/ for a GitHub Pages '
            'project site at https://<user>.github.io/Douri/. Must start and end with /.',
        )
        parser.add_argument('--out-dir', default='docs', help='Output directory (relative to the project root).')

    def handle(self, *args, **options):
        base_path = options['base_path']
        if not base_path.startswith('/') or not base_path.endswith('/'):
            self.stderr.write(self.style.ERROR('--base-path must start and end with /'))
            return

        out_dir = Path(settings.BASE_DIR) / options['out_dir']
        if out_dir.exists():
            shutil.rmtree(out_dir)
        out_dir.mkdir(parents=True)

        settings.ALLOWED_HOSTS = ['*']
        factory = RequestFactory()

        # Collect paths with the default ('/') script prefix so resolve() matches
        # the real urlconf; switch to the export prefix only for rendering.
        paths = self.collect_paths()

        # STATIC_URL/MEDIA_URL feed FileSystemStorage.base_url, a cached_property
        # that only refreshes on Django's setting_changed signal — plain attribute
        # assignment on `settings` doesn't fire it, override_settings does.
        with override_settings(
            STATIC_URL=f"{base_path}static/",
            MEDIA_URL=f"{base_path}media/",
        ):
            set_script_prefix(base_path)
            for path in paths:
                match = resolve(path)
                request = factory.get(path)
                response = match.func(request, *match.args, **match.kwargs)
                if hasattr(response, 'render'):
                    response.render()
                if response.status_code != 200:
                    self.stdout.write(self.style.WARNING(f'{path} -> HTTP {response.status_code}, skipped'))
                    continue
                dest = self.dest_for(out_dir, path)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(response.content)
                self.stdout.write(f'wrote {dest.relative_to(out_dir)}')
            set_script_prefix('/')

        static_src = Path(settings.BASE_DIR) / 'static'
        if static_src.exists():
            shutil.copytree(static_src, out_dir / 'static', dirs_exist_ok=True)

        media_src = Path(settings.MEDIA_ROOT)
        if media_src.exists():
            shutil.copytree(media_src, out_dir / 'media', dirs_exist_ok=True)
        else:
            self.stdout.write(self.style.WARNING(
                'No media/ directory found — run `python manage.py seed_content` first '
                'so projects/interviews/etc. have photos.'
            ))

        (out_dir / '.nojekyll').touch()

        self.stdout.write(self.style.SUCCESS(
            f'Static preview written to {out_dir}/ for base path {base_path}\n'
            'This is a look-alike snapshot only: the admin dashboard and the '
            'Contact/Volunteer/Support Us forms will not work (no backend on GitHub Pages).'
        ))

    def collect_paths(self):
        paths = [
            reverse('core:home'),
            reverse('core:about'),
            reverse('projects:list'),
            reverse('interviews:list'),
            reverse('agenda:agenda'),
            reverse('people:our-team'),
            reverse('core:volunteer'),
            reverse('core:support-us'),
            reverse('core:contact'),
            reverse('core:shop'),
        ]
        paths += [reverse('projects:detail', args=[p.slug]) for p in Project.objects.all()]
        paths += [reverse('workshops:detail', args=[w.slug]) for w in Workshop.objects.all()]
        paths += [reverse('interviews:detail', args=[i.slug]) for i in Interview.objects.all()]
        return paths

    @staticmethod
    def dest_for(out_dir, path):
        segments = [s for s in path.split('/') if s]
        if not segments:
            return out_dir / 'index.html'
        return out_dir.joinpath(*segments) / 'index.html'
