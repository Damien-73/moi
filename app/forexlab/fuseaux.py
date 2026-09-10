"""Résolution des fuseaux horaires, compatible avec les Python plus anciens.

`zoneinfo` n'existe qu'à partir de Python 3.9. Sur un Mac un peu ancien, la
version installée peut être antérieure. Plutôt que d'échouer à l'import avec
un message incompréhensible, on essaie les solutions de repli et on explique
clairement quoi faire.
"""
from __future__ import annotations

try:
    from zoneinfo import ZoneInfo                      # Python 3.9+
except ImportError:                                    # pragma: no cover
    try:
        from backports.zoneinfo import ZoneInfo        # pip install backports.zoneinfo
    except ImportError:
        try:
            from pytz import timezone as _tz           # pip install pytz

            def ZoneInfo(nom):                          # noqa: N802
                return _tz(nom)
        except ImportError:
            raise ImportError(
                "Aucune bibliothèque de fuseaux horaires disponible.\n"
                "Python 3.9 ou plus la fournit d'origine (module zoneinfo).\n"
                "Sur une version antérieure, installe l'une des deux :\n"
                "    pip3 install backports.zoneinfo\n"
                "    pip3 install pytz\n"
                "Le fuseau est indispensable : la journée de négociation clôture "
                "à 17:00 heure de New York, et le changement d'heure doit être "
                "absorbé automatiquement."
            ) from None

__all__ = ["ZoneInfo"]
