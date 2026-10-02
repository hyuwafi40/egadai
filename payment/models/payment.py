from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from payment.models.base import TimestampMixin
from payment.utils.constants import (
    DEFAULT_PAYMENT_METHOD,
    DEFAULT_PAYMENT_TYPE,
    JUMLAH_BAYAR_DECIMAL_PLACES,
    JUMLAH_BAYAR_MAX_DIGITS,
    JUMLAH_BAYAR_MIN_VALUE,
    MAX_LENGTH_CHOICE,
    MAX_LENGTH_PAYMENT_NUMBER,
    PaymentMethodChoices,
    PaymentTypeChoices,
)
from payment.utils.helpers import (
    generate_payment_number,
    normalize_payment_number,
    normalize_text,
)
from payment.utils.managers import PaymentManager
from payment.utils.validators import validate_payment_number


class Payment(TimestampMixin):
    transaction = models.ForeignKey(
        "transaction.Transaction",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="Transaksi",
    )
    nomor_pembayaran = models.CharField(
        max_length=MAX_LENGTH_PAYMENT_NUMBER,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        validators=[validate_payment_number],
        verbose_name="Nomor Pembayaran",
        help_text="Kosongkan agar dibuat otomatis.",
    )
    tanggal_bayar = models.DateField(
        db_index=True,
        verbose_name="Tanggal Bayar",
    )
    jumlah_bayar = models.DecimalField(
        max_digits=JUMLAH_BAYAR_MAX_DIGITS,
        decimal_places=JUMLAH_BAYAR_DECIMAL_PLACES,
        validators=[MinValueValidator(JUMLAH_BAYAR_MIN_VALUE)],
        verbose_name="Jumlah Bayar",
    )
    tipe_pembayaran = models.CharField(
        max_length=MAX_LENGTH_CHOICE,
        choices=PaymentTypeChoices.choices,
        default=DEFAULT_PAYMENT_TYPE,
        db_index=True,
        verbose_name="Tipe Pembayaran",
    )
    metode_pembayaran = models.CharField(
        max_length=MAX_LENGTH_CHOICE,
        choices=PaymentMethodChoices.choices,
        default=DEFAULT_PAYMENT_METHOD,
        db_index=True,
        verbose_name="Metode Pembayaran",
    )
    catatan = models.TextField(
        blank=True,
        verbose_name="Catatan",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_payments",
        verbose_name="Dibuat Oleh",
    )

    objects = PaymentManager()

    class Meta:
        verbose_name = "Pembayaran"
        verbose_name_plural = "Pembayaran"
        ordering = ["-tanggal_bayar", "-created_at"]

    def save(self, *args, **kwargs):
        self.catatan = normalize_text(self.catatan)
        if not self.nomor_pembayaran:
            self.nomor_pembayaran = self._generate_unique_payment_number()
        else:
            self.nomor_pembayaran = normalize_payment_number(self.nomor_pembayaran)
        super().save(*args, **kwargs)

    def _generate_unique_payment_number(self):
        for _ in range(5):
            candidate = generate_payment_number()
            qs = type(self).objects.filter(nomor_pembayaran=candidate)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if not qs.exists():
                return candidate
        raise ValidationError(
            {"nomor_pembayaran": "Gagal membuat nomor pembayaran. Coba lagi."}
        )

    def __str__(self):
        return f"{self.nomor_pembayaran} - {self.transaction.nomor_kontrak}"
