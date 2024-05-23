from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
	path('createPoll/',views.createPoll,name="createPoll"),
	path('savePoll/',views.savePoll,name="savePoll"),
	path('viewPolls/',views.listPolls,name="listPolls"),
	path('displayPoll/<int:poll_id>/',views.displayPoll,name="displayPoll"),
	path('votePoll/',views.castVote,name="votePoll"),
	# path('searchPolls/',views.searchPolls,name="searchPolls"),
]
