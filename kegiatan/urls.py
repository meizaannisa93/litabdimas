from django.urls import path
from . import views

urlpatterns = [
    # DOSEN
    path('dosen/', views.dosen_dashboard, name='dosen_dashboard'),
    path('dosen/kegiatan/tambah/', views.tambah_kegiatan, name='tambah_kegiatan'),
    path('dosen/kegiatan/<int:pk>/', views.detail_kegiatan, name='detail_kegiatan'),
    path('dosen/kegiatan/<int:pk>/edit/', views.edit_kegiatan, name='edit_kegiatan'),
    path('dosen/kegiatan/<int:pk>/hapus/', views.hapus_kegiatan, name='hapus_kegiatan'),
    path('dosen/kegiatan/<int:pk>/milestone/', views.tambah_milestone, name='tambah_milestone'),
    path('dosen/kegiatan/<int:pk>/laporan/', views.upload_laporan, name='upload_laporan'),
    
    # KAPRODI
    path('kaprodi/', views.kaprodi_dashboard, name='kaprodi_dashboard'),
    
    # DEKAN
    path('dekan/', views.dekan_dashboard, name='dekan_dashboard'),
    
    # SHARED REVIEW (Kaprodi & Dekan)
    path('review/<int:pk>/', views.review_kegiatan, name='review_kegiatan'),
    
    # DAFTAR KEGIATAN SPESIFIK
    path('penelitian/', views.penelitian_list, name='penelitian_list'),
    path('pengabdian/', views.pengabdian_list, name='pengabdian_list'),
    
    # NOTIFIKASI
    path('notifikasi/', views.list_notifikasi, name='list_notifikasi'),
]
