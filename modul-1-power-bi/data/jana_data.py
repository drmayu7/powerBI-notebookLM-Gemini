"""Jana dataset statistik perubatan sintetik untuk Modul 1 (Power BI).

Data ini SEPENUHNYA SINTETIK (rekaan) - tiada kaitan dengan pesakit sebenar.
Boleh dihasilkan semula kerana random.seed ditetapkan.

Guna:
    python jana_data.py

Hasil (dalam folder yang sama):
    disiplin.csv, wad.csv, tarikh.csv, kemasukan.csv
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(20260625)
OUT = Path(__file__).parent
TARIKH_MULA = date(2025, 1, 1)
TARIKH_TAMAT = date(2025, 12, 31)
N_KEMASUKAN = 3000

# Dimensi disiplin (kod, nama)
DISIPLIN = [
    ("DIS01", "Perubatan"),
    ("DIS02", "Pembedahan"),
    ("DIS03", "O&G"),
    ("DIS04", "Pediatrik"),
    ("DIS05", "Ortopedik"),
    ("DIS06", "Kardiologi"),
]

# Dimensi wad (kod, nama, kapasiti katil, jenis)
WAD = [
    ("W01", "Wad Perubatan Lelaki", 30, "Umum"),
    ("W02", "Wad Perubatan Wanita", 30, "Umum"),
    ("W03", "Wad Pembedahan", 28, "Umum"),
    ("W04", "Wad O&G", 24, "Khusus"),
    ("W05", "Wad Pediatrik", 20, "Khusus"),
    ("W06", "Wad Ortopedik", 26, "Umum"),
    ("W07", "Unit Rawatan Rapi (ICU)", 10, "Kritikal"),
]

# Diagnosis / DRG ringkas (sintetik)
DRG = [
    "A01-Jangkitan",
    "C50-Barah",
    "I20-Jantung",
    "J18-Pneumonia",
    "K35-Apendisitis",
    "O80-Bersalin",
    "S72-Patah Tulang",
    "E11-Diabetes",
]

NAMA_BULAN = ["Jan", "Feb", "Mac", "Apr", "Mei", "Jun",
              "Jul", "Ogos", "Sep", "Okt", "Nov", "Dis"]


def jana_tarikh():
    """Satu baris bagi setiap hari dalam julat data."""
    rows = []
    d = TARIKH_MULA
    while d <= TARIKH_TAMAT:
        rows.append([d.isoformat(), d.year, d.month, NAMA_BULAN[d.month - 1]])
        d += timedelta(days=1)
    return rows


def jana_kemasukan():
    """Jadual fakta kemasukan pesakit."""
    rows = []
    rentang = (TARIKH_TAMAT - TARIKH_MULA).days
    for i in range(1, N_KEMASUKAN + 1):
        masuk = TARIKH_MULA + timedelta(days=random.randint(0, rentang))
        # Tempoh tinggal (LOS) - taburan lognormal supaya majoriti pendek,
        # sebahagian kecil panjang (realistik).
        los = max(1, int(random.lognormvariate(1.1, 0.6)))
        discaj = masuk + timedelta(days=los)
        if discaj > TARIKH_TAMAT:
            discaj = TARIKH_TAMAT
        wad = random.choice(WAD)[0]
        dis = random.choice(DISIPLIN)[0]
        rows.append([
            f"K{i:05d}",
            masuk.isoformat(),
            discaj.isoformat(),
            wad,
            dis,
            random.choice(DRG),
            random.randint(0, 95),
            random.choice(["L", "P"]),
        ])
    return rows


def tulis(nama, header, rows):
    with open(OUT / nama, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


if __name__ == "__main__":
    tulis("disiplin.csv", ["Kod_Disiplin", "Nama_Disiplin"], DISIPLIN)
    tulis("wad.csv",
          ["Kod_Wad", "Nama_Wad", "Kapasiti_Katil", "Jenis_Wad"], WAD)
    tulis("tarikh.csv",
          ["Tarikh", "Tahun", "Bulan", "Nama_Bulan"], jana_tarikh())
    tulis("kemasukan.csv",
          ["ID_Kemasukan", "Tarikh_Masuk", "Tarikh_Discaj", "Kod_Wad",
           "Kod_Disiplin", "Diagnosis_DRG", "Umur", "Jantina"],
          jana_kemasukan())
    print("Siap: kemasukan.csv, wad.csv, disiplin.csv, tarikh.csv")
