"""
translate.py — kamus alias emoji -> teks (PC-side).

Dipakai otomatis oleh pengirim PTH (paste_pc_to_hp.py / faa_clipboard_copas.py
/ fcc.py) pada tahap sanitasi: emoji yg punya alias DIUBAH jadi teks (bukan
dibuang), sehingga maknanya tetap sampai ke HP. Emoji tanpa alias tetap
dibuang + dilaporkan seperti biasa.

Cara nambah alias: tambah baris "emoji": "[alias]", misal:
    "\U0001F600": "[senyum]",
Lalu paste ulang — tidak perlu restart apa-apa (dibaca tiap pengiriman).

Aturan alias yg bagus:
- unik & jelas (pakai kurung [...] agar tidak tertukar kata biasa),
- pakai kata yg dimengerti aplikasi tujuan (mis. prompt AI),
- emoji multi-karakter (mis. ❤️ = U+2764 U+FE0F) otomatis diutamakan
  karena pencocokan diurut dari yg terpanjang.
"""

# Kamus bawaan. Ubah/tambah sesukamu — file ini milikmu.
EMOJI_ALIASES = {
    "\U0001FA75": "[hati biru]",     # 🩵 light blue heart
    "\u2764\uFE0F": "[hati merah]",  # ❤️ red heart (varian + VS16)
    "\u2764": "[hati merah]",        # ❤ red heart (tanpa VS16)
    "\U0001F525": "[api]",           # 🔥 fire
    "\U0001F602": "[tertawa]",       # 😂 face with tears of joy
    "\U0001F60D": "[love]",          # 😍 smiling face with heart-eyes
    "\U0001F622": "[menangis]",      # 😢 crying face
    "\U0001F44D": "[jempol]",        # 👍 thumbs up
    "\U0001F44E": "[jempol bawah]",  # 👎 thumbs down
    "\U0001F64F": "[berdoa]",        # 🙏 folded hands
    "\u2B50": "[bintang]",           # ⭐ star
    "\u2705": "[centang]",           # ✅ check mark
}


def translate_aliases(s: str) -> tuple[str, list[tuple[str, str]]]:
    """Ganti emoji yg punya alias. Return (teks_baru, [(emoji, alias), ...])."""
    found: list[tuple[str, str]] = []
    out = s
    # terpanjang dulu agar varian multi-karakter menang atas tunggalnya
    for emo, alias in sorted(EMOJI_ALIASES.items(), key=lambda kv: -len(kv[0])):
        if emo in out:
            out = out.replace(emo, alias)
            found.append((emo, alias))
    return out, found


if __name__ == "__main__":
    # demo cepat: python translate.py (aman di console Windows)
    demo = "Aku suka kamu \U0001FA75 dan ini \U0001F525 banget \U0001F600"
    new, rep = translate_aliases(demo)
    print("OUT:", ascii(new))
    print("ganti:", [(ascii(e), a) for e, a in rep] if rep else "-")
