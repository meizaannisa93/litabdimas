from django import forms
from .models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'nip', 'phone', 'google_scholar_link', 'scopus_link', 'roadmap_link']
        labels = {
            'first_name': 'Nama Lengkap (Depan)',
            'last_name': 'Nama Belakang',
            'email': 'Alamat Email',
            'nip': 'NIP / NIDN',
            'phone': 'Nomor Identitas / Telepon',
            'google_scholar_link': 'Link Akun Google Scholar',
            'scopus_link': 'Link Scopus',
            'roadmap_link': 'Link Roadmap',
        }

class UserJabatanForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['fakultas', 'prodi']
        labels = {
            'fakultas': 'Fakultas',
            'prodi': 'Program Studi'
        }

