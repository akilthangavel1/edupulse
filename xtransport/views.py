from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TransportFee
from .forms import TransportFeeForm

@login_required
def transport_fee_list(request):
    fees = TransportFee.objects.all()
    return render(request, 'xtransport/transport_fee_list.html', {'fees': fees})

@login_required
def transport_fee_create(request):
    if request.method == 'POST':
        form = TransportFeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transport fee entry created successfully!')
            return redirect('xtransport:transport_fee_list')
    else:
        form = TransportFeeForm()
    return render(request, 'xtransport/transport_fee_form.html', {'form': form})

@login_required
def transport_fee_edit(request, pk):
    fee = get_object_or_404(TransportFee, pk=pk)
    if request.method == 'POST':
        form = TransportFeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transport fee entry updated successfully!')
            return redirect('xtransport:transport_fee_list')
    else:
        form = TransportFeeForm(instance=fee)
    return render(request, 'xtransport/transport_fee_form.html', {'form': form})
