from django.db import models
from django.utils import timezone
import datetime




class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def test_was_published_recently_with_old_question(self):
    
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
   
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
# Define custom permissions
# class Meta:
#     permissions = [
#         ("can_create_question", "Can create question"),
#         ("can_modify_question", "Can modify question"),
#     ]

# this in views.py:
# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import PermissionDenied

# @login_required
# def create_question(request):
#     if not request.user.has_perm('app_name.can_create_question'):
#         raise PermissionDenied
    

# @login_required
# def modify_question(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if not request.user.has_perm('app_name.can_modify_question') or request.user != question.owner:
#         raise PermissionDenied
   
