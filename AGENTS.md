# AGENTS.md

## Project Snapshot
- Django monolith with app boundaries by domain: `accounts`, `services`, `business`, `checkout`, `home`, `information`.
- Root routing is in `booking_platform/urls.py`; each app exposes its own `urls.py` and templates.
- Core product loop: business owner defines hours -> slots are generated -> customer books service -> Stripe payment -> booking status updates.

## Architecture and Data Flow (Read These First)
- Auth uses custom user model `accounts.CustomUser` (`booking_platform/settings.py`, `accounts/models.py`). `is_business_owner` and `is_guest` drive behavior.
- `Business` is one-to-one with owner (`business/models.py`), and `Service` belongs to `Business` (`services/models.py`).
- Booking objects live in `checkout.Booking` and point to `Service` + customer (`checkout/models.py`).
- Availability is materialized as `business.Slot` rows generated from `BusinessHours` (`business/views.py`: `generate_slots_for_business`).
- Reviews are one-to-one with bookings (`accounts/models.py`), then ratings are recomputed in `accounts/views.py` (`update_service_rating`, `update_business_rating`).

## Booking + Payment Workflow Contracts
- Main booking entrypoint: `checkout/views.py::confirm_booking(service_id)`.
- Slot availability AJAX endpoint: `checkout/views.py::fetch_time_slots`; expects `date` and `service_id` query params.
- Stripe flow in this repo is session-based: create session -> redirect -> `payment_verification` -> `checkout_success`.
- Success handler marks booking `confirmed`, attempts to mark a matching `Slot.is_booked=True`, and sends email (`checkout/views.py`).
- Webhook endpoint `checkout/webhook/stripe/` also confirms booking by `payment_intent_id` (`stripe_webhook`). Keep both paths in sync when editing.

## Project-Specific Conventions
- Signup behavior depends on `?type=business` in `accounts/views.py::custom_signup_view` and `accounts/forms.py::CustomSignupForm`.
- Business-hours edits regenerate slots for roughly the next 30 days (`business/views.py`: add/edit flows).
- Service catalog URLs are nested under `/services/` from root plus app paths (example list route resolves via `services/urls.py` path `services/`).
- Messages framework + toast partials are the default UX feedback channel (`templates/base.html`, `templates/includes/toasts/*`).
- Category filtering is hierarchical/recursive (`services/views.py::get_services_by_category`) using `accounts.Category.parent`.

## Developer Workflow
- Local setup (from `README.md`): install deps, migrate, run server.
- Typical commands:
  - `python manage.py migrate`
  - `python manage.py runserver`
  - `python manage.py test`
- Deployment assumptions are Heroku-style (`Procfile`) with `collectstatic` + `gunicorn booking_platform.wsgi:application`.
- Static storage switches in tests (`booking_platform/settings.py`): tests use plain `StaticFilesStorage`, non-test uses WhiteNoise manifest storage.

## Integrations and Environment
- External services used directly in code: Stripe, Cloudinary, SMTP email, django-allauth.
- `booking_platform/settings.py` reads env via `python-dotenv`; optional `env.py` is imported if present.
- DB backend is `DATABASE_URL` when provided, otherwise local SQLite (`db.sqlite3`).
- Required env names are documented in `README.md` (`SECRET_KEY`, `DATABASE_URL`, `CLOUDINARY_URL`, Stripe keys, email creds, `DEVELOPMENT`).

## Practical Guardrails for Agents
- Preserve URL names and namespaces (`services:...`, `business:...`, `checkout:...`), many templates/tests use `reverse()` by name.
- When changing booking/payment code, validate both session redirect flow and webhook flow.
- When changing `BusinessHours`, update slot-generation behavior too; booking availability depends on materialized `Slot` rows.
- Keep custom-user assumptions intact (`AUTH_USER_MODEL = 'accounts.CustomUser'`), especially in migrations/tests.

