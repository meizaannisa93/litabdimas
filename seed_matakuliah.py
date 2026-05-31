import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litabdimas_project.settings')
django.setup()

from kegiatan.models import MataKuliah

MATA_KULIAH_LIST = [
    "Anatomi Dasar",
    "Komunikasi Kesehatan",
    "Fisiologi",
    "Fisika Kesehatan",
    "Biomolekuler dan Biokimia Fisioterapi",
    "Sosiologi dan Antropologi Kesehatan",
    "Psikologi Kesehatan",
    "Konsep Dasar Fisioterapi",
    "Bahasa Inggris Dasar",
    "Pemeriksaan dan Pengukuran Fisioterapi",
    "Ilmu Perkembangan Gerak",
    "Farmakologi",
    "Promosi Kesehatan",
    "Patologi Sistem",
    "Pemeriksaan Penunjang",
    "Biomekanik dan Patomekanik",
    "Kewirausahaan",
    "Manajemen Fisioterapi Tumbuh Kembang dan Pediatrik",
    "Metodologi Penelitian dan Penulisan Ilmiah",
    "Epidemiologi",
    "Kesehatan Matra",
    "Manajemen Fisioterapi Neuromuskular",
    "Manajemen Fisioterapi Kardiovaskuler",
    "Manajemen Fisioterapi Ergonomi",
    "Etika Profesi, Hukum, dan Sistem Kesehatan Nasional",
    "Manajemen Pelayanan Fisioterapi",
    "Manajemen Fisioterapi Olahraga dan Wellness",
    "Manajemen Fisioterapi Geriatri",
    "Manajemen Fisioterapi Kegawatdaruratan (BTCLS)",
    "Hidroterapi dan Terapi Latihan Khusus",
    "Manajemen Fisioterapi Layanan Primer dan Komunitas",
    "Evidence Based Practice Physiotherapy",
    "Terapi Manual",
    "Manajemen Fisioterapi Kardiopulmonal",
    "English for Physiotherapy",
    "Manajemen Fisioterapi Muskuloskeletal",
    "Anatomi Terapan",
    "Biostatistik",
    "Terapi Latihan",
    "Patologi Umum",
    "Terapi Masase",
    "Fisiologi Latihan",
    "Ilmu Gizi Fisioterapi",
    "Elektroterapi dan Sumber Fisis",
    "Manajemen Fisioterapi Kesehatan Wanita dan Integumen",
]

def seed():
    created = 0
    skipped = 0
    for nama in MATA_KULIAH_LIST:
        obj, is_new = MataKuliah.objects.get_or_create(nama=nama)
        if is_new:
            print(f"  [OK] {nama}")
            created += 1
        else:
            print(f"  [SKIP] {nama}")
            skipped += 1

    print(f"\nSelesai! {created} mata kuliah ditambahkan, {skipped} sudah ada.")

if __name__ == '__main__':
    seed()
