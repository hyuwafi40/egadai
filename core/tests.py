from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from collateral.models import Collateral
from collateral.utils.constants import CollateralStatusChoices
from account.utils.constants import JobChoices
from core.models.brand import Brand
from core.models.orgs import Orgs
from customer.models import Customer
from payment.models import Payment
from payment.utils.constants import PaymentMethodChoices, PaymentTypeChoices
from transaction.models import Transaction
from transaction.utils.constants import ContractStatusChoices
from vault.models import Category, Scheme, Storages


class DashboardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="dashboard-user",
            email="dashboard@example.com",
            password="test-password",
        )
        self.client.force_login(self.user)
        self.category = Category.objects.create(name="Elektronik", code="ELK")
        self.storage = Storages.objects.create(name="Gudang Utama", kode_gudang="GD001")
        self.scheme = Scheme.objects.create(
            name="Reguler",
            bunga=Decimal("1.00"),
            periode_bunga=30,
            durasi_maksimal_hari=30,
            denda_persen_perhari=Decimal("0.10"),
            biaya_admin=Decimal("5000.00"),
        )
        self.customer = Customer.objects.create(
            name="Nasabah Aktif",
            nik="1234567890123456",
        )

    def _create_transaction(self, name, customer, due_date):
        collateral = Collateral.objects.create(
            name=name,
            category=self.category,
            storages=self.storage,
            status=CollateralStatusChoices.STORED,
            appraisal_value=Decimal("500000.00"),
        )
        return Transaction.objects.create(
            collateral=collateral,
            storages=self.storage,
            customer=customer,
            scheme=self.scheme,
            tanggal_pinjam=timezone.localdate(),
            tanggal_jatuh_tempo=due_date,
            uang_pinjaman=Decimal("300000.00"),
            tujuan_pinjaman="Modal usaha",
            status_kontrak=ContractStatusChoices.AKTIF,
            created_by=self.user,
        )

    def test_dashboard_shows_operational_aggregates_and_due_alerts(self):
        today = timezone.localdate()
        inactive_customer = Customer.objects.create(
            name="Nasabah Nonaktif",
            nik="2234567890123456",
            is_active=False,
        )
        overdue = self._create_transaction(
            "Cincin Emas",
            self.customer,
            today - timezone.timedelta(days=1),
        )
        due_soon = self._create_transaction(
            "Laptop",
            inactive_customer,
            today + timezone.timedelta(days=3),
        )
        Payment.objects.create(
            transaction=overdue,
            tanggal_bayar=today,
            jumlah_bayar=Decimal("125000.00"),
            tipe_pembayaran=PaymentTypeChoices.CICILAN,
            metode_pembayaran=PaymentMethodChoices.CASH,
            created_by=self.user,
        )

        response = self.client.get("/core/")

        self.assertEqual(response.status_code, 200)
        dashboard = response.context["dashboard"]
        self.assertEqual(dashboard["customers"]["total"], 2)
        self.assertEqual(dashboard["customers"]["active"], 1)
        self.assertEqual(dashboard["collaterals"]["stored"], 2)
        self.assertEqual(dashboard["transactions"]["active"], 2)
        self.assertEqual(dashboard["transactions"]["overdue"], 1)
        self.assertEqual(dashboard["transactions"]["due_soon"], 1)
        self.assertEqual(dashboard["payments"]["count"], 1)
        self.assertEqual(dashboard["payments"]["total"], Decimal("125000.00"))
        self.assertEqual(list(dashboard["overdue_transactions"]), [overdue])
        self.assertEqual(list(dashboard["due_soon_transactions"]), [due_soon])
        self.assertIsNone(dashboard["storages"])

    def test_manager_sees_storage_summary(self):
        manager = get_user_model().objects.create_user(
            username="dashboard-manager",
            email="manager@example.com",
            password="test-password",
            job=JobChoices.ADMINISTRATOR,
        )
        Storages.objects.create(
            name="Gudang Penuh",
            kode_gudang="GD002",
            capacity=1,
            current_occupancy=1,
        )
        self.client.force_login(manager)

        response = self.client.get("/core/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["dashboard"]["storages"],
            {"active": 2, "full": 1},
        )


class SidebarNavigationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="sidebar-user",
            email="sidebar@example.com",
            password="test-password",
        )
        self.client.force_login(self.user)

    def test_sidebar_has_named_groups_and_current_page_state(self):
        response = self.client.get("/core/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-label="Navigasi utama"')
        self.assertContains(response, "Operasional")
        self.assertNotContains(response, "Data & Pengaturan")
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'aria-controls="sidebarNav"')
        self.assertNotContains(response, "Admin Panel")
        self.assertContains(response, 'action="/logout/"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')

    def test_manager_sees_management_menu(self):
        manager = get_user_model().objects.create_user(
            username="sidebar-manager",
            email="sidebar-manager@example.com",
            password="test-password",
            job=JobChoices.ADMINISTRATOR,
        )
        self.client.force_login(manager)

        response = self.client.get("/core/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Data &amp; Pengaturan")
        self.assertContains(response, "Pengguna")
        sidebar_labels = [
            item["label"]
            for group in response.context["sidebar_items"]
            for item in group["items"]
        ]
        self.assertIn("Organisasi", sidebar_labels)

    def test_logout_requires_post(self):
        response = self.client.get("/logout/")

        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.client.get("/core/").status_code, 200)

        response = self.client.post("/logout/")

        self.assertRedirects(response, "/")
        self.assertEqual(self.client.get("/core/").status_code, 302)


class LoginBrandInformationTests(TestCase):
    def test_organization_remains_primary_and_brand_is_developer_watermark(self):
        Orgs.objects.update_or_create(pk=1, defaults={"name": "Perusahaan Utama"})
        Brand.objects.update_or_create(
            pk=1,
            defaults={
                "name": "Project Watermark",
                "creator": "Developer Uji",
                "version": "2.4.0",
                "description": "Informasi project untuk halaman login.",
                "facebook": "https://facebook.com/example",
            },
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1 id="login-brand-name">Perusahaan Utama</h1>')
        self.assertContains(response, "PROJECT &amp; DEVELOPER")
        self.assertContains(response, "Project Watermark")
        self.assertContains(response, "Dikembangkan oleh Developer Uji")
        self.assertContains(response, "v2.4.0")
        self.assertContains(response, "Informasi project untuk halaman login.")
        self.assertContains(response, "https://facebook.com/example")

    def test_brand_name_is_not_used_as_company_identity_fallback(self):
        Orgs.objects.update_or_create(
            pk=1,
            defaults={"name": "", "legal_name": "", "brand_name": ""},
        )
        Brand.objects.update_or_create(
            pk=1,
            defaults={"name": "Project Watermark"},
        )

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        display_name = response.context["fallback_app_name"]
        self.assertContains(
            response,
            f'<h1 id="login-brand-name">{display_name}</h1>',
        )
        self.assertNotContains(
            response,
            '<h1 id="login-brand-name">Project Watermark</h1>',
        )
