from django.contrib import admin
from .models import Profile, Competitor, Micromatch, Announsment, Tournament, TournamentGroup

class TournamentAdmin(admin.ModelAdmin):
    fields = ('tour_id', 'date', 'played_with_matrix')
    readonly_fields = ('tour_id', 'date')  
    search_fields = ('tour_id',)

class CompetitorAdmin(admin.ModelAdmin):
    search_fields = ('player_id', 'name')
    list_filter = ('group_id', 'gender')

class MicromatchAdmin(admin.ModelAdmin):
    search_fields = ('created_at',)
    list_filter = ('tournament__tour_id',)

admin.site.register(Profile)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Micromatch, MicromatchAdmin)
admin.site.register(Announsment)
admin.site.register(TournamentGroup)


