from django.contrib import admin
from .models import Poll, Option
# Register your models here.

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
	list_display = ('question', 'pub_date')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
	list_display = ('poll', 'option_text', 'votes')