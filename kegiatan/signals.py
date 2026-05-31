from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Kegiatan, Notifikasi
from accounts.models import CustomUser

@receiver(pre_save, sender=Kegiatan)
def capture_old_status(sender, instance, **kwargs):
    if instance.pk:
        # Pengecekan ada atau tidaknya instance sebelumnya
        try:
            old_instance = Kegiatan.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Kegiatan.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Kegiatan)
def handle_status_change(sender, instance, created, **kwargs):
    status_baru = instance.status
    status_lama = getattr(instance, '_old_status', None)
    
    if created or status_baru == status_lama:
        return

    # 1. DOSEN UPLOAD LAPORAN -> KAPRODI
    if status_baru == 'WAITING_KAPRODI_REVIEW':
        kaprodi_list = CustomUser.objects.filter(role='KAPRODI', prodi=instance.dosen.prodi)
        for kaprodi in kaprodi_list:
            Notifikasi.objects.create(
                user=kaprodi,
                kegiatan=instance,
                pesan=f"Laporan Akhir untuk kegiatan '{instance.judul}' (Dosen: {instance.dosen.username}) siap untuk direview."
            )
            
    # 2. KAPRODI APPROVE -> DEKAN
    elif status_baru == 'WAITING_DEKAN_REVIEW':
        Notifikasi.objects.create(
            user=instance.dosen,
            kegiatan=instance,
            pesan=f"Laporan kegiatan '{instance.judul}' telah disetujui Kaprodi dan sedang direview oleh Dekan."
        )
        dekan_list = CustomUser.objects.filter(role='DEKAN', fakultas=instance.dosen.fakultas)
        for dekan in dekan_list:
            Notifikasi.objects.create(
                user=dekan,
                kegiatan=instance,
                pesan=f"Kegiatan '{instance.judul}' siap untuk persetujuan akhir (Dekan)."
            )

    # 3. KAPRODI REVISE -> DOSEN
    elif status_baru == 'REVISION_KAPRODI':
        Notifikasi.objects.create(
            user=instance.dosen,
            kegiatan=instance,
            pesan=f"Laporan kegiatan '{instance.judul}' perlu direvisi (Catatan Kaprodi)."
        )

    # 4. DEKAN APPROVE -> DOSEN
    elif status_baru == 'APPROVED_FINAL':
        Notifikasi.objects.create(
            user=instance.dosen,
            kegiatan=instance,
            pesan=f"Selamat! Laporan akhir kegiatan '{instance.judul}' telah disetujui sepenuhnya oleh Dekan."
        )

    # 5. DEKAN REVISE -> DOSEN
    elif status_baru == 'REVISION_DEKAN':
        Notifikasi.objects.create(
            user=instance.dosen,
            kegiatan=instance,
            pesan=f"Laporan kegiatan '{instance.judul}' perlu direvisi (Catatan Dekan)."
        )
