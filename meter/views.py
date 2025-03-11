import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import matplotlib.pyplot as plt
import io, base64
import datetime
from django.shortcuts import render, redirect
from .forms import TariffForm, MeterReadingForm
from .models import MeterReading, Tariff

def input_data(request):
    if request.method == "POST":
        meter_form = MeterReadingForm(request.POST)
        tariff_form = TariffForm(request.POST)

        if meter_form.is_valid():
            meter_form.save()

        if tariff_form.is_valid():  # ✅ Fix: Properly validate the form
            tariff_form.save()

        return redirect('dashboard')

    # ✅ Ensure new forms are created for the template
    meter_form = MeterReadingForm()
    tariff_form = TariffForm()
    return render(request, 'input.html', {'meter_form': meter_form, 'tariff_form': tariff_form})

def dashboard(request):
    readings = MeterReading.objects.all().order_by('date')
    tariff = Tariff.objects.last()
    
    if not readings.exists() or not tariff:
        return render(request, 'dashboard.html', {'error': "No data available."})

    dates = [reading.date for reading in readings]
    kwh = [reading.kwh_used for reading in readings]
    costs = [reading.kwh_used * tariff.price_per_kwh for reading in readings]

    # Matplotlib Plot
    plt.figure(figsize=(8, 5))
    plt.plot(dates, costs, marker='o', linestyle='-')
    plt.xlabel("Date")
    plt.ylabel("Cost (£)")
    plt.title("Energy Cost Over Time")
    plt.grid(True)

    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close()

    return render(request, 'dashboard.html', {'chart': encoded, 'readings': readings, 'tariff': tariff})
