from django.db.models.signals import post_save
from django.dispatch import receiver

from collateral.models import Collateral
from collateral.utils.constants import CollateralStatusChoices
from payment.models import Payment
from payment.utils.constants import PaymentTypeChoices
from payment.utils.services import get_transaction_summary
from transaction.models import Transaction
from transaction.utils.constants import ContractStatusChoices


@receiver(post_save, sender=Payment)
def update_transaction_on_payment(sender, instance, created, **kwargs):
    if not created:
        return
    transaction = instance.transaction
    summary = get_transaction_summary(transaction)
    is_lunas_type = instance.tipe_pembayaran == PaymentTypeChoices.LUNAS
    if not summary["lunas"] and not is_lunas_type:
        return
    Transaction.objects.filter(pk=transaction.pk).update(
        status_kontrak=ContractStatusChoices.LUNAS
    )
    if transaction.collateral_id:
        Collateral.objects.filter(pk=transaction.collateral_id).update(
            status=CollateralStatusChoices.REDEEMED
        )
