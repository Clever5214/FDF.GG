from django.db import models

class match(models.Model):
	title = models.CharField(max_length = 20)
	nick_name = models.CharField(max_length = 15)
	content = models.TextField()
	password = models.CharField(max_length=120)
	created_at = models.DateTimeField(auto_now_add=True)
    
	def __str__(self):
		return self.title
