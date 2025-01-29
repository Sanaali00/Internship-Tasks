from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Record
from .forms import RecordForm

@login_required
def record_list(request):
    records = Record.objects.filter(created_by=request.user)
    return render(request, 'crid/record_list.html', {'records': records})

@login_required
def record_detail(request, pk):
    record = get_object_or_404(Record, pk=pk, created_by=request.user)
    return render(request, 'crid/record_detail.html', {'record': record})

@login_required
def record_create(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            return redirect('record_list')
    else:
        form = RecordForm()
    return render(request, 'crid/record_form.html', {'form': form})

@login_required
def record_update(request, pk):
    record = get_object_or_404(Record, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = RecordForm(instance=record)
    return render(request, 'crid/record_form.html', {'form': form})

@login_required
def record_delete(request, pk):
    record = get_object_or_404(Record, pk=pk, created_by=request.user)
    record.delete()
    return redirect('record_list')