from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, F, Q, Sum
from django.utils import timezone

from collateral.models import Collateral
from collateral.utils.constants import CollateralStatusChoices
from config.shared.access import user_is_manager
from core.views.base import BaseAuthView
from customer.models import Customer
from payment.models import Payment
from transaction.models import Transaction
from transaction.utils.constants import ContractStatusChoices
from vault.models import Storages


class IndexViews(BaseAuthView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        due_cutoff = today + timedelta(days=7)

        customer_stats = Customer.objects.aggregate(
            total=Count("pk"),
            active=Count("pk", filter=Q(is_active=True)),
        )
        collateral_stats = Collateral.objects.aggregate(
            stored=Count(
                "pk",
                filter=Q(is_active=True, status=CollateralStatusChoices.STORED),
            ),
            redeemed=Count(
                "pk",
                filter=Q(is_active=True, status=CollateralStatusChoices.REDEEMED),
            ),
            auctioned=Count(
                "pk",
                filter=Q(is_active=True, status=CollateralStatusChoices.AUCTIONED),
            ),
            stored_appraisal=Sum(
                "appraisal_value",
                filter=Q(is_active=True, status=CollateralStatusChoices.STORED),
            ),
        )
        transaction_stats = Transaction.objects.aggregate(
            active=Count(
                "pk",
                filter=Q(status_kontrak=ContractStatusChoices.AKTIF),
            ),
            overdue=Count(
                "pk",
                filter=Q(
                    status_kontrak__in=(
                        ContractStatusChoices.AKTIF,
                        ContractStatusChoices.JATUH_TEMPO,
                    ),
                    tanggal_jatuh_tempo__lt=today,
                ),
            ),
            due_soon=Count(
                "pk",
                filter=Q(
                    status_kontrak=ContractStatusChoices.AKTIF,
                    tanggal_jatuh_tempo__gte=today,
                    tanggal_jatuh_tempo__lte=due_cutoff,
                ),
            ),
            paid=Count(
                "pk",
                filter=Q(status_kontrak=ContractStatusChoices.LUNAS),
            ),
            auctioned=Count(
                "pk",
                filter=Q(status_kontrak=ContractStatusChoices.LELANG),
            ),
        )
        month_payments = Payment.objects.filter(
            tanggal_bayar__gte=today.replace(day=1),
            tanggal_bayar__lte=today,
        ).aggregate(count=Count("pk"), total=Sum("jumlah_bayar"))

        overdue_transactions = (
            Transaction.objects.filter(
                status_kontrak__in=(
                    ContractStatusChoices.AKTIF,
                    ContractStatusChoices.JATUH_TEMPO,
                ),
                tanggal_jatuh_tempo__lt=today,
            )
            .select_related("customer")
            .order_by("tanggal_jatuh_tempo")[:5]
        )
        due_soon_transactions = (
            Transaction.objects.filter(
                status_kontrak=ContractStatusChoices.AKTIF,
                tanggal_jatuh_tempo__gte=today,
                tanggal_jatuh_tempo__lte=due_cutoff,
            )
            .select_related("customer")
            .order_by("tanggal_jatuh_tempo")[:5]
        )

        storage_stats = None
        if user_is_manager(self.request.user):
            storage_stats = Storages.objects.aggregate(
                active=Count("pk", filter=Q(is_active=True)),
                full=Count(
                    "pk",
                    filter=Q(
                        is_active=True,
                        capacity__gt=0,
                        current_occupancy__gte=F("capacity"),
                    ),
                ),
            )

        context["dashboard"] = {
            "today": today,
            "customers": customer_stats,
            "collaterals": collateral_stats,
            "transactions": transaction_stats,
            "payments": {
                "count": month_payments["count"],
                "total": month_payments["total"] or Decimal("0"),
            },
            "overdue_transactions": overdue_transactions,
            "due_soon_transactions": due_soon_transactions,
            "storages": storage_stats,
        }
        return context
