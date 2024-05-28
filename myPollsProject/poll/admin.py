from django.contrib import admin
from .models import Poll, Option, Vote
# Register your models here.

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
	list_display = ('question', 'pub_date','created_by','is_anonymous')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	list_display = ('poll', 'option_text', 'votes')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
	list_display = ('user', 'poll', 'option', 'voted_on')