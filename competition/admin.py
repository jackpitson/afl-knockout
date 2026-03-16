from django.contrib import admin
from .models import Player, Team, Round, Match, Tip 
from django.db import transaction

@admin.action(description="Process selected round")
def process_round(modeladmin, request, queryset):

    for round_obj in queryset:

        matches = Match.objects.filter(round=round_obj)
        tips = Tip.objects.filter(round=round_obj)

        winners = [m.winner for m in matches if m.winner]

        for tip in tips:
            if tip.team not in winners:
                player = tip.player
                player.eliminated = True
                player.save()

        round_obj.completed = True
        round_obj.save()

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("number", "completed", "lockout_time")
    actions = [process_round]

class TipInline(admin.TabularInline):
    model = Tip
    extra = 0
    readonly_fields = ["player", "team"]


class RoundAdmin(admin.ModelAdmin):
    inlines = [TipInline]

class TipAdmin(admin.ModelAdmin):
    list_display = ["player", "round", "team"]
    list_filter = ["round"]

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Tip, TipAdmin)
