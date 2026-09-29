from django.contrib import admin
from solo.admin import SingletonModelAdmin

from core.models import Brand, Orgs


@admin.register(Brand)
class BrandAdmin(SingletonModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Identitas",
            {
                "fields": (
                    "name",
                    "description",
                    "version",
                    "creator",
                )
            },
        ),
        (
            "Sosial",
            {
                "fields": (
                    "facebook",
                    "instagram",
                    "tiktok",
                    "youtube",
                )
            },
        ),
        (
            "Logo",
            {"fields": ("logo",)},
        ),
        (
            "Timestamp",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Orgs)
class OrgsAdmin(SingletonModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Identitas",
            {
                "fields": (
                    "name",
                    "owner",
                    "legal_name",
                    "brand_name",
                    "company_status",
                    "company_type",
                    "description",
                    "tagline",
                    "logo",
                )
            },
        ),
        (
            "Legalitas",
            {
                "fields": (
                    "npwp",
                    "license_number",
                    "license_date",
                    "deed_number",
                    "deed_date",
                    "last_amendment_number",
                    "last_amendment_date",
                    "founded_date",
                    "founded_place",
                    "business_sector",
                )
            },
        ),
        (
            "Permodalan & Wilayah",
            {
                "fields": (
                    "authorized_capital",
                    "paid_up_capital",
                    "business_scope",
                )
            },
        ),
        (
            "Alamat & Kontak",
            {
                "fields": (
                    "address",
                    "city",
                    "province",
                    "postal_code",
                    "country",
                    "phone",
                    "fax",
                    "email",
                    "website",
                )
            },
        ),
        (
            "Bisnis & Operasional",
            {
                "fields": (
                    "business_type",
                    "products_services",
                    "total_branches",
                    "total_employees",
                    "psp_name",
                    "psp_type",
                )
            },
        ),
        (
            "Visi & Misi",
            {
                "fields": ("vision", "mission"),
                "classes": ("collapse",),
            },
        ),
        (
            "Geografis",
            {
                "fields": ("latitude", "longitude"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamp",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
