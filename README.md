# Generatore di password sicure da terminale

Script Python **offline** che genera password casuali con CSPRNG (`secrets`), garanzia di almeno un carattere per ogni set attivo, esclusione opzionale dei caratteri ambigui e stima dell’entropia teorica in bit.

Allineato al [tool online di ai riparo](https://airiparo.it/tools/generatore-password/) e alla guida:

**[Generatore di password sicure da terminale](https://airiparo.it/python/script-python-generatore-password-terminale/)**

## Caratteristiche

- Solo libreria standard Python (`secrets`, `argparse`, `math`)
- Nessuna rete, nessuna scrittura su disco, nessuna telemetria
- Lunghezza configurabile (8–128, default 20)
- Flag per escludere minuscole, maiuscole, numeri, simboli
- Flag `--no-ambiguous` per evitare `0 O o 1 l I | \``
- Stima entropia con etichette: Debole / Discreta / Buona / Molto forte
- Licenza **MIT**

## Requisiti

- Python **3.9+** (testato con Python 3.12)
- Windows, macOS o Linux

## Installazione

### Opzione 1 — Clona il repository

```bash
git clone https://github.com/lunoffice/generatore-password-terminale.git
cd generatore-password-terminale
```

### Opzione 2 — Scarica solo lo script

Dalla [release/pagina del repo](https://github.com/lunoffice/generatore-password-terminale) usa **Code → Download ZIP**, oppure scarica `genera_password.py` dal sito:

[Download verificato su ai riparo](https://airiparo.it/python/script-python-generatore-password-terminale/)

## Uso

### Windows (PowerShell o cmd)

```bash
python genera_password.py
```

### macOS / Linux

```bash
python3 genera_password.py
```

### Esempio di output

```text
Password : <stringa casuale>
Lunghezza: 20 caratteri
Alfabeto : 91 caratteri disponibili
Entropia : ~130 bit (Molto forte)
```

## Opzioni della CLI

| Flag | Effetto | Default |
| --- | --- | --- |
| `-n` / `--length` | Lunghezza password (8–128) | `20` |
| `--no-lower` | Esclude minuscole | off |
| `--no-upper` | Esclude maiuscole | off |
| `--no-digits` | Esclude numeri | off |
| `--no-symbols` | Esclude simboli | off |
| `--no-ambiguous` | Esclude caratteri ambigui | off |
| `-h` / `--help` | Aiuto nativo | — |

### Combinazioni tipiche

Password lunga “da vault”:

```bash
python genera_password.py -n 24
```

```bash
python3 genera_password.py -n 24
```

Senza simboli (alcuni form lo vietano):

```bash
python genera_password.py --no-symbols
```

```bash
python3 genera_password.py --no-symbols
```

Facile da dettare / digitare (niente ambigui):

```bash
python genera_password.py --no-ambiguous -n 20
```

```bash
python3 genera_password.py --no-ambiguous -n 20
```

Solo alfanumerico, 16 caratteri:

```bash
python genera_password.py -n 16 --no-symbols
```

```bash
python3 genera_password.py -n 16 --no-symbols
```

## Verifica integrità (SHA-256)

Checksum del file `genera_password.py` (versione 1.0.0 pubblicata con l’articolo):

```text
dae5a1ab8681d7abe12e868bb774da431d25101e7d095ee542b74096a9715c79
```

Guida opzionale: [Verificare un download con SHA-256](https://airiparo.it/python/verificare-sha256-download/).

## Sicurezza (in breve)

- Usa `secrets` (CSPRNG), non `random`
- Garantisce almeno un carattere per ogni set attivo, poi mescola con Fisher–Yates basato su `secrets`
- L’entropia stampata è **teorica** sul pool di caratteri: non è un audit del tuo account
- Dopo aver generato una password, salvala in un password manager e evita di lasciarla nello scrollback del terminale

## Licenza

[MIT](LICENSE) — Copyright (c) 2026 Alex Lunalbi (ai riparo)

## Autore

- Alex Lunalbi — [ai riparo](https://airiparo.it/)
- GitHub: [lunoffice](https://github.com/lunoffice)
