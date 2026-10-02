from decimal import Decimal


def calculate_transaction_cost(uang_pinjaman, scheme):
    if not uang_pinjaman or not scheme:
        return {
            "bunga": Decimal("0"),
            "biaya_admin": Decimal("0"),
            "total_biaya": Decimal("0"),
            "total_tebus": Decimal("0"),
        }
    uang = Decimal(str(uang_pinjaman))
    bunga = (uang * scheme.bunga / Decimal("100")).quantize(Decimal("1"))
    biaya_admin = scheme.biaya_admin.quantize(Decimal("1"))
    total_biaya = bunga + biaya_admin
    total_tebus = uang + total_biaya
    return {
        "bunga": bunga,
        "biaya_admin": biaya_admin,
        "total_biaya": total_biaya,
        "total_tebus": total_tebus,
    }
