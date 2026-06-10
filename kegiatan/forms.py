import datetime
from django import forms
from .models import Kegiatan, Dokumen, MilestoneLog, ReviewLog, MataKuliah
from accounts.models import CustomUser

def get_tahun_akademik_choices():
    current_year = datetime.datetime.now().year
    choices = [('', '-- Pilih Tahun Akademik --')]
    for year in range(2019, current_year + 5):
        choices.append((f"{year}/{year+1}", f"{year}/{year+1}"))
    return choices

class DosenMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name() or obj.username

class KegiatanForm(forms.ModelForm):
    tahun_akademik = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Tahun Akademik'
    )
    tim_dosen = DosenMultipleChoiceField(
        queryset=CustomUser.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'}),
        label='Tim Dosen'
    )

    class Meta:
        model = Kegiatan
        fields = ['judul', 'kategori', 'tahun_akademik', 'semester', 'status_pelaksanaan', 'sumber_pendanaan', 'tim_dosen', 'deskripsi', 'link_jurnal', 'integrasi_mata_kuliah']
        labels = {
            'status_pelaksanaan': 'Status Pengisian',
            'sumber_pendanaan': 'Sumber Pendanaan',
            'link_jurnal': 'Link Jurnal (URL) / Link Dokumen',
            'integrasi_mata_kuliah': 'Integrasi Mata Kuliah',
            'semester': 'Semester',
        }
        widgets = {
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
            'integrasi_mata_kuliah': forms.SelectMultiple(attrs={'class': 'form-control select2-multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tahun_akademik'].choices = get_tahun_akademik_choices()
        self.fields['integrasi_mata_kuliah'].queryset = MataKuliah.objects.all()
        self.fields['integrasi_mata_kuliah'].required = False
        self.fields['tim_dosen'].queryset = CustomUser.objects.filter(role='DOSEN')

class DokumenForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        fields = ['file', 'deskripsi']
        labels = {
            'file': 'File PDF max 10MB',
            'deskripsi': 'Deskripsi Artikel'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False
        self.fields['deskripsi'].required = False

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
        fields = ['keputusan_roadmap', 'keputusan_integrasi_mk', 'catatan']
        labels = {
            'keputusan_roadmap': 'Keputusan Roadmap',
            'keputusan_integrasi_mk': 'Keputusan Integrasi Mata Kuliah',
        }
        widgets = {
            'keputusan_roadmap': forms.Select(attrs={'class': 'form-control'}),
            'keputusan_integrasi_mk': forms.Select(attrs={'class': 'form-control'}),
            'catatan': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Berikan catatan (wajib jika direvisi).'}),
        }
