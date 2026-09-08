# FCB — FAA Clipboard Copas

Copy-paste dua arah antara PC (Windows) dan HP (Android) via ADB. Tanpa aplikasi tambahan di HP, tetap pakai GBoard.

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey) ![ADB](https://img.shields.io/badge/adb-required-green)

## Fitur

- **Tab PTH (PC → HP)** — ketik otomatis teks dari PC ke kolom aktif di HP (`adb shell input`)
  - Kutip `"`, `'` terkirim utuh (POSIX shell escaping)
  - Teks panjang auto-split 400 char, support multi-baris + Enter
  - Emoji / kutip lengkung / karakter aneh otomatis disanitasi + dilaporkan di log
  - Teks ber-emoji otomatis via APK helper (kalau terinstall, lihat bawah):
    clipboard HP + tombol PASTE, unicode 100% utuh, GBoard tetap
  - Retry 3x untuk gagal sesaat + klasifikasi error yang jujur (`security` / `connection` / `badchar` / `other`)
- **Tab HTP (HP → PC)** — baca clipboard HP via `service call clipboard 4` (`getPrimaryClip`)
  - Hasil otomatis masuk clipboard PC, tinggal `Ctrl+V`
  - Mode auto-monitor (polling tiap 2 detik)
- **Tab Manual** — panduan + troubleshooting di dalam aplikasi
- Tanpa kedip console (`CREATE_NO_WINDOW`, jalan via `pythonw`)

## Syarat

1. Python 3.8+ (sudah termasuk `tkinter`)
2. Android SDK Platform-Tools (`adb.exe`) **wajib ada di PATH environment** — cek: `adb --version`

> **Note — cara masukin ADB ke PATH (Windows):**
> 1. Download *SDK Platform-Tools* dari situs resmi Android developer, extract misal ke `C:\platform-tools` (pastikan ada `adb.exe` di dalamnya).
> 2. Start → ketik *Environment Variables* → *Edit the system environment variables* → **Environment Variables** → di *System variables* pilih **Path** → **Edit** → **New** → isi `C:\platform-tools` → OK.
> 3. Buka terminal **baru**, cek `adb --version`. Kalau masih *"not recognized"*, berarti terminalnya belum dibuka ulang atau path-nya salah ketik.
3. HP: USB Debugging ON, colok USB, tap **Allow** di popup HP — cek: `adb devices`
4. **Xiaomi/Redmi WAJIB**: di *Settings > Additional settings > Developer options* aktifkan **DUA** toggle:
   - `USB debugging`
   - `USB debugging (Security settings)` ← yang ini sering kelupaan!
   
   lalu **reboot HP**. Catatan: toggle Security suka OFF sendiri habis reboot / update / cabut SIM (butuh SIM + akun Mi biar nempel).

## Cara pakai

```bat
python fcc.py
```

Atau tanpa jendela console (Windows): tinggal **double-click `fcb.vbs`** —
file launcher yang sudah disertakan di folder ini.

### Cara edit `fcb.vbs`

Klik kanan `fcb.vbs` → **Edit** (Notepad). Isinya:

```vbs
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("Wscript.Shell")
here = fso.GetParentFolderName(WScript.ScriptFullName)
sh.Run "pythonw """ & here & "\fcc.py""", 0, False
```

Yang biasa diubah:

- **Nama file python** — kalau `fcc.py` di-rename, ganti juga `\fcc.py` di baris terakhir.
- **Path absolut** — kalau `fcc.py` tidak sefolder dengan `.vbs`, ganti `here & "\fcc.py"` menjadi path lengkap, contoh:
  ```vbs
  sh.Run "pythonw ""D:\Tools\FCB\fcc.py""", 0, False
  ```
- **Lihat console untuk debug** — ganti `pythonw` menjadi `python` dan `0, False` menjadi `1, True` agar jendela console tampil dan error terlihat.
- **Arti `0, False`** — `0` = jalan tersembunyi (tanpa kedip cmd), `False` = tidak menunggu aplikasi ditutup.

### APK helper (opsional, emoji full-otomatis)

ADB tidak bisa mengetik emoji (keterbatasan Android). APK mini di folder
`fcb-helper/` (8 KB, source Java disertakan) menerima teks via broadcast
lalu menaruhnya ke clipboard HP lewat Java API (unicode utuh),
disusul tombol PASTE otomatis. GBoard tidak berubah sama sekali.

1. Install: `adb install fcb-helper/fcb-helper.apk`
   (atau build sendiri: jalankan `build.bat` di folder itu —
   butuh JDK + Android SDK build-tools).
2. Buka aplikasi "FCB Helper" di HP: cek status izin, tap
   **Grant via Root** (HP root, popup Superuser) atau **Buka Settings**
   (non-root, aktifkan izin clipboard manual).
   Tanpa izin ini, paste emoji gagal diam-diam (MIUI membatasi tulis
   clipboard ke foreground-only).
3. Tab PTH otomatis pakai mode helper kalau teks mengandung emoji
   dan APK terdeteksi. Tanpa APK: teks tetap terkirim minus emoji
   (dilaporkan di log + dialog).

### Tab PTH (PC → HP)

1. Di HP: tap kolom teks sampai keyboard GBoard muncul (kursor aktif).
2. Ketik/paste teks di textbox, atau centang **Pakai Clipboard PC**.
3. Klik **Paste ke HP**.

### Tab HTP (HP → PC)

1. Di HP: blok teks → **Salin** seperti biasa.
2. Klik **Ambil dari HP** — teks masuk clipboard PC, tinggal `Ctrl+V`.
3. Atau centang **Auto-monitor HP** untuk sinkron otomatis.

## Arti error (tab PTH)

| Pesan | Artinya | Solusi |
|---|---|---|
| HP tidak nyambung | kabel / device salah / popup Allow belum di-OK | colok ulang, cek pilihan device, klik Reconnect |
| `security` | HP nolak inject (`INJECT_EVENTS`) | cek toggle Security settings + reboot |
| `connection` | ADB putus sesaat | retry otomatis 3x; masih gagal → Reconnect |
| `badchar` | teks berisi karakter yang tak bisa diketik (mis. full emoji) | ganti jadi karakter biasa |
| `other` | penyebab lain, detail mentah ditampilkan | sertakan log saat lapor bug |

## Struktur

```
FCB/
├── fcc.py       # aplikasi utama (PTH + HTP + Manual, satu file)
├── fcb-helper/  # source + APK helper (emoji via broadcast + PASTE)
│   ├── AndroidManifest.xml
│   ├── build.bat
│   ├── fcb-helper.apk
│   └── src/com/faa/fcbclip/*.java
├── fcb.vbs      # launcher Windows tanpa jendela cmd (double-click)
├── README.md
├── LICENSE      # MIT
└── .gitignore
```

Riwayat pengembangan: berawal dari dua script terpisah (`paste_pc_to_hp.py`, `paste_hp_to_pc.py`) yang digabung menjadi satu aplikasi tab.

## Batasan

- `adb shell input` hanya bisa mengetik karakter yang ada di keymap HP (ASCII). Emoji tidak bisa diketik — otomatis dibuang saat pengiriman.
- Clipboard HP yang bukan teks (mis. gambar) tidak didukung tab HTP.
- Multi-user Android: dibaca dari user utama (`userId 0`).

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).
