from django.contrib import admin
from .models import Kegiatan, Dokumen, MilestoneLog, ReviewLog, Notifikasi, MataKuliah

@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)
    ordering = ('nama',)

class DokumenInline(admin.TabularInline):
    model = Dokumen
    extra = 1

class MilestoneLogInline(admin.TabularInline):
    model = MilestoneLog
    extra = 1

@admin.register(Kegiatan)
class KegiatanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'dosen', 'kategori', 'status', 'tahun_akademik')
    list_filter = ('status', 'kategori', 'tahun_akademik')
    search_fields = ('judul', 'dosen__username')
    inlines = [DokumenInline, MilestoneLogInline]

admin.site.register(Dokumen)
admin.site.register(MilestoneLog)
admin.site.register(ReviewLog)
admin.site.register(Notifikasi)
