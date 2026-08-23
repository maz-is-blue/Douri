# Douri — website & content dashboard

The Django codebase for [douri.lu](https://douri.lu), a Luxembourg non-profit using art to
help refugees and marginalised communities process trauma and integrate. The whole site is
data-driven: every page (projects, workshops, interviews, agenda, team, partners) is rendered
from the database, and the Django admin — themed as the "Douri Dashboard" — is the CMS staff
use to add and edit it, with no code changes.

## Stack

- Python 3.12, Django 5
- SQLite for local dev (see "Going to production" below for Postgres)
- Pillow + `ImageField` for photography, served from local disk in dev
- `django-ckeditor` for rich text (interview bodies, workshop bodies, team bios)
- `django-jazzmin` for the themed admin dashboard
- Django templates + a single hand-written `static/css/design-system.css` — no frontend
  framework

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in SECRET_KEY etc. — see below
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_content    # optional: loads Douri's real copy + placeholder photos
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` for the
dashboard.

### `.env`

Copy `.env.example` to `.env` (never commit `.env`). At minimum, set a real `SECRET_KEY` for
anything beyond local dev. `DEBUG=True` and SQLite are the defaults if you set nothing else.

### `seed_content`

`python manage.py seed_content` loads Douri's real project descriptions, interview text, team
bios and agenda sessions — not lorem ipsum — so the site looks right immediately. Every image
field is filled with a locally generated placeholder photo (a solid colour with a label,
produced by `core/placeholder.py` using Pillow) since real photography isn't part of this
repo. Replace them through the admin exactly as you would for brand-new content.

Run `python manage.py seed_content --flush` to wipe the seeded rows and reseed from scratch.
It's safe to run without `--flush` at any time — it no-ops if projects already exist.

## How to add a new project (no code required)

This is the core "dashboard for everything" workflow:

1. Log into `/admin/` with a staff account.
2. Under **Projects**, click **Add project**. Fill in the title (the URL slug fills itself
   in), tagline, hero image and an optional introduction paragraph.
3. Tick the `show_*` boxes for whichever sections this project should display: workshops,
   film, related interviews, Instagram highlights, closing call-to-action. Leave the rest
   unticked — the project page hides those sections automatically.
4. Still on the same screen, add **workshops**, **CTA buttons** and **closing links** inline
   — no need to leave the page.
5. If the project has interviews, pick them from the **related interviews** picker
   (searchable, two-column widget).
6. Save. The project is live at `/projects/<slug>/` immediately.

The same pattern applies to interviews, agenda sessions, team members, partners and
Instagram posts — each is its own model in the dashboard sidebar, with image previews,
readable field labels and help text written for a social worker or media director, not a
developer.

### Singletons

**Site settings** (contact details, IBAN, footer text) and **Featured event** are singleton
models — the admin only lets you edit the existing row, so staff can't accidentally create a
duplicate "settings" record.

### Form submissions

Every message sent from the Contact, Volunteer and Support Us pages lands in **Form
submissions**, with filters for status (new / read / archived) and a bulk action to mark
messages as read or archived. There's no outgoing email integration in v1 — staff check the
inbox in the dashboard.

## Static UI preview (GitHub Pages)

GitHub Pages only serves static files — it can't run Django, so the admin dashboard and the
Contact/Volunteer/Support Us forms won't work there. For a look-only preview of the UI:

```bash
python manage.py seed_content     # if you haven't already
python manage.py export_static    # renders every page to docs/, links prefixed for /Douri/
git add docs && git commit -m "Update static preview" && git push
```

Then in the GitHub repo: **Settings → Pages → Source: Deploy from a branch → Branch: `main`,
folder: `/docs`**. The site will be live at `https://<your-username>.github.io/Douri/` a
minute or two later.

`export_static` re-renders every page with `{% url %}`/`{% static %}` output rewritten for
that subpath (`--base-path` defaults to `/Douri/`; pass a different value if the repo is
renamed or forked). Re-run it after any content or template change — `docs/` is a generated
snapshot, not something to hand-edit.

## Design system

The palette, type and motion are pulled directly from Douri's real brand (not placeholders):

- Blue `#0092D4` / `#29A1E2`, pale blue `#77B3FF`, ink `#222222`, white background
- `Montserrat Alternates` for headings, `Roboto` for body text
- A line-drawing sparrow — Douri's real logo mark — travels down a dashed vertical track
  fixed to the right edge of the page, tracking scroll position
  (`static/js/sparrow-flight.js` + `templates/partials/sparrow_flight.html`, included once
  from `base.html`)
- Grayscale-to-colour photography on hover, and a calm fade-and-rise reveal as sections
  scroll into view — no flashy animation, this is a documentary site about survivors of
  displacement and violence

All of it lives in `static/css/design-system.css`, one file, no build step.

## Going to production

- **Database**: set `DATABASE_URL` (e.g. `postgres://user:pass@host:5432/dbname`) and
  Postgres becomes a drop-in swap via `dj-database-url` — no code change.
- **Media storage**: local disk (`MEDIA_ROOT`/`MEDIA_URL`) works for dev; swap in
  `django-storages` (S3) or Cloudinary for production by changing `DEFAULT_FILE_STORAGE`
  and adding credentials — no model changes needed, since every image is a plain
  `ImageField`.
- **Instagram**: `InstagramPost` is a manual feed manager for v1 — staff paste the post URL
  and upload a screenshot, then toggle "Show in the homepage strip". A live feed (SnapWidget
  or Elfsight embed) is a fast future upgrade if the team wants automatic syncing — it's a
  config/embed swap, not new development.
- Run `python manage.py collectstatic` and put a real static-file server or CDN in front of
  `STATIC_ROOT` before deploying.

## Project layout

```
douri/
  manage.py
  requirements.txt
  core/         # home, about, volunteer, support-us, contact, site settings, form submissions
  projects/     # Project, Workshop models + views
  interviews/   # Interview model + views
  agenda/       # AgendaFeatured, AgendaRecurring models + views
  people/       # TeamMember, Partner models + views
  social/       # InstagramPost model
  static/
    css/design-system.css
    js/sparrow-flight.js
  templates/
```
