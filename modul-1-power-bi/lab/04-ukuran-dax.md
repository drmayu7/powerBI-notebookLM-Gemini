# Lab 4: Ukuran (Measure) DAX

**Matlamat:** Cipta ukuran statistik perubatan menggunakan **DAX**
(*Data Analysis Expressions*).

> **Measure** ialah pengiraan yang dinilai semula secara automatik mengikut
> penapis semasa. Kita akan cipta tujuh measure (lima utama + dua bantuan untuk
> BOR).

**Cara cipta measure:** Klik jadual `kemasukan` di panel **Fields** →
tab **Home** → **New measure** → taip/tampal formula → tekan **Enter**.

---

## Measure utama

### 1. Jumlah Kemasukan
Bilangan episod kemasukan.
```DAX
Jumlah Kemasukan = COUNTROWS('kemasukan')
```

### 2. Jumlah Discaj
Bilangan kemasukan yang sudah ada tarikh discaj.
```DAX
Jumlah Discaj = CALCULATE(COUNTROWS('kemasukan'), NOT(ISBLANK('kemasukan'[Tarikh_Discaj])))
```

### 3. ALOS (Average Length of Stay)
Purata tempoh tinggal (hari).
```DAX
ALOS = AVERAGE('kemasukan'[Tempoh_Tinggal])
```

### 4. Bilangan Pesakit ikut Wad
Bilangan episod unik (dipaparkan mengikut `Nama_Wad` pada visual di Lab 5).
```DAX
Bilangan Pesakit ikut Wad = DISTINCTCOUNT('kemasukan'[ID_Kemasukan])
```

---

## Measure bantuan (untuk BOR %)

BOR (*Bed Occupancy Rate*) = jumlah hari pesakit ÷ jumlah hari katil tersedia.
Kita pecahkan kepada dua measure bantuan dahulu.

### 5. Jumlah Hari Pesakit
Jumlah semua tempoh tinggal.
```DAX
Jumlah Hari Pesakit = SUMX('kemasukan', 'kemasukan'[Tempoh_Tinggal])
```

### 6. Jumlah Hari Katil Tersedia
Jumlah katil (semua wad) × bilangan hari dalam tempoh ditapis.
```DAX
Jumlah Hari Katil Tersedia = SUMX('wad', 'wad'[Kapasiti_Katil]) * DISTINCTCOUNT('tarikh'[Tarikh])
```

### 7. BOR %
Peratus penggunaan katil.
```DAX
BOR % = DIVIDE([Jumlah Hari Pesakit], [Jumlah Hari Katil Tersedia]) * 100
```

> **Nota:** `DIVIDE` digunakan supaya tiada ralat jika penyebut sifar.

---

## Hasil yang dijangka

Tujuh measure muncul di panel **Fields** (ikon kalkulator) di bawah jadual
`kemasukan`. Anda boleh seret mana-mana measure ke kanvas untuk menguji
nilainya.

➡️ Seterusnya: [Lab 5 — Visual asas](05-visual-asas.md)
