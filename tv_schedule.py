"""
tivie_scraper.py
Scraper jadwal siaran TV dari tivie.id
"""

import sys
import datetime
import requests
import bs4
from urllib.parse import urljoin

# ── Konstanta ────────────────────────────────────────────────────────────────

BASE_URL = "https://tivie.id/channel/"

TV_CHANNELS: tuple[str, ...] = (
    "antv", "gtv", "hbo", "inews", "indosiar", "kompastv", "mdtv",
    "mentaritv", "mnctv", "moji", "rcti", "rtv", "sctv", "trans7", "transtv",
)

# Label tampilan untuk setiap channel (key = nama slug, value = label layar)
_CHANNEL_LABELS: dict[str, str] = {
    "antv":     "ANTV",
    "gtv":      "GTV",
    "hbo":      "HBO",
    "inews":    "iNews",
    "indosiar": "INDOSIAR",
    "kompastv": "KOMPAS TV",
    "mdtv":     "MDTV",
    "mentaritv":"MENTARI TV",
    "mnctv":    "MNCTV",
    "moji":     "MOJI",
    "rcti":     "RCTI",
    "rtv":      "RTV",
    "sctv":     "SCTV",
    "trans7":   "TRANS7",
    "transtv":  "TRANS TV",
}

# CSS class yang dipakai tivie.id — simpan sebagai konstanta agar mudah diubah
_CLASS_ITEM    = "flex items-start w-full bg-white"
_CLASS_HOURS   = (
    "order-first flex w-1/2 flex justify-end -space-x-px "
    "before:content-[attr(before)] before:block before:shrink-0 before:w-2.5 before:scale-90 "
    "after:content-[attr(after)] after:block after:shrink-0 after:w-2.5 after:scale-90"
)
_CLASS_MINUTES = (
    "flex w-1/2 flex justify-start -space-x-px "
    "before:content-[attr(before)] before:block before:shrink-0 before:w-2.5 before:scale-90 "
    "after:content-[attr(after)] after:block after:shrink-0 after:w-2.5 after:scale-90"
)
_CLASS_PROGRAM = "flex-grow overflow-x-clip"

# ── Tipe alias ───────────────────────────────────────────────────────────────

Schedule = list[tuple[datetime.datetime, str]]

# ── Fungsi pemilihan channel ─────────────────────────────────────────────────

def _print_channel_list() -> None:
    """Cetak daftar channel yang tersedia ke layar."""
    print("\n=== Daftar Channel ===")
    for i, slug in enumerate(TV_CHANNELS, start=1):
        label = _CHANNEL_LABELS.get(slug, slug.upper())
        print(f"  {i:>2}. {label}")
    print()


def selected_channel() -> str | None:
    """
    Tampilkan menu channel, minta input pengguna, kembalikan slug channel
    yang dipilih, atau ``None`` jika input tidak valid.
    """
    _print_channel_list()
    raw = input("Masukkan no. channel: ").strip()
    try:
        number = int(raw)
    except ValueError:
        print("❌  Input tidak valid — harap masukkan angka.")
        return None

    if not (1 <= number <= len(TV_CHANNELS)):
        print(f"❌  Angka harus antara 1 dan {len(TV_CHANNELS)}.")
        return None

    return TV_CHANNELS[number - 1]


# ── Fungsi pengambilan jadwal ────────────────────────────────────────────────

def _parse_time(tag: bs4.Tag, today: datetime.datetime) -> datetime.datetime | None:
    """
    Ekstrak jam dan menit dari sepasang <span> tivie.id, kembalikan objek
    datetime. Kembalikan ``None`` jika elemen tidak ditemukan atau datanya
    rusak.
    """
    tag_h = tag.find("span", class_=_CLASS_HOURS)
    tag_m = tag.find("span", class_=_CLASS_MINUTES)
    if not tag_h or not tag_m:
        return None
    try:
        hours   = int(f"{tag_h['before']}{tag_h['after']}")
        minutes = int(f"{tag_m['before']}{tag_m['after']}")
        return today.replace(hour=hours, minute=minutes, second=0, microsecond=0)
    except (KeyError, ValueError):
        return None


def get_schedule(channel_name: str) -> Schedule | None:
    """
    Ambil jadwal siaran untuk *channel_name* dari tivie.id.

    Kembalikan list of ``(datetime, program_title)`` atau ``None`` bila
    terjadi kesalahan.
    """
    if not isinstance(channel_name, str) or not channel_name:
        print("❌  Nama channel harus berupa string yang tidak kosong.")
        return None

    url   = urljoin(BASE_URL, channel_name)
    today = datetime.datetime.now()

    # ── Kirim request ──────────────────────────────────────────────────────
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("❌  Tidak dapat terhubung ke server. Periksa koneksi internet Anda.")
        return None
    except requests.exceptions.Timeout:
        print("❌  Koneksi habis waktu (timeout). Coba lagi nanti.")
        return None
    except requests.exceptions.HTTPError as exc:
        print(f"❌  Server mengembalikan error HTTP: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        print(f"❌  Terjadi kesalahan jaringan: {exc}")
        return None

    # ── Parse HTML ─────────────────────────────────────────────────────────
    soup      = bs4.BeautifulSoup(response.text, "html.parser")
    tag_items = soup.find_all("div", class_=_CLASS_ITEM)

    if not tag_items:
        print("⚠️  Jadwal tidak ditemukan atau struktur halaman telah berubah.")
        return None

    # ── Ekstrak data ───────────────────────────────────────────────────────
    schedule: Schedule = []
    for tag in tag_items:
        time_obj = _parse_time(tag, today)
        if time_obj is None:
            continue  # lewati entri yang datanya rusak

        program_tag = tag.find("div", class_=_CLASS_PROGRAM)
        if program_tag is None:
            continue

        program_title = program_tag.get_text(separator=" ", strip=True)
        schedule.append((time_obj, program_title))

    return schedule if schedule else None


# ── Fungsi tampilan jadwal ───────────────────────────────────────────────────

def display_schedule(schedule: Schedule | None, channel_name: str = "") -> None:
    """
    Cetak jadwal siaran ke stdout.  Tampilkan penanda 'SEKARANG' pada
    program yang sedang tayang.
    """
    if not schedule:
        print("Tidak ada jadwal yang dapat ditampilkan.")
        return

    label = _CHANNEL_LABELS.get(channel_name, channel_name.upper())
    now   = datetime.datetime.now()

    print(f"\n{'='*50}")
    print(f"  Jadwal Siaran {label} — {now.strftime('%A, %d %B %Y')}")
    print(f"{'='*50}")

    # Tentukan program yang sedang tayang (entri terakhir yang waktunya ≤ sekarang)
    current_index: int | None = None
    for i, (t, _) in enumerate(schedule):
        if now >= t:
            current_index = i

    for i, (t, program) in enumerate(schedule):
        marker = " ◀ SEKARANG" if i == current_index else ""
        print(f"  {t.strftime('%H:%M')}  {program}{marker}")

    print(f"{'='*50}\n")


# ── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    """Fungsi utama: pilih channel → ambil jadwal → tampilkan."""
    print("╔══════════════════════════════════╗")
    print("║   Penjadwal Siaran TV — tivie.id ║")
    print("╚══════════════════════════════════╝")

    channel_name = selected_channel()
    if channel_name is None:
        sys.exit(1)

    print(f"\n⏳  Mengambil jadwal untuk {_CHANNEL_LABELS.get(channel_name, channel_name.upper())}…")
    schedule = get_schedule(channel_name)

    display_schedule(schedule, channel_name)


if __name__ == "__main__":
    main()