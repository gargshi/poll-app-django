from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
	path('contact/',views.contact,name="contact"),
	path('createPoll/',views.createPoll,name="createPoll"),
	path('savePoll/',views.savePoll,name="savePoll"),
	path('viewPolls/',views.listPolls,name="listPolls"),
	path('displayPoll/<int:poll_id>/',views.displayPoll,name="displayPoll"),
	path('votePoll/',views.castVote,name="votePoll"),
	path('deletePoll/<int:poll_id>/',views.deletePoll,name="deletePoll"),
	# path('searchPolls/',views.searchPolls,name="searchPolls"),
]
