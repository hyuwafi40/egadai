from core.models import Brand, Orgs
from core.utils.constants import SINGLETON_AUTO_FIELDS


def get_brand():
    return Brand.objects.get_current()


def get_orgs():
    return Orgs.objects.get_current()


def _validate_fields(model, data):
    excluded = set(SINGLETON_AUTO_FIELDS)
    valid = {field.name for field in model._meta.fields} - excluded
    invalid = set(data) - valid
    if invalid:
        names = ", ".join(sorted(invalid))
        raise ValueError(f"Field tidak valid: {names}")


def _apply_and_save(instance, model, data):
    _validate_fields(model, data)
    for field, value in data.items():
        setattr(instance, field, value)
    instance.full_clean(exclude=list(SINGLETON_AUTO_FIELDS))
    instance.save()
    return instance


def update_brand(**kwargs):
    brand, _ = Brand.objects.get_or_create(pk=1)
    return _apply_and_save(brand, Brand, kwargs)


def update_orgs(**kwargs):
    orgs, _ = Orgs.objects.get_or_create(pk=1)
    return _apply_and_save(orgs, Orgs, kwargs)
