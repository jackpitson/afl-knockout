from django.contrib import admin
from .models import Player, Team, Round, Match, Tip


@admin.action(description="Process selected round")
def process_round(modeladmin, request, queryset):

    for round_obj in queryset:

        matches = Match.objects.filter(round=round_obj)
        tips = Tip.objects.filter(round=round_obj)

        # Safety check – make sure every match has a winner
        if matches.filter(winner=None).exists():
            modeladmin.message_user(
                request,
                "Cannot process round. Some matches do not have a winner yet."
            )
            return

        for tip in tips:

            match = matches.filter(team1=tip.team).first() or matches.filter(team2=tip.team).first()

            if match and match.winner != tip.team:
                tip.player.eliminated = True
                tip.player.save()

        round_obj.completed = True
        round_obj.save()


class TipInline(admin.TabularInline):
    model = Tip
    extra = 0
    readonly_fields = ["player", "team"]


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("number", "completed", "lockout_time")
    actions = [process_round]
    inlines = [TipInline]


class TipAdmin(admin.ModelAdmin):
    list_display = ["player", "round", "team", "margin"]
    list_filter = ["round"]


admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Tip, TipAdmin)