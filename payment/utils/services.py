from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction as db_transaction

from payment.models import Payment
from payment.utils.constants import PaymentTypeChoices
from transaction.models.transaction import Transaction
from transaction.utils.constants import ContractStatusChoices
from transaction.utils.services import calculate_transaction_cost


def get_transaction_summary(transaction):
    cost = calculate_transaction_cost(transaction.uang_pinjaman, transaction.scheme)
    total_tebus = cost["total_tebus"]
    agg = Payment.objects.filter(transaction=transaction).aggregate(
        total=models.Sum("jumlah_bayar")
    )
    total_dibayar = agg.get("total") or Decimal("0")
    sisa_bayar = total_tebus - total_dibayar
    if sisa_bayar < 0:
        sisa_bayar = Decimal("0")
    return {
        "total_tebus": total_tebus,
        "total_dibayar": total_dibayar,
        "sisa_bayar": sisa_bayar,
        "lunas": sisa_bayar <= 0,
    }


def get_transactions_summary_batch(transactions):
    trx_list = list(transactions)
    if not trx_list:
        return {}
    trx_ids = [t.pk for t in trx_list]
    totals = (
        Payment.objects.filter(transaction_id__in=trx_ids)
        .values("transaction_id")
        .annotate(total=models.Sum("jumlah_bayar"))
    )
    totals_map = {row["transaction_id"]: row["total"] for row in totals}
    results = {}
    for trx in trx_list:
        cost = calculate_transaction_cost(trx.uang_pinjaman, trx.scheme)
        total_tebus = cost["total_tebus"]
        total_dibayar = totals_map.get(trx.pk) or Decimal("0")
        sisa_bayar = total_tebus - total_dibayar
        if sisa_bayar < 0:
            sisa_bayar = Decimal("0")
        results[trx.pk] = {
            "total_tebus": total_tebus,
            "total_dibayar": total_dibayar,
            "sisa_bayar": sisa_bayar,
            "lunas": sisa_bayar <= 0,
        }
    return results


def validate_payment_amount(transaction, jumlah_bayar, tipe_pembayaran):
    if transaction.status_kontrak == ContractStatusChoices.LUNAS:
        raise ValidationError("Transaksi ini sudah lunas.")
    summary = get_transaction_summary(transaction)
    if summary["lunas"]:
        raise ValidationError("Transaksi ini sudah lunas.")
    if tipe_pembayaran == PaymentTypeChoices.LUNAS:
        return
    if jumlah_bayar is None or jumlah_bayar <= 0:
        raise ValidationError("Jumlah bayar harus lebih besar dari 0.")
    if jumlah_bayar > summary["sisa_bayar"]:
        raise ValidationError(
            f"Jumlah bayar melebihi sisa. Sisa: Rp {summary['sisa_bayar']}."
        )


def apply_payment(
    transaction,
    jumlah_bayar,
    tipe_pembayaran,
    metode_pembayaran,
    tanggal_bayar,
    created_by,
    catatan="",
    nomor_pembayaran=None,
):
    with db_transaction.atomic():
        locked = Transaction.objects.select_for_update().get(pk=transaction.pk)
        summary = get_transaction_summary(locked)
        if tipe_pembayaran == PaymentTypeChoices.LUNAS:
            jumlah_bayar = summary["sisa_bayar"]
        validate_payment_amount(locked, jumlah_bayar, tipe_pembayaran)
        payment = Payment.objects.create(
            transaction=locked,
            jumlah_bayar=jumlah_bayar,
            tipe_pembayaran=tipe_pembayaran,
            metode_pembayaran=metode_pembayaran,
            tanggal_bayar=tanggal_bayar,
            catatan=catatan,
            created_by=created_by,
            nomor_pembayaran=nomor_pembayaran,
        )
        return payment
