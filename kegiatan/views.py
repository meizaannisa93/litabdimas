from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from .models import Kegiatan, Dokumen, MilestoneLog, ReviewLog, Notifikasi
from .forms import KegiatanForm, DokumenForm, LaporanAkhirForm, MilestoneLogForm, ReviewForm
from accounts.models import CustomUser

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(request, "Anda tidak memiliki akses ke halaman ini.")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# --- DOSEN VIEWS ---
@login_required
@role_required(['DOSEN'])
def dosen_dashboard(request):
    if not request.user.nip:
        messages.warning(request, "Perhatian: NIP Anda belum terdaftar di sistem. Mohon segera lengkapi profil Anda.")
        
    kegiatans = Kegiatan.objects.filter(dosen=request.user).order_by('-created_at')
    
    total_aktif = kegiatans.exclude(status='APPROVED_FINAL').count()
    total_selesai = kegiatans.filter(status='APPROVED_FINAL').count()

    context = {
        'kegiatans': kegiatans,
        'total_aktif': total_aktif,
        'total_selesai': total_selesai,
    }
    return render(request, 'kegiatan/dosen_dashboard.html', context)

@login_required
@role_required(['DOSEN'])
def tambah_kegiatan(request):
    if request.method == 'POST':
        form = KegiatanForm(request.POST)
        dokumen_form = DokumenForm(request.POST, request.FILES)
        if form.is_valid() and dokumen_form.is_valid():
            with transaction.atomic():
                kegiatan = form.save(commit=False)
                kegiatan.dosen = request.user
                kegiatan.status = 'ONGOING'
                kegiatan.save()
                form.save_m2m()
                
                dokumen = dokumen_form.save(commit=False)
                dokumen.kegiatan = kegiatan
                dokumen.jenis = 'PROPOSAL'
                dokumen.save()
                
            messages.success(request, 'Kegiatan berhasil ditambahkan.')
            return redirect('dosen_dashboard')
    else:
        form = KegiatanForm()
        dokumen_form = DokumenForm()
        
    return render(request, 'kegiatan/tambah_kegiatan.html', {
        'form': form,
        'dokumen_form': dokumen_form
    })

@login_required
@role_required(['DOSEN'])
def edit_kegiatan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk, dosen=request.user)
    
    proposal_doc = kegiatan.dokumen.filter(jenis='PROPOSAL').first()
    
    if request.method == 'POST':
        form = KegiatanForm(request.POST, instance=kegiatan)
        dokumen_form = DokumenForm(request.POST, request.FILES, instance=proposal_doc)
        
        if form.is_valid() and dokumen_form.is_valid():
            with transaction.atomic():
                kegiatan = form.save(commit=False)
                
                # Update main status based on status_pelaksanaan selection
                if kegiatan.status_pelaksanaan == 'ONGOING':
                    kegiatan.status = 'ONGOING'
                    
                kegiatan.save()
                form.save_m2m()
                
                dokumen = dokumen_form.save(commit=False)
                dokumen.kegiatan = kegiatan
                dokumen.jenis = 'PROPOSAL'
                dokumen.save()
                
            messages.success(request, 'Kegiatan berhasil diperbarui.')
            return redirect('detail_kegiatan', pk=kegiatan.pk)
    else:
        form = KegiatanForm(instance=kegiatan)
        dokumen_form = DokumenForm(instance=proposal_doc)
        
    return render(request, 'kegiatan/edit_kegiatan.html', {
        'form': form,
        'dokumen_form': dokumen_form,
        'kegiatan': kegiatan
    })

@login_required
@role_required(['DOSEN'])
def hapus_kegiatan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk, dosen=request.user)
    if request.method == 'POST':
        kegiatan.delete()
        messages.success(request, 'Kegiatan berhasil dihapus.')
    return redirect('dosen_dashboard')

@login_required
def detail_kegiatan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    
    # Simple access control
    if request.user.role == 'DOSEN' and kegiatan.dosen != request.user:
        messages.error(request, "Anda tidak memiliki akses ke kegiatan ini.")
        return redirect('dashboard')
    elif request.user.role == 'KAPRODI' and kegiatan.dosen.prodi != request.user.prodi:
        messages.error(request, "Anda tidak memiliki akses ke kegiatan ini.")
        return redirect('dashboard')
    elif request.user.role == 'DEKAN' and kegiatan.dosen.fakultas != request.user.fakultas:
        messages.error(request, "Anda tidak memiliki akses ke kegiatan ini.")
        return redirect('dashboard')

    milestones = kegiatan.milestone_logs.all().order_by('-tanggal')
    reviews = kegiatan.review_logs.all().order_by('-created_at')
    dokumens = kegiatan.dokumen.all().order_by('-uploaded_at')

    context = {
        'kegiatan': kegiatan,
        'milestones': milestones,
        'reviews': reviews,
        'dokumens': dokumens,
    }
    return render(request, 'kegiatan/detail_kegiatan.html', context)

