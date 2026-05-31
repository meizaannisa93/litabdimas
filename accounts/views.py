from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, UserJabatanForm

@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'DOSEN':
        return redirect('dosen_dashboard')
    elif role == 'KAPRODI':
        return redirect('kaprodi_dashboard')
    elif role == 'DEKAN':
        return redirect('dekan_dashboard')
    elif role == 'ADMIN':
        return redirect('/admin/')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        if 'btn_informasi_akun' in request.POST:
            form = UserProfileForm(request.POST, instance=request.user)
            jabatan_form = UserJabatanForm(instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Informasi akun berhasil diubah.')
                return redirect('profile')
        elif 'btn_jabatan_peran' in request.POST:
            form = UserProfileForm(instance=request.user)
            jabatan_form = UserJabatanForm(request.POST, instance=request.user)
            if jabatan_form.is_valid():
                jabatan_form.save()
                messages.success(request, 'Detail jabatan/peran berhasil diubah.')
                return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
        jabatan_form = UserJabatanForm(instance=request.user)
        
    return render(request, 'accounts/profile.html', {
        'form': form,
        'jabatan_form': jabatan_form
    })
