from django.db import models

from transaction.utils.constants import ContractStatusChoices


class TransactionQuerySet(models.QuerySet):
    def aktif(self):
        return self.filter(status_kontrak=ContractStatusChoices.AKTIF)

    def lunas(self):
        return self.filter(status_kontrak=ContractStatusChoices.LUNAS)

    def jatuh_tempo(self):
        return self.filter(status_kontrak=ContractStatusChoices.JATUH_TEMPO)

    def lelang(self):
        return self.filter(status_kontrak=ContractStatusChoices.LELANG)


class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)

    def aktif(self):
        return self.get_queryset().aktif()

    def lunas(self):
        return self.get_queryset().lunas()

    def jatuh_tempo(self):
        return self.get_queryset().jatuh_tempo()

    def lelang(self):
        return self.get_queryset().lelang()
