import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litabdimas_project.settings')
django.setup()

from accounts.models import Fakultas, ProgramStudi, CustomUser
from kegiatan.models import Kegiatan

def debug_data():
    print("--- Debugging Relationships ---")
    users = CustomUser.objects.all()
    for u in users:
        print(f"User: {u.username}, Role: {u.role}, Fakultasi_ID: {u.fakultas_id}, Prodi_ID: {u.prodi_id}")
    
    kegiatans = Kegiatan.objects.all()
    print(f"\nTotal Kegiatan Global: {kegiatans.count()}")
    
    # Simulate Kaprodi Kep Dashboard
    kaprodi = CustomUser.objects.get(username='kaprodi_kep')
    prodi_users = CustomUser.objects.filter(prodi=kaprodi.prodi)
    semua_kaprodi = Kegiatan.objects.filter(dosen__in=prodi_users)
    print(f"\nKaprodi Kep Stats:")
    print(f"  Total Kegiatan: {semua_kaprodi.count()}")
    print(f"  Pending Review: {semua_kaprodi.filter(status='WAITING_KAPRODI_REVIEW').count()}")
    
    # Simulate Dekan Fikes Dashboard
    dekan = CustomUser.objects.get(username='dekan_fikes')
    fakultas_users = CustomUser.objects.filter(fakultas=dekan.fakultas)
    semua_dekan = Kegiatan.objects.filter(dosen__in=fakultas_users)
    print(f"\nDekan Fikes Stats:")
    print(f"  Total Kegiatan: {semua_dekan.count()}")
    print(f"  Pending Review: {semua_dekan.filter(status='WAITING_DEKAN_REVIEW').count()}")

    print("\n--- Listing All Activities ---")
    for k in kegiatans:
        print(f"Kegiatan: {k.judul}, Dosen: {k.dosen.username}, Status: {k.status}")
        print(f"  Dosen Prodi_ID: {k.dosen.prodi_id}, Dosen Fakultasi_ID: {k.dosen.fakultas_id}")

if __name__ == '__main__':
    debug_data()
