from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Round, Match, Player, Tip, Team

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return redirect("submit_tip")
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('submit_tip')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def submit_tip(request):
    player, created = Player.objects.get_or_create(user=request.user)
    current_round = Round.objects.filter(completed=False).first()
    matches = Match.objects.filter(round=current_round)

    if player.eliminated:
        return render(request, 'eliminated.html')

    if request.method == "POST":
        team_id = request.POST.get('team')

        if not team_id:
            messages.error(request, "You must select a team.")
            return redirect('submit_tip')

        team = Team.objects.get(id=team_id)

        tip = Tip(
            player=player,
            round=current_round,
            team=team
        )

        try:
            tip.full_clean()
            tip.save()
            messages.success(request, "Tip submitted successfully!")
            return redirect('submit_tip')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('submit_tip')

    return render(request, 'submit_tip.html', {
        'matches': matches,
        'round': current_round,
    })