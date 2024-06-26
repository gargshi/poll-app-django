from django.shortcuts import redirect, render
from django.db.models import Sum,F
from .models import Poll, Option, Vote, Contact
from django.contrib import messages
import datetime
import pytz

utc=pytz.timezone('UTC')

# Create your views here.
def index(request):
	return render(request,'index.html')

def contact(request):
	if request.method == 'POST' and '/contact/' in request.headers['Referer']:
		name=request.POST['name']
		email=request.POST['email']
		message=request.POST['message']
		subject=request.POST['subject']
		category=request.POST['category']
		if email == '' or not email:
			messages.error(request, 'Please enter valid email address.')
		if message == '' or not message:
			messages.error(request, 'Please enter a message.')
		else:
			Contact.objects.create(name=name, email=email, subject=subject, message=message, category=category)
			messages.success(request, 'Thank you for contacting us. We will get back to you soon.')		
	return render(request,'contact.html')

def createPoll(request):
	return render(request,'createPoll.html')

def savePoll(request):
	if request.method == 'POST' and request.user.is_authenticated:
		print(request.POST)
		# dum='2024-05-20T20:52'
		end_time=request.POST.get('poll_end_time')
		# end_time=dum
		end_time=datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M') if end_time else datetime.datetime.now()+datetime.timedelta(hours=1)
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
	polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','poll__is_anonymous','poll__created_by__username','poll__poll_end','c').filter(poll__poll_end__gt = datetime.datetime.now()).order_by('-poll__pub_date').all()
	# check if polls are already voted
	for poll in polls:
		if poll['poll__poll_end'] > utc.localize(datetime.datetime.now()):
			poll['time_left'] = poll['poll__poll_end'] - utc.localize(datetime.datetime.now())
			poll['is_active'] = True
		else:
			poll['is_active'] = False
		if request.user.is_authenticated:
			vote = Vote.objects.filter(user=request.user, poll=poll['poll__id'])
			if vote:
				poll['voted'] = True
			else:
				poll['voted'] = False
	# if search is used
	if request.method == 'POST':
		query=request.POST['search']
		made_by_me = False				
		# polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','c','poll__is_anonymous','poll__created_by__username','poll__poll_end').filter(poll__question__icontains=query).order_by('-poll__pub_date').all()
		polls=polls.filter(poll__question__icontains=query).order_by('-poll__pub_date').all()
		if request.user.is_authenticated:
			made_by_me = request.POST.get('made_by_me')
			if made_by_me and made_by_me == 'on':
				polls = polls.filter(poll__created_by=request.user).order_by('-poll__pub_date').all()		
		return render(request,'viewPolls.html',{'polls':polls,'query':query,'made_by_me':made_by_me})	
	return render(request,'viewPolls.html',{'polls':polls})

def displayPoll(request,poll_id):
	poll = Poll.objects.get(id=poll_id)
	options = Option.objects.filter(poll=poll)
	already_voted = False
	vote = None
	if request.user.is_authenticated:
		vote = Vote.objects.filter(user=request.user, poll=poll)
		vote = vote if vote else None
		already_voted = False
		if vote:
			messages.warning(request, 'You have already voted for this poll on '+vote[0].voted_on.strftime("%Y-%m-%d %H:%M"))
			already_voted = True	
		poll_op = options.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','c','poll__created_by__username')[0]
		return render(request,'displayPoll.html',{'poll_op':poll_op,'poll':poll,'options':options,'already_voted':already_voted,'vote':vote[0] if vote else None})
	else:
		poll_op = options.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','c','poll__created_by__username')[0]
		return render(request,'displayPoll.html',{'poll_op':poll_op,'poll':poll,'options':options})

def castVote(request):
	if request.method == 'POST' and request.user.is_authenticated:
		# print(request.POST)		
		option_id = request.POST['vote']
		poll=Option.objects.get(id=option_id).poll
		vote = Vote.objects.filter(user=request.user, poll=poll)
		if vote:
			messages.warning(request, 'You have already voted for this poll')			
		else:
			Vote.objects.create(user=request.user, poll=poll, option=Option.objects.get(id=option_id))
			Option.objects.filter(id=option_id).update(votes=F('votes')+1)
			messages.success(request, f'Yay! Your Vote was Cast Successfully, thank you {request.user.username}.')
	else:
		messages.warning(request, 'Vote cannot be cast due to some error or you are not logged in. Please contact the administrator.')
	return redirect('listPolls')

def deletePoll(request,poll_id):
	if request.user.is_authenticated:
		poll = Poll.objects.get(id=poll_id)
		options = Option.objects.filter(poll=poll)
		if request.user == poll.created_by:
			for i in options:
				i.delete()
			poll.delete()
			messages.success(request, 'Poll deleted successfully')
		else:
			messages.warning(request, 'You are not authorized to delete this poll')
	else:
		messages.info(request, 'Poll deletion failed as you are not logged in')		
	return redirect('listPolls')