import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litabdimas_project.settings')
django.setup()

from accounts.models import Fakultas, ProgramStudi, CustomUser
from kegiatan.models import Kegiatan, Dokumen, ReviewLog, MilestoneLog
from django.utils import timezone
from datetime import timedelta

def create_demo_data():
    print("Membersihkan database lama (data demo)...")
    # Kita hapus data lama agar bersih, kecuali superuser jika ingin dipertahankan
    # Namun untuk seed ini kita reset saja agar sesuai skema baru
    Fakultas.objects.all().delete()
    CustomUser.objects.all().delete()
    
    # 1. Buat Fakultas Ilmu Kesehatan (FIKES)
    print("Membuat Fakultas Ilmu Kesehatan & Program Studi...")
    fikes = Fakultas.objects.create(nama='Ilmu Kesehatan')
    feb = Fakultas.objects.create(nama='Ekonomi dan Bisnis')
    
    # Prodi FIKES
    kep = ProgramStudi.objects.create(nama='S1 Keperawatan', fakultas=fikes)
    kesmas = ProgramStudi.objects.create(nama='S1 Kesehatan Masyarakat', fakultas=fikes)
    farmasi = ProgramStudi.objects.create(nama='S1 Farmasi', fakultas=fikes)
    fisio = ProgramStudi.objects.create(nama='S1 Fisioterapi', fakultas=fikes)

    # 2. Buat Users
    print("Membuat Users FIKES...")
    
    # Admin / Superuser
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser('admin', 'admin@upnvj.ac.id', 'admin123', role='ADMIN')
        print("- Admin created")
    
    # Dekan FIKES
    dekan_fikes = CustomUser.objects.create_user(
        username='dekan_fikes', password='password123', 
        role='DEKAN', fakultas=fikes, first_name='Dekan', last_name='FIKES',
        nip='197001012000031001'
    )
    print("- Dekan FIKES created")
    
    # Kaprodi Keperawatan
    kaprodi_kep = CustomUser.objects.create_user(
        username='kaprodi_kep', password='password123', 
        role='KAPRODI', fakultas=fikes, prodi=kep, first_name='Kajur', last_name='Keperawatan',
        nip='198005122010122001'
    )
    print("- Kaprodi Keperawatan created")

    # Dosen 1 (Keperawatan)
    dosen_kep1 = CustomUser.objects.create_user(
        username='dosen_kep1', password='password123', 
        role='DOSEN', fakultas=fikes, prodi=kep, first_name='Anisa', last_name='S.Kep',
        nip='199008202022032001'
    )
    
    # Dosen 2 (Kesmas)
    dosen_kesmas1 = CustomUser.objects.create_user(
        username='dosen_kesmas1', password='password123', 
        role='DOSEN', fakultas=fikes, prodi=kesmas, first_name='Budi', last_name='SKM',
        nip='198812122018031002'
    )
    print("- Dosen created")

    # 3. Buat 5 Data Penelitian Dummy
    print("Membuat 5 Data Penelitian Scenarios...")

    # Scenario 1: Ongoing (Dosen Keperawatan)
    k1 = Kegiatan.objects.create(
        dosen=dosen_kep1, judul="Analisis Pola Makan Lansia di Jakarta Timur",
        kategori="PENELITIAN", tahun_akademik="2025/2026",
        status="ONGOING", deskripsi="Penelitian tentang korelasi asupan nutrisi terhadap kesehatan jantung lansia."
    )
    Dokumen.objects.create(kegiatan=k1, jenis="PROPOSAL", file="demo_proposal1.pdf")
    
    # Scenario 2: Menunggu Review Kaprodi (Dosen Keperawatan)
    k2 = Kegiatan.objects.create(
        dosen=dosen_kep1, judul="Efektivitas Edukasi Cuci Tangan di Sekolah Dasar",
        kategori="PENGABDIAN", tahun_akademik="2025/2026",
        status="WAITING_KAPRODI_REVIEW", deskripsi="Program pengabdian untuk meningkatkan kesadaran sanitasi anak."
    )
    Dokumen.objects.create(kegiatan=k2, jenis="PROPOSAL", file="prop2.pdf")
    Dokumen.objects.create(kegiatan=k2, jenis="LAPORAN_AKHIR", file="laporan_akhir2.pdf")

    # Scenario 3: Revisi Kaprodi (Dosen Keperawatan)
    k3 = Kegiatan.objects.create(
        dosen=dosen_kep1, judul="Studi Kasus Penanganan Stunting di Puskesmas Limo",
        kategori="PENELITIAN", tahun_akademik="2025/2026",
        status="REVISION_KAPRODI", deskripsi="Evaluasi program intervensi gizi pada balita stunting."
    )
    Dokumen.objects.create(kegiatan=k3, jenis="PROPOSAL", file="prop3.pdf")
    Dokumen.objects.create(kegiatan=k3, jenis="LAPORAN_AKHIR", file="lap3_v1.pdf")
    ReviewLog.objects.create(kegiatan=k3, aktor=kaprodi_kep, tingkat="KAPRODI", keputusan="REVISE", catatan="Metodologi pada laporan akhir kurang detail bagian instrumen.")

    # Scenario 4: Menunggu Review Dekan (Dosen Kesmas)
    k4 = Kegiatan.objects.create(
        dosen=dosen_kesmas1, judul="Pemetaan Penyakit Menular di Wilayah Urban",
        kategori="PENELITIAN", tahun_akademik="2025/2026",
        status="WAITING_DEKAN_REVIEW", deskripsi="Analisis geospasial penyebaran penyakit DBD."
    )
    Dokumen.objects.create(kegiatan=k4, jenis="PROPOSAL", file="prop4.pdf")
    Dokumen.objects.create(kegiatan=k4, jenis="LAPORAN_AKHIR", file="lap4_final.pdf")
    ReviewLog.objects.create(kegiatan=k4, aktor=kaprodi_kep, tingkat="KAPRODI", keputusan="APPROVE", catatan="Bagus, layak diajukan ke Dekan.")

    # Scenario 5: Approved Final (Dosen Keperawatan)
    k5 = Kegiatan.objects.create(
        dosen=dosen_kep1, judul="Digitalisasi Rekam Medis untuk Klinik Swadaya",
        kategori="PENGABDIAN", tahun_akademik="2024/2025",
        status="APPROVED_FINAL", deskripsi="Implementasi sistem manajemen pasien sederhana."
    )
    Dokumen.objects.create(kegiatan=k5, jenis="PROPOSAL", file="prop5.pdf")
    Dokumen.objects.create(kegiatan=k5, jenis="LAPORAN_AKHIR", file="lap5_complete.pdf")
    ReviewLog.objects.create(kegiatan=k5, aktor=kaprodi_kep, tingkat="KAPRODI", keputusan="APPROVE", catatan="Sesuai target.")
    ReviewLog.objects.create(kegiatan=k5, aktor=dekan_fikes, tingkat="DEKAN", keputusan="APPROVE", catatan="Sangat bermanfaat bagi masyarakat.")
    
    print("\nData FIKES Berhasil Diperbarui!")
    print("Login credentials:")
    print("1. admin / admin123")
    print("2. dekan_fikes / password123")
    print("3. kaprodi_kep / password123")
    print("4. dosen_kep1 / password123")
    print("5. dosen_kesmas1 / password123")

if __name__ == '__main__':
    create_demo_data()
