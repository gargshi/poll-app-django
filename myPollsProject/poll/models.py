from django.db import models
from datetime import datetime

# Create your models here.
class Poll(models.Model):
	question = models.CharField(max_length=250)
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