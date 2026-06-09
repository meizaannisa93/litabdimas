from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
import os

class MataKuliah(models.Model):
    nama = models.CharField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['nama']
        verbose_name = 'Mata Kuliah'
        verbose_name_plural = 'Daftar Mata Kuliah'
    
    def __str__(self):
        return self.nama

def validate_pdf_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() == '.pdf':
        raise ValidationError('File harus berformat PDF.')

def validate_file_size(value):
    limit = 10 * 1024 * 1024  # 10 MB
    if value.size > limit:
        raise ValidationError('Ukuran file maksimal adalah 10 MB.')

class Kegiatan(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft Proposal'),
        ('ONGOING', 'Ongoing / Pelaksanaan'),
        ('WAITING_KAPRODI_REVIEW', 'Menunggu Review Kaprodi'),
        ('REVISION_KAPRODI', 'Revisi dari Kaprodi'),
        ('WAITING_DEKAN_REVIEW', 'Menunggu Review Dekan'),
        ('REVISION_DEKAN', 'Revisi dari Dekan'),
        ('APPROVED_FINAL', 'Selesai / Approved Final'),
    ]

    KATEGORI_CHOICES = [
        ('PENELITIAN', 'Penelitian'),
        ('PENGABDIAN', 'Pengabdian Masyarakat'),
    ]

    dosen = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='kegiatan')
    judul = models.CharField(max_length=255)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    deskripsi = models.TextField()
    SEMESTER_CHOICES = [
        ('GANJIL', 'Semester Ganjil'),
        ('GENAP', 'Semester Genap'),
    ]

    tahun_akademik = models.CharField(max_length=20)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='GANJIL')
    STATUS_PELAKSANAAN_CHOICES = [
        ('ONGOING', 'On going'),
        ('PUBLISHED', 'Sudah publish'),
    ]

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    
    status_pelaksanaan = models.CharField(max_length=20, choices=STATUS_PELAKSANAAN_CHOICES, default='ONGOING')
    kategori_status = models.CharField(max_length=50, blank=True, null=True)
    link_jurnal = models.URLField(blank=True, null=True)
    integrasi_mata_kuliah = models.ForeignKey(
        'MataKuliah', on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Integrasi Mata Kuliah'
    )
    SUMBER_PENDANAAN_CHOICES = [
        ('MANDIRI', 'Mandiri'),
        ('HIBAH', 'Hibah'),
    ]
    sumber_pendanaan = models.CharField(
        max_length=20,
        choices=SUMBER_PENDANAAN_CHOICES,
        default='MANDIRI',
        verbose_name='Sumber Pendanaan'
    )
    tim_dosen = models.ManyToManyField(
        CustomUser,
        related_name='tim_kegiatan',
        verbose_name='Tim Dosen'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul

class Dokumen(models.Model):
    JENIS_CHOICES = [
        ('PROPOSAL', 'Proposal Diterima'),
        ('LAPORAN_AKHIR', 'Laporan Akhir'),
        ('LUARAN', 'Bukti Luaran'),
    ]
    
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='dokumen')
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES)
    file = models.FileField(upload_to='dokumen_kegiatan/', validators=[validate_pdf_extension, validate_file_size])
    deskripsi = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_jenis_display()} - {self.kegiatan.judul}"

class MilestoneLog(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='milestone_logs')
    tanggal = models.DateField()
    deskripsi = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Milestone: {self.tanggal} - {self.kegiatan.judul}"

class ReviewLog(models.Model):
    KEPUTUSAN_CHOICES = [
        ('APPROVE', 'Sesuai'),
        ('REVISE', 'Tidak Sesuai'),
    ]
    
    TINGKAT_CHOICES = [
        ('KAPRODI', 'Tingkat Kaprodi'),
        ('DEKAN', 'Tingkat Dekan'),
    ]

    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='review_logs')
    aktor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    tingkat = models.CharField(max_length=20, choices=TINGKAT_CHOICES)
    keputusan = models.CharField(max_length=20, choices=KEPUTUSAN_CHOICES)
    catatan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_keputusan_display()} by {self.aktor.username}"

class Notifikasi(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifikasi')
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, null=True, blank=True)
    pesan = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.user.username} - {self.pesan[:30]}"
