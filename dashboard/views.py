from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from .models import KsebCds, CdsDailyData, CdsPreset
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def round_to_two(value):
    """Helper function to round a value to 2 decimal places."""
    return round(value, 2)

@login_required
def dashboard(request):
    # Fetch parent categories
    circle = KsebCds.objects.get(title="Kozhikode", category=KsebCds.CategoryChoices.CIRCLE)
    division = KsebCds.objects.filter(category=KsebCds.CategoryChoices.DIVISION, parent=circle)

    balussery = KsebCds.objects.get(title="Balussery", parent=circle, category=KsebCds.CategoryChoices.DIVISION)
    kozhikode = KsebCds.objects.get(title="Kozhikode", parent=circle, category=KsebCds.CategoryChoices.DIVISION)
    feroke = KsebCds.objects.get(title="Feroke", parent=circle, category=KsebCds.CategoryChoices.DIVISION)

    # Fetch sections for each division
    circle_sections = KsebCds.objects.filter(category=KsebCds.CategoryChoices.SECTION, parent__parent=circle)
    balussery_sections = KsebCds.objects.filter(parent=balussery, category=KsebCds.CategoryChoices.SECTION)
    kozhikode_sections = KsebCds.objects.filter(parent=kozhikode, category=KsebCds.CategoryChoices.SECTION)
    feroke_sections = KsebCds.objects.filter(parent=feroke, category=KsebCds.CategoryChoices.SECTION)

    # DailyData totals
    circle_total = round_to_two(CdsDailyData.objects.filter(section__in=circle_sections).aggregate(total=Sum('value'))['total'] or 0)
    Balussery_total = round_to_two(CdsDailyData.objects.filter(section__in=balussery_sections).aggregate(total=Sum('value'))['total'] or 0)
    Kozhikode_total = round_to_two(CdsDailyData.objects.filter(section__in=kozhikode_sections).aggregate(total=Sum('value'))['total'] or 0)
    Feroke_total = round_to_two(CdsDailyData.objects.filter(section__in=feroke_sections).aggregate(total=Sum('value'))['total'] or 0)

    # Calculate totals for each section
    section_totals = {}
    for section in circle_sections:
        section_total_value = round_to_two(CdsDailyData.objects.filter(section=section).aggregate(total=Sum('value'))['total'] or 0)
        section_actual_total = round_to_two(CdsPreset.objects.filter(section=section).aggregate(total_actual_qty=Sum('actual_qty'))['total_actual_qty'] or 0)
        section_completion_percentage = round_to_two((section_total_value / section_actual_total) * 100) if section_actual_total else 0
        section_totals[section.title] = {
            'total_value': section_total_value,
            'completion_percentage': section_completion_percentage
        }

    # Actual_qty totals
    circle_actual_total = round_to_two(CdsPreset.objects.filter(section__in=circle_sections).aggregate(total_actual_qty=Sum('actual_qty'))['total_actual_qty'] or 0)
    Balussery_actual_total = round_to_two(CdsPreset.objects.filter(section__in=balussery_sections).aggregate(total_actual_qty=Sum("actual_qty"))['total_actual_qty'] or 0)
    Kozhikode_actual_total = round_to_two(CdsPreset.objects.filter(section__in=kozhikode_sections).aggregate(total_actual_qty=Sum("actual_qty"))['total_actual_qty'] or 0)
    Feroke_actual_total = round_to_two(CdsPreset.objects.filter(section__in=feroke_sections).aggregate(total_actual_qty=Sum("actual_qty"))['total_actual_qty'] or 0)

    # qty_ulccs totals
    circle_qty_ulccs_total = round_to_two(CdsPreset.objects.filter(section__in=circle_sections).aggregate(total_qty_ulccs=Sum("qty_ulccs"))['total_qty_ulccs'] or 0)
    Balussery_qty_ulccs_total = round_to_two(CdsPreset.objects.filter(section__in=balussery_sections).aggregate(total_qty_ulccs=Sum("qty_ulccs"))['total_qty_ulccs'] or 0)
    Kozhikode_qty_ulccs_total = round_to_two(CdsPreset.objects.filter(section__in=kozhikode_sections).aggregate(total_qty_ulccs=Sum("qty_ulccs"))['total_qty_ulccs'] or 0)
    Feroke_qty_ulccs_total = round_to_two(CdsPreset.objects.filter(section__in=feroke_sections).aggregate(total_qty_ulccs=Sum("qty_ulccs"))['total_qty_ulccs'] or 0)

    # Percentages (handle zero safely)
    circle_total_percentage = round_to_two((circle_total / circle_actual_total) * 100) if circle_actual_total else 0
    Balussery_total_percentage = round_to_two((Balussery_total / circle_actual_total) * 100) if circle_actual_total else 0
    Kozhikode_total_percentage = round_to_two((Kozhikode_total / circle_actual_total) * 100) if circle_actual_total else 0
    Feroke_total_percentage = round_to_two((Feroke_total / circle_actual_total) * 100) if circle_actual_total else 0

    # Context
    context = {
        'circle': circle,
        'division': division,
        'Balussery': balussery,
        'Kozhikode': kozhikode,
        'Feroke': feroke,
        'circle_sections': circle_sections,
        'balussery_sections': balussery_sections,
        'kozhikode_sections': kozhikode_sections,
        'feroke_sections': feroke_sections,
        'circle_total': circle_total,
        'Balussery_total': Balussery_total,
        'Kozhikode_total': Kozhikode_total,
        'Feroke_total': Feroke_total,
        'circle_actual_total': circle_actual_total,
        'Balussery_actual_total': Balussery_actual_total,
        'Kozhikode_actual_total': Kozhikode_actual_total,
        'Feroke_actual_total': Feroke_actual_total,
        'circle_total_percentage': circle_total_percentage,
        'Balussery_total_percentage': Balussery_total_percentage,
        'Kozhikode_total_percentage': Kozhikode_total_percentage,
        'Feroke_total_percentage': Feroke_total_percentage,
        'circle_qty_ulccs_total': circle_qty_ulccs_total,
        'Balussery_qty_ulccs_total': Balussery_qty_ulccs_total,
        'Kozhikode_qty_ulccs_total': Kozhikode_qty_ulccs_total,
        'Feroke_qty_ulccs_total': Feroke_qty_ulccs_total,
        'section_totals': section_totals,
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Attempting login for username: {username}")  # Debug log

        user = authenticate(request, username=username, password=password)
        if user:
            print("Authentication successful.")  # Debug log
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard on success
        else:
            print("Authentication failed.")  # Debug log
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def import_csv(request):
    # Your logic here
    return render(request, 'import_csv.html')



@login_required
def get_sections(request, division_id):
    try:
        division = KsebCds.objects.get(id=division_id, category=KsebCds.CategoryChoices.DIVISION)
        sections = KsebCds.objects.filter(parent=division, category=KsebCds.CategoryChoices.SECTION)

        section_data = []
        for section in sections:
            total_value = round_to_two(CdsDailyData.objects.filter(section=section).aggregate(total=Sum('value'))['total'] or 0)
            actual_qty = round_to_two(CdsPreset.objects.filter(section=section).aggregate(total_actual_qty=Sum('actual_qty'))['total_actual_qty'] or 0)
            qty_ulccs = round_to_two(CdsPreset.objects.filter(section=section).aggregate(total_qty_ulccs=Sum('qty_ulccs'))['total_qty_ulccs'] or 0)
            completion_percentage = round_to_two((total_value / actual_qty) * 100) if actual_qty else 0

            section_data.append({
                'title': section.title,
                'total_value': total_value,
                'actual_qty': actual_qty,
                'qty_ulccs': qty_ulccs,
                'completion_percentage': completion_percentage,
            })

        return JsonResponse({'sections': section_data})
    except KsebCds.DoesNotExist:
        return JsonResponse({'sections': []})
