from django.apps import AppConfig

class KegiatanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kegiatan'

    def ready(self):
        import kegiatan.signals # Mendaftarkan signals