@login_required
@role_required(['DOSEN'])
def tambah_milestone(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk, dosen=request.user)
    
    if request.method == 'POST':
        form = MilestoneLogForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.kegiatan = kegiatan
            milestone.created_by = request.user
            milestone.save()
            messages.success(request, 'Milestone berhasil ditambahkan.')
            return redirect('detail_kegiatan', pk=kegiatan.pk)
    else:
        form = MilestoneLogForm()
        
    return render(request, 'kegiatan/tambah_milestone.html', {'form': form, 'kegiatan': kegiatan})

@login_required
@role_required(['DOSEN'])
def upload_laporan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk, dosen=request.user)
    
    if request.method == 'POST':
        form = LaporanAkhirForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                dokumen = form.save(commit=False)
                dokumen.kegiatan = kegiatan
                dokumen.jenis = 'LAPORAN_AKHIR'
                dokumen.save()
                
                # Update status
                kegiatan.status = 'WAITING_KAPRODI_REVIEW'
                kegiatan.save()
                
            messages.success(request, 'Laporan akhir berhasil diunggah. Menunggu review Kaprodi.')
            return redirect('detail_kegiatan', pk=kegiatan.pk)
    else:
        form = LaporanAkhirForm()
        
    return render(request, 'kegiatan/upload_laporan.html', {'form': form, 'kegiatan': kegiatan})

# --- KAPRODI VIEWS ---
@login_required
@role_required(['KAPRODI'])
def kaprodi_dashboard(request):
    if not request.user.nip:
        messages.warning(request, "Perhatian: NIP Anda belum terdaftar di sistem. Mohon segera lengkapi profil Anda.")
        
    prodi_users = CustomUser.objects.filter(prodi=request.user.prodi)
    semua_kegiatan = Kegiatan.objects.filter(dosen__in=prodi_users)
    
    # Pending actions
    pending_kegiatans = semua_kegiatan.filter(status='WAITING_KAPRODI_REVIEW').order_by('updated_at')
    
    # Metrics
    total_kegiatan = semua_kegiatan.count()
    total_penelitian = semua_kegiatan.filter(kategori='PENELITIAN').count()
    total_pengabdian = semua_kegiatan.filter(kategori='PENGABDIAN').count()

    # Statistik Integrasi Mata Kuliah
    stats_raw = semua_kegiatan.exclude(integrasi_mata_kuliah=None).values(
        'tahun_akademik', 'integrasi_mata_kuliah__nama', 'kategori'
    ).annotate(count=Count('id'))

    mk_stats_dict = {}
    for item in stats_raw:
        tahun = item['tahun_akademik']
        mk_nama = item['integrasi_mata_kuliah__nama']
        kategori = item['kategori']
        count = item['count']

        if tahun not in mk_stats_dict:
            mk_stats_dict[tahun] = {}
        
        if mk_nama not in mk_stats_dict[tahun]:
            mk_stats_dict[tahun][mk_nama] = {'PENELITIAN': 0, 'PENGABDIAN': 0, 'total': 0}
        
        mk_stats_dict[tahun][mk_nama][kategori] = count
        mk_stats_dict[tahun][mk_nama]['total'] += count

    mk_stats = []
    for tahun, mks in sorted(mk_stats_dict.items(), reverse=True):
        year_data = {'tahun': tahun, 'items': []}
        for mk_nama, counts in sorted(mks.items()):
            total = counts['total']
            p_count = counts['PENELITIAN']
            m_count = counts['PENGABDIAN']
            year_data['items'].append({
                'mk_nama': mk_nama,
                'penelitian_count': p_count,
                'pengabdian_count': m_count,
                'total': total,
                'penelitian_pct': round((p_count / total * 100), 1) if total > 0 else 0,
                'pengabdian_pct': round((m_count / total * 100), 1) if total > 0 else 0,
            })
        mk_stats.append(year_data)

    context = {
        'pending_kegiatans': pending_kegiatans,
        'semua_kegiatan': semua_kegiatan,
        'total_kegiatan': total_kegiatan,
        'total_penelitian': total_penelitian,
        'total_pengabdian': total_pengabdian,
        'mk_stats': mk_stats,
    }
    return render(request, 'kegiatan/kaprodi_dashboard.html', context)

