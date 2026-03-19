from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.utils import timezone

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

    # Get or create player record
    player, created = Player.objects.get_or_create(user=request.user)

    # Get current round (first unfinished round)
    current_round = Round.objects.filter(completed=False).first()
    

    matches = Match.objects.filter(round=current_round)

    # If eliminated show eliminated page
    if player.eliminated:
        return render(request, "eliminated.html")

    # Lock tips after deadline
    if timezone.now() > current_round.lockout_time:
        return render(request, "tips_locked.html", {"round": current_round})

    # Get teams player has already used
    used_team_ids = set(
        Tip.objects.filter(player=player).values_list("team_id", flat=True)
    )

    # Mark teams as used so template can disable them
    for match in matches:
        match.team1_used = match.team1.id in used_team_ids
        match.team2_used = match.team2.id in used_team_ids

    if request.method == "POST":

        team_id = request.POST.get("team")
        margin = request.POST.get("margin")

        if not team_id:
            messages.error(request, "You must select a team.")
            return redirect("submit_tip")

        team = Team.objects.get(id=team_id)

        # Prevent picking same team twice
        if team.id in used_team_ids:
            messages.error(request, "You have already picked this team.")
            return redirect("submit_tip")

        # Allow tip change before lockout
        tip, created = Tip.objects.update_or_create(
        player=player,
        round=current_round,
        defaults={
        "team": team,
        "margin": margin
    }
)

        messages.success(request, "Tip submitted successfully!")
        return redirect("submit_tip")

    return render(request, "submit_tip.html", {
        "matches": matches,
        "round": current_round,
    })
    

@login_required
def leaderboard(request):
    players = Player.objects.select_related("user").all()
    rounds = Round.objects.order_by("number")

    alive_players = players.filter(eliminated=False).count()
    total_players = players.count()

    tips = Tip.objects.select_related("team", "round", "player")
    matches = Match.objects.select_related("winner")

    # tip lookup

    rows = []

    for player in players:
        player_row = {
            "player": player,
            "tips": []
        }

        for round in rounds:
            tip = tips.filter(player=player, round=round).first()
            player_row["tips"].append({
                "round": round,
                "tip": tip
            })

        rows.append(player_row)

    # winner lookup
    winner_lookup = {}

    for match in matches:
     if match.winner:
        winner_lookup[match.team1_id] = match.winner_id
        winner_lookup[match.team2_id] = match.winner_id

    current_round = Round.objects.filter(completed=False).first()

    round_locked = False
    if current_round and timezone.now() > current_round.lockout_time:
        round_locked = True

    return render(request, "leaderboard.html", {
        "players": players,
        "rounds": rounds,
        "rows": rows,
        "winner_lookup": winner_lookup,
        "alive_players": alive_players,
        "total_players": total_players,
        "current_round": current_round,
        "round_locked": round_locked,
    })