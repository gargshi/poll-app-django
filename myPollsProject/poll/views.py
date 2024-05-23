from django.shortcuts import redirect, render
from django.db.models import Sum,F
from .models import Poll, Option

# Create your views here.
def index(request):
	return render(request,'index.html')

def createPoll(request):
	return render(request,'createPoll.html')

def savePoll(request):
	if request.method == 'POST':
		# print(request.POST)
		question = request.POST['question']
		# print(question)
		poll = Poll.objects.create(question=question)
		for i in request.POST.keys():
			if i.startswith('option_text'):
				print(i)
				option_text = request.POST[i]
				Option.objects.create(poll=poll, option_text=option_text)

	return redirect('index')

def listPolls(request):
	# if search is used
	if request.method == 'POST':
		query=request.POST['search']		
		# polls = Poll.objects.filter(question__contains=query)
		polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','c').filter(poll__question__contains=query).all()
		# return redirect('listPolls',query=query,polls=polls)
		return render(request,'viewPolls.html',{'polls':polls,'query':query})
	# if search is not used
	polls = Option.objects.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','poll__pub_date','c')
	return render(request,'viewPolls.html',{'polls':polls})

def displayPoll(request,poll_id):
	poll = Poll.objects.get(id=poll_id)
	options = Option.objects.filter(poll=poll)
	poll_op = options.values('poll').annotate(c=Sum('votes')).values('poll__id','poll__question','c')[0]
	# print(poll_op)
	return render(request,'displayPoll.html',{'poll_op':poll_op,'poll':poll,'options':options})

def castVote(request):
	if request.method == 'POST':
		# print(request.POST)		
		option_id = request.POST['vote']
		poll=Option.objects.get(id=option_id).poll
		Option.objects.filter(id=option_id).update(votes=F('votes')+1)
	return redirect('listPolls')