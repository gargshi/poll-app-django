from django.shortcuts import redirect, render
from django.db.models import Sum,F
from .models import Poll, Option
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
	return render(request,'index.html')

def createPoll(request):
	return render(request,'createPoll.html')

def savePoll(request):
	if request.method == 'POST' and request.user.is_authenticated:
		print(request.POST)
		# dum='2024-05-20T20:52'
		end_time=request.POST.get('poll_end_time')
		# end_time=dum
		end_time=datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
		# print(end_time)
		question = request.POST['question']
		make_anonymous = request.POST.get('anonymous-poll')
		if make_anonymous and make_anonymous == 'on':
			make_anonymous = True
		else:
			make_anonymous = False
		# print(make_anonymous)
		print(question)
		poll = Poll.objects.create(question=question, created_by=request.user, is_anonymous=make_anonymous, poll_end=end_time)
		for i in request.POST.keys():
			if i.startswith('option_text'):
				print(i)
				option_text = request.POST[i]
				Option.objects.create(poll=poll, option_text=option_text)
		messages.info(request, 'Poll created successfully')
		return redirect('listPolls')
	else:
		messages.info(request, 'Poll creation failed as you are not logged in')
	return redirect('listPolls')

def listPolls(request):
	# if search is used
	if request.method == 'POST':
		query=request.POST['search']
		made_by_me = False		
		polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','c','poll__is_anonymous','poll__created_by__username','poll__poll_end').filter(poll__question__contains=query).all()
		if request.user.is_authenticated:
			made_by_me = request.POST.get('made_by_me')
			if made_by_me and made_by_me == 'on':
				polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','c','poll__is_anonymous','poll__created_by__username','poll__poll_end').filter(poll__question__contains=query,poll__created_by=request.user).all()	
		else:
			polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','c','poll__is_anonymous','poll__created_by__username','poll__poll_end').filter(poll__question__contains=query).all()		
		return render(request,'viewPolls.html',{'polls':polls,'query':query,'made_by_me':made_by_me})
	# if search is not used
	polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','poll__is_anonymous','poll__created_by__username','poll__poll_end','c')
	return render(request,'viewPolls.html',{'polls':polls})

def displayPoll(request,poll_id):
	poll = Poll.objects.get(id=poll_id)
	options = Option.objects.filter(poll=poll)
	poll_op = options.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','c')[0]
	# print(poll_op)
	return render(request,'displayPoll.html',{'poll_op':poll_op,'poll':poll,'options':options})

def castVote(request):
	if request.method == 'POST' and request.user.is_authenticated:
		# print(request.POST)		
		option_id = request.POST['vote']
		poll=Option.objects.get(id=option_id).poll
		Option.objects.filter(id=option_id).update(votes=F('votes')+1)
		messages.success(request, f'Yay! Your Vote was Cast Successfully, thank you {request.user.username}.')
	else:
		messages.warning(request, 'Vote cannot be cast due to some error or you are not logged in. Please contact the administrator.')
	return redirect('listPolls')