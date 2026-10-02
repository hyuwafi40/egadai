from django.db import models

from payment.utils.constants import PaymentMethodChoices, PaymentTypeChoices


class PaymentQuerySet(models.QuerySet):
    def cicilan(self):
        return self.filter(tipe_pembayaran=PaymentTypeChoices.CICILAN)

    def lunas(self):
        return self.filter(tipe_pembayaran=PaymentTypeChoices.LUNAS)

    def cash(self):
        return self.filter(metode_pembayaran=PaymentMethodChoices.CASH)

    def transfer(self):
        return self.filter(metode_pembayaran=PaymentMethodChoices.TRANSFER)


class PaymentManager(models.Manager):
    def get_queryset(self):
        return PaymentQuerySet(self.model, using=self._db)

    def cicilan(self):
        return self.get_queryset().cicilan()

    def lunas(self):
        return self.get_queryset().lunas()

    def cash(self):
        return self.get_queryset().cash()

    def transfer(self):
        return self.get_queryset().transfer()
