"""
Enable Row Level Security (RLS) on all public tables and create policies
that only allow the postgres role full access.

This blocks Supabase anon/authenticated roles from accessing tables
directly via PostgREST while keeping Django's ORM access intact
(Django connects as postgres, which bypasses RLS, or uses the
service_role which also bypasses RLS).

Skips automatically on non-PostgreSQL backends (e.g. local SQLite).
"""

from django.db import migrations

# Every table visible in the Supabase Table Editor / Security Advisor
TABLES = [
    "account_emailaddress",
    "account_emailconfirmation",
    "accounts_category",
    "accounts_customuser",
    "accounts_customuser_groups",
    "accounts_customuser_user_permissions",
    "accounts_review",
    "accounts_userprofile",
    "accounts_userprofileimage",
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "business_business",
    "business_businesshours",
    "business_slot",
    "checkout_booking",
    "checkout_transaction",
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session",
    "django_site",
    "services_service",
    "socialaccount_socialaccount",
    "socialaccount_socialapp",
    "socialaccount_socialapp_sites",
    "socialaccount_socialtoken",
]


def enable_rls(apps, schema_editor):
    """Enable RLS and add a postgres-only policy on each table (PostgreSQL only)."""
    if schema_editor.connection.vendor != "postgresql":
        return
    cursor = schema_editor.connection.cursor()
    for table in TABLES:
        cursor.execute(
            f'ALTER TABLE public."{table}" ENABLE ROW LEVEL SECURITY;'
        )
        cursor.execute(
            f'CREATE POLICY "allow_postgres_full_access" ON public."{table}" '
            f"FOR ALL TO postgres USING (true) WITH CHECK (true);"
        )


def disable_rls(apps, schema_editor):
    """Drop the policies and disable RLS to revert (PostgreSQL only)."""
    if schema_editor.connection.vendor != "postgresql":
        return
    cursor = schema_editor.connection.cursor()
    for table in TABLES:
        cursor.execute(
            f'DROP POLICY IF EXISTS "allow_postgres_full_access" ON public."{table}";'
        )
        cursor.execute(
            f'ALTER TABLE public."{table}" DISABLE ROW LEVEL SECURITY;'
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0013_alter_review_service"),
    ]

    operations = [
        migrations.RunPython(enable_rls, reverse_code=disable_rls),
    ]

