import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'litabdimas_project.settings')
django.setup()

from accounts.models import Fakultas, ProgramStudi, CustomUser

def create_dosen_users():
    # Pastikan Fakultas & Prodi sudah ada
    fikes, _ = Fakultas.objects.get_or_create(nama='Ilmu Kesehatan')
    fisio, _ = ProgramStudi.objects.get_or_create(nama='S1 Fisioterapi', fakultas=fikes)

    dosen_list = [
        ("Agustiyawan", "agustiyawan@upnvj.ac.id"),
        ("Rabia", "rabia@upnvj.ac.id"),
        ("Kiki Rezki Faradillah", "kikirezkif@upnvj.ac.id"),
        ("Mona Oktarina", "monaoktarina@upnvj.ac.id"),
        ("Fidyatul Nazhira", "fidyatul@upnvj.ac.id"),
        ("Andy Sirada", "andy.sirada@upnvj.ac.id"),
        ("Heri Wibisono", "heri.wibisono@upnvj.ac.id"),
        ("Risa Kusuma Anggraeni", "risakusuma@upnvj.ac.id"),
        ("Sri Gunda Fahriana Fahruddin", "srigunda@upnvj.ac.id"),
        ("Sri Yani", "sri.yani@upnvj.ac.id"),
        ("Purnamadyawati", "purnama@upnvj.ac.id"),
        ("Rena Mailani", "rena.mailani@upnvj.ac.id"),
        ("Meiza Anniza", "meizaanniza@upnvj.ac.id"),
        ("Firdausiyah Rizki Amallia", "firdausiyahramallia@upnvj.ac.id"),
        ("Raufina Riandhani Mulyoto", "raufinarmulyoto@upnvj.ac.id"),
        ("A A I Ayesa Febrinia Adyasputri", "ayesafa@upnvj.ac.id"),
        ("Ni Nyoman Melani Karang", "nnmelanikarang@upnvj.ac.id"),
        ("Tina Zarkiyani", "tinaz@upnvj.ac.id"),
        ("Enny Fauziah", "ennyfauziah@upnvj.ac.id"),
        ("Arfian Hamzah", "arfianh@upnvj.ac.id"),
    ]

    password = "pass12345"
    created_count = 0
    skipped_count = 0

    for nama, email in dosen_list:
        # Pisahkan nama depan dan belakang
        parts = nama.split(' ', 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

        if CustomUser.objects.filter(username=email).exists():
            print(f"  [SKIP] {email} sudah ada")
            skipped_count += 1
            continue

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            role='DOSEN',
            fakultas=fikes,
            prodi=fisio,
            first_name=first_name,
            last_name=last_name,
        )
        print(f"  [OK] {email} - {nama}")
        created_count += 1

    print(f"\nSelesai! {created_count} dosen dibuat, {skipped_count} di-skip.")
    print(f"Password seragam: {password}")
    print(f"Login menggunakan email sebagai username.")

if __name__ == '__main__':
    create_dosen_users()
