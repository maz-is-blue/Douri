from django.shortcuts import render

from .models import TeamMember


def our_team(request):
    return render(request, 'our_team.html', {'team': TeamMember.objects.all()})
