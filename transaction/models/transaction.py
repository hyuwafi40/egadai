from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from transaction.models.base import TimestampMixin
from transaction.utils.constants import (
    DEFAULT_STATUS,
    MAX_LENGTH_CONTRACT_NUMBER,
    MAX_LENGTH_STATUS,
    UANG_PINJAMAN_DECIMAL_PLACES,
    UANG_PINJAMAN_MAX_DIGITS,
    UANG_PINJAMAN_MIN_VALUE,
    ContractStatusChoices,
)
from transaction.utils.helpers import (
    generate_contract_number,
    normalize_contract_number,
    normalize_text,
)
from transaction.utils.managers import TransactionManager
from transaction.utils.validators import validate_contract_number


class Transaction(TimestampMixin):
    collateral = models.ForeignKey(
        "collateral.Collateral",
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Barang Jaminan",
    )
    storages = models.ForeignKey(
        "vault.Storages",
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Gudang",
    )
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Nasabah",
    )
    scheme = models.ForeignKey(
        "vault.Scheme",
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Skema",
    )
    tanggal_pinjam = models.DateField(
        db_index=True,
        verbose_name="Tanggal Pinjam",
    )
    tanggal_jatuh_tempo = models.DateField(
        db_index=True,
        verbose_name="Jatuh Tempo",
        help_text="Otomatis dihitung dari skema, bisa diubah manual.",
    )
    uang_pinjaman = models.DecimalField(
        max_digits=UANG_PINJAMAN_MAX_DIGITS,
        decimal_places=UANG_PINJAMAN_DECIMAL_PLACES,
        validators=[MinValueValidator(UANG_PINJAMAN_MIN_VALUE)],
        verbose_name="Uang Pinjaman",
    )
    tujuan_pinjaman = models.TextField(
        verbose_name="Tujuan Pinjam",
    )
    nomor_kontrak = models.CharField(
        max_length=MAX_LENGTH_CONTRACT_NUMBER,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        validators=[validate_contract_number],
        verbose_name="Nomor Kontrak",
        help_text="Kosongkan agar dibuat otomatis.",
    )
    status_kontrak = models.CharField(
        max_length=MAX_LENGTH_STATUS,
        choices=ContractStatusChoices.choices,
        default=DEFAULT_STATUS,
        db_index=True,
        verbose_name="Status Kontrak",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_transactions",
        verbose_name="Dibuat Oleh",
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = "Transaksi"
        verbose_name_plural = "Transaksi"
        ordering = ["-tanggal_pinjam", "-created_at"]

    def clean(self):
        super().clean()
        if (
            self.tanggal_pinjam
            and self.tanggal_jatuh_tempo
            and self.tanggal_jatuh_tempo <= self.tanggal_pinjam
        ):
            raise ValidationError(
                {
                    "tanggal_jatuh_tempo": (
                        "Jatuh tempo harus lebih besar dari tanggal pinjam."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.tujuan_pinjaman = normalize_text(self.tujuan_pinjaman)
        if not self.nomor_kontrak:
            self.nomor_kontrak = self._generate_unique_contract_number()
        else:
            self.nomor_kontrak = normalize_contract_number(self.nomor_kontrak)
        super().save(*args, **kwargs)

    def _generate_unique_contract_number(self):
        for _ in range(5):
            candidate = generate_contract_number()
            qs = type(self).objects.filter(nomor_kontrak=candidate)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if not qs.exists():
                return candidate
        raise ValidationError(
            {"nomor_kontrak": "Gagal membuat nomor kontrak. Coba lagi."}
        )

    @property
    def is_overdue(self):
        if self.status_kontrak != ContractStatusChoices.AKTIF:
            return False
        if not self.tanggal_jatuh_tempo:
            return False
        return self.tanggal_jatuh_tempo < timezone.localdate()

    def __str__(self):
        return f"{self.nomor_kontrak} - {self.customer.name}"
