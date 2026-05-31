from django import forms
from .models import Kegiatan, Dokumen, MilestoneLog, ReviewLog, MataKuliah

class KegiatanForm(forms.ModelForm):
    class Meta:
        model = Kegiatan
        fields = ['judul', 'kategori', 'tahun_akademik', 'semester', 'status_pelaksanaan', 'deskripsi', 'link_jurnal', 'integrasi_mata_kuliah']
        labels = {
            'status_pelaksanaan': 'Status Pengisian',
            'link_jurnal': 'Link Jurnal (URL) / Link Dokumen',
            'integrasi_mata_kuliah': 'Integrasi Mata Kuliah',
            'semester': 'Semester',
            'tahun_akademik': 'Tahun Akademik',
        }
        widgets = {
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
            'integrasi_mata_kuliah': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['integrasi_mata_kuliah'].queryset = MataKuliah.objects.all()
        self.fields['integrasi_mata_kuliah'].empty_label = '-- Pilih Mata Kuliah --'
        self.fields['integrasi_mata_kuliah'].required = False

class DokumenForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        fields = ['file', 'deskripsi']
        labels = {
            'file': 'File PDF max 10MB',
            'deskripsi': 'Deskripsi Artikel'
        }

class LaporanAkhirForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        fields = ['file', 'deskripsi']
        labels = {
            'file': 'File Laporan Akhir (PDF max 10MB)',
            'deskripsi': 'Deskripsi Singkat Laporan/Luaran'
        }

class MilestoneLogForm(forms.ModelForm):
    class Meta:
        model = MilestoneLog
        fields = ['tanggal', 'deskripsi']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewLog
        fields = ['keputusan', 'catatan']
        widgets = {
            'catatan': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Berikan catatan (wajib jika direvisi).'}),
        }
