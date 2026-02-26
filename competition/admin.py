from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Team, Round, Match, Player, Tip

admin.site.register(Team)
admin.site.register(Round)
admin.site.register(Match)
admin.site.register(Player)
admin.site.register(Tip)