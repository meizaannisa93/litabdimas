from django.db import models
from django.contrib.auth.models import AbstractUser

class Fakultas(models.Model):
    nama = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama

class ProgramStudi(models.Model):
    nama = models.CharField(max_length=100)
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE, related_name='prodi')
    
    def __str__(self):
        return self.nama

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DOSEN', 'Dosen'),
        ('KAPRODI', 'Koordinator Program Studi'),
        ('DEKAN', 'Dekan'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='DOSEN')
    fakultas = models.ForeignKey(Fakultas, on_delete=models.SET_NULL, null=True, blank=True)
    prodi = models.ForeignKey(ProgramStudi, on_delete=models.SET_NULL, null=True, blank=True)
    nip = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    google_scholar_link = models.URLField(blank=True, null=True)
    scopus_link = models.URLField(blank=True, null=True, verbose_name='Link Scopus')
    roadmap_link = models.URLField(blank=True, null=True, verbose_name='Link Roadmap')
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
