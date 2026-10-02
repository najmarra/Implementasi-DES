Simulasi Komunikasi Dua Arah dengan Enkripsi DES

Simulasi transmisi ciphertext antara **Sender** dan **Receiver** menggunakan algoritma **DES (Data Encryption Standard)** yang diimplementasikan secara manual, tanpa library enkripsi.

> **Nama:** Najma Lail Arazy
> **NRP:** 5025241243
> **Mata Kuliah:** Keamanan Informasi B

---

## 1. Deskripsi

Program terdiri dari dua proses terpisah (Sender dan Receiver) yang terhubung lewat **TCP socket**. Setiap pesan dienkripsi dengan DES sebelum dikirim, dan hanya **ciphertext** yang melewati jaringan. Receiver mendekripsi pesan tersebut, dan bisa membalas dengan cara yang sama, sehingga komunikasinya **dua arah**.

### Ketentuan yang dipenuhi

| Ketentuan | Implementasi |
|---|---|
| Komunikasi dua arah | Dua pihak dapat saling kirim dan terima (thread terpisah untuk menerima) |
| Key sudah diketahui kedua pihak | Key diinput manual di kedua sisi, **tidak dikirim lewat jaringan** |
| Ada transmisi data nyata | Dua proses terpisah, terhubung via TCP socket (port 5000) |
| Enkripsi dan dekripsi DES manual | Ditulis sendiri di `des_simple.py`, tanpa library kriptografi |
| Bahasa pemrograman bebas | Python 3 |
| Capture Wireshark (opsional) | Lihat bagian 7 |

---

## 2. Cara Menjalankan

**Terminal 1 - Receiver (jalankan lebih dulu):**
```bash
python chat.py listen key
```

**Terminal 2 - Sender:**
```bash
python chat.py connect key 127.0.0.1
```

### Contoh output

Sender mengetik `tes receiver`:
```
Plaintext : tes receiver
Ciphertext: beff4212ba107d402b3efbf39f55abd23f0c33cdb347a670
```

Sisi lawan menerima:
```
Ciphertext: beff4212ba107d402b3efbf39f55abd23f0c33cdb347a670
Plaintext : Receiver: tes receiver
```

---

## 3. Alur Algoritma DES

DES memproses data per **blok 64 bit (8 byte)** dengan key 64 bit (efektif 56 bit), menggunakan struktur **Feistel 16 ronde**.

### 4.1 Pembuatan 16 Subkey (`make_subkeys`)
1. Key 64 bit dipermutasi dengan **PC-1** menjadi 56 bit.
2. Dibagi dua: C (28 bit) dan D (28 bit).
3. Tiap ronde: C dan D digeser kiri (1 atau 2 bit sesuai tabel `SHIFTS`), digabung, lalu dipermutasi dengan **PC-2** menjadi subkey 48 bit.

### 4.2 Enkripsi satu blok (`des_block`)
1. Blok 64 bit dipermutasi dengan **IP** (Initial Permutation), lalu dibagi menjadi L (32 bit) dan R (32 bit).
2. Ulangi **16 ronde**:
   ```
   L_baru = R_lama
   R_baru = L_lama XOR f(R_lama, subkey)
   ```
3. Gabungkan `R + L` (ditukar), lalu **FP** (Final Permutation) menghasilkan ciphertext.

### 4.3 Fungsi f (`f`)
1. **Ekspansi (E)**: R 32 bit menjadi 48 bit.
2. **XOR** dengan subkey 48 bit.
3. **S-Box**: 8 kelompok 6 bit diubah menjadi 4 bit (baris = bit pertama dan terakhir, kolom = 4 bit tengah).
4. **Permutasi P** pada hasil 32 bit.

### 4.4 Dekripsi
Proses **sama persis** dengan enkripsi, hanya **urutan 16 subkey dibalik** (`subkeys[::-1]`). Ini sifat khas jaringan Feistel.

### 4.5 Pemrosesan pesan panjang
Pesan dipotong menjadi blok 8 byte dan tiap blok diproses sendiri-sendiri (mode **ECB**), setelah diberi padding.

---

## 4. Padding

DES hanya dapat memproses blok **tepat 8 byte**, sehingga pesan perlu ditambah byte isian (skema **PKCS#7**):

- Jumlah byte yang kurang = `n`, lalu ditambahkan `n` byte yang masing-masing bernilai `n`.
- Jika panjang pesan sudah kelipatan 8, tetap ditambahkan 1 blok penuh (8 byte bernilai `08`) agar proses `unpad` tidak ambigu.

```python
def pad(data):
    n = 8 - len(data) % 8
    return data + bytes([n]) * n

def unpad(data):
    n = data[-1]
    if n < 1 or n > 8:
        raise ValueError("key salah / data rusak")
    return data[:-n]
```
---

## 5. Kesimpulan

Algoritma DES berhasil diimplementasikan secara manual dan diverifikasi dengan test vector resmi (key `133457799BBCDFF1`, plaintext `0123456789ABCDEF`, ciphertext `85E813540F0AB405`). Simulasi komunikasi dua arah antara Sender dan Receiver berjalan dengan benar: data yang melewati jaringan hanya berupa ciphertext, dan pesan hanya dapat dibaca kembali oleh pihak yang memiliki key yang sama.

---

- Dokumentasi Python: modul `socket` dan `threading`.

_Catatan: kode dibuat dengan bantuan AI (Claude), kemudian dipelajari dan diuji oleh penulis._
