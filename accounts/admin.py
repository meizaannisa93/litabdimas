from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Fakultas, ProgramStudi

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'prodi', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Civitas Akademika', {'fields': ('role', 'fakultas', 'prodi', 'nip', 'phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Fakultas)
admin.site.register(ProgramStudi)
