from itertools import groupby

from django.shortcuts import render

from .models import AgendaFeatured, AgendaRecurring


def agenda(request):
    featured = AgendaFeatured.objects.filter(active=True).first()
    recurring = AgendaRecurring.objects.all()
    months = [
        {'month': month, 'items': list(items)}
        for month, items in groupby(recurring, key=lambda item: item.month)
    ]
    return render(
        request,
        'agenda/list.html',
        {'featured': featured, 'agenda_months': months},
    )
