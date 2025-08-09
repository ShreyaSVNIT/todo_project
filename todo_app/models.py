from django.db import models
from django.contrib.auth.models import User
from datetime import date

'''
Model is a python class that defines structure of database.
it is linked to the default User model of django with foreign key.
django's job to create the table for you.
'''

'''
each task:
1) belongs to a user
2) has title 
3) has description
4) timestamp of when task was SAVED
5) completed (will get toggled)'''

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=date.today)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