@login_required
@role_required(['KAPRODI', 'DEKAN'])
def review_kegiatan(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    laporan_dokumen = kegiatan.dokumen.filter(jenis='LAPORAN_AKHIR').last()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                keputusan = form.cleaned_data['keputusan']
                catatan = form.cleaned_data['catatan']
                
                review = ReviewLog(
                    kegiatan=kegiatan,
                    aktor=request.user,
                    keputusan=keputusan,
                    catatan=catatan
                )
                
                if request.user.role == 'KAPRODI':
                    review.tingkat = 'KAPRODI'
                    if keputusan == 'APPROVE':
                        kegiatan.status = 'WAITING_DEKAN_REVIEW'
                    else:
                        kegiatan.status = 'REVISION_KAPRODI'
                elif request.user.role == 'DEKAN':
                    review.tingkat = 'DEKAN'
                    if keputusan == 'APPROVE':
                        kegiatan.status = 'APPROVED_FINAL'
                    else:
                        kegiatan.status = 'REVISION_DEKAN'
                        
                review.save()
                kegiatan.save()
                
            messages.success(request, f'Review berhasil disimpan sebagai {keputusan}.')
            return redirect('dashboard')
    else:
        form = ReviewForm()
        
    return render(request, 'kegiatan/review_interface.html', {
        'kegiatan': kegiatan,
        'laporan': laporan_dokumen,
        'form': form
    })

# --- DEKAN VIEWS ---
@login_required
@role_required(['DEKAN'])
def dekan_dashboard(request):
    if not request.user.nip:
        messages.warning(request, "Perhatian: NIP Anda belum terdaftar di sistem. Mohon segera lengkapi profil Anda.")
        
    fakultas_users = CustomUser.objects.filter(fakultas=request.user.fakultas)
    semua_kegiatan = Kegiatan.objects.filter(dosen__in=fakultas_users)
    
    pending_kegiatans = semua_kegiatan.filter(status='WAITING_DEKAN_REVIEW').order_by('updated_at')
    
    total_kegiatan = semua_kegiatan.count()

    context = {
        'pending_kegiatans': pending_kegiatans,
        'semua_kegiatan': semua_kegiatan,
        'total_kegiatan': total_kegiatan,
    }
    return render(request, 'kegiatan/dekan_dashboard.html', context)

# --- NOTIFIKASI VIEWS ---
@login_required
def list_notifikasi(request):
    notifikasi = request.user.notifikasi.all().order_by('-created_at')
    notifikasi.filter(is_read=False).update(is_read=True)
    return render(request, 'kegiatan/notifikasi.html', {'notifikasi': notifikasi})

# --- DAFTAR KEGIATAN VIEWS ---
@login_required
def penelitian_list(request):
    if request.user.role == 'DOSEN':
        kegiatans = Kegiatan.objects.filter(dosen=request.user, kategori='PENELITIAN').order_by('-created_at')
    elif request.user.role == 'KAPRODI':
        prodi_users = CustomUser.objects.filter(prodi=request.user.prodi)
        kegiatans = Kegiatan.objects.filter(dosen__in=prodi_users, kategori='PENELITIAN').order_by('-created_at')
    elif request.user.role == 'DEKAN':
        fakultas_users = CustomUser.objects.filter(fakultas=request.user.fakultas)
        kegiatans = Kegiatan.objects.filter(dosen__in=fakultas_users, kategori='PENELITIAN').order_by('-created_at')
    else:
        kegiatans = Kegiatan.objects.none()
        
    return render(request, 'kegiatan/penelitian_list.html', {'kegiatans': kegiatans})

@login_required
def pengabdian_list(request):
    if request.user.role == 'DOSEN':
        kegiatans = Kegiatan.objects.filter(dosen=request.user, kategori='PENGABDIAN').order_by('-created_at')
    elif request.user.role == 'KAPRODI':
        prodi_users = CustomUser.objects.filter(prodi=request.user.prodi)
        kegiatans = Kegiatan.objects.filter(dosen__in=prodi_users, kategori='PENGABDIAN').order_by('-created_at')
    elif request.user.role == 'DEKAN':
        fakultas_users = CustomUser.objects.filter(fakultas=request.user.fakultas)
        kegiatans = Kegiatan.objects.filter(dosen__in=fakultas_users, kategori='PENGABDIAN').order_by('-created_at')
    else:
        kegiatans = Kegiatan.objects.none()
        
    return render(request, 'kegiatan/pengabdian_list.html', {'kegiatans': kegiatans})

