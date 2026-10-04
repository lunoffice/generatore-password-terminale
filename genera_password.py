#!/usr/bin/env python3
"""
genera_password.py — ai riparo (Alex Lunalbi)
Generatore di password da terminale con CSPRNG (`secrets`), garanzia di
almeno un carattere per set attivo, esclusione opzionale dei caratteri
ambigui e stima dell'entropia teorica in bit.

Allineato alla logica del tool online /tools/generatore-password/.
Solo libreria standard. Nessuna rete, nessuna scrittura su disco.
"""

from __future__ import annotations

import argparse
import math
import secrets
import sys

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
AMBIGUOUS = set("0Oo1lI|`")

MIN_LEN = 8
MAX_LEN = 128
DEFAULT_LEN = 20


def filter_ambiguous(charset: str, exclude: bool) -> str:
    if not exclude:
        return charset
    return "".join(c for c in charset if c not in AMBIGUOUS)


def build_charset(
    *,
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
) -> tuple[str, list[str]]:
    buckets: list[str] = []

    def add(charset: str) -> None:
        filtered = filter_ambiguous(charset, exclude_ambiguous)
        if filtered:
            buckets.append(filtered)

    if use_lower:
        add(LOWER)
    if use_upper:
        add(UPPER)
    if use_digits:
        add(DIGITS)
    if use_symbols:
        add(SYMBOLS)

    # Pool unico (come nel tool web)
    pool = "".join(dict.fromkeys("".join(buckets)))
    return pool, buckets


def strength_label(bits: float) -> str:
    if bits < 40:
        return "Debole"
    if bits < 60:
        return "Discreta"
    if bits < 80:
        return "Buona"
    return "Molto forte"


def generate_password(
    length: int,
    *,
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
) -> tuple[str, float, int]:
    pool, buckets = build_charset(
        use_lower=use_lower,
        use_upper=use_upper,
        use_digits=use_digits,
        use_symbols=use_symbols,
        exclude_ambiguous=exclude_ambiguous,
    )

    if not pool or not buckets:
        raise ValueError("Devi selezionare almeno un set di caratteri.")

    if length < len(buckets):
        raise ValueError(
            f"Con questi set servono almeno {len(buckets)} caratteri."
        )

    chars: list[str] = []
    for bucket in buckets:
        chars.append(secrets.choice(bucket))
    for _ in range(length - len(buckets)):
        chars.append(secrets.choice(pool))

    # Fisher–Yates con CSPRNG
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    bits = length * math.log2(len(pool))
    return "".join(chars), bits, len(pool)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generatore di password sicure da terminale (ai riparo)"
    )
    parser.add_argument(
        "-n",
        "--length",
        type=int,
        default=DEFAULT_LEN,
        help=f"Lunghezza ({MIN_LEN}-{MAX_LEN}, default: {DEFAULT_LEN})",
    )
    parser.add_argument("--no-lower", action="store_true", help="Escludi minuscole")
    parser.add_argument("--no-upper", action="store_true", help="Escludi maiuscole")
    parser.add_argument("--no-digits", action="store_true", help="Escludi numeri")
    parser.add_argument("--no-symbols", action="store_true", help="Escludi simboli")
    parser.add_argument(
        "--no-ambiguous",
        action="store_true",
        help="Escludi caratteri ambigui (0, O, o, 1, l, I, |, `)",
    )
    args = parser.parse_args()

    if args.length < MIN_LEN or args.length > MAX_LEN:
        sys.exit(
            f"Errore: la lunghezza deve essere compresa tra {MIN_LEN} e {MAX_LEN}."
        )

    try:
        password, bits, alphabet_size = generate_password(
            args.length,
            use_lower=not args.no_lower,
            use_upper=not args.no_upper,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
            exclude_ambiguous=args.no_ambiguous,
        )
    except ValueError as exc:
        sys.exit(f"Errore: {exc}")

    label = strength_label(bits)
    print()
    print(f"Password : {password}")
    print(f"Lunghezza: {args.length} caratteri")
    print(f"Alfabeto : {alphabet_size} caratteri disponibili")
    print(f"Entropia : ~{int(bits)} bit ({label})")
    print()


if __name__ == "__main__":
    main()
