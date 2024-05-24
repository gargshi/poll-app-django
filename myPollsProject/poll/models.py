from django.db import models
from datetime import datetime
# from django.contrib.auth import User

# Create your models here.
class Poll(models.Model):
	question = models.CharField(max_length=250)
	created_by = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING, default=None)
	is_anonymous = models.BooleanField(default=False)
	pub_date = models.DateTimeField('date published', default=datetime.now)

	def __str__(self):
		return self.question
	
	class Meta:
		verbose_name_plural = "Polls"
		db_table = "polls"

class Option(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING)
	option_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.option_text
	
	class Meta:
		verbose_name_plural = "Options"
		db_table = "options"