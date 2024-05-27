from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db import connection
import logging

from .models import Choice, Question

# Set up logging
logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)  # Safe ORM query
        # Log the voting attempt
        logger.info(f"User {request.user.id} voting for choice_id: {choice_id} in question_id: {question_id}")

        # Vulnerable SQL query (SQL Injection)
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE polls_choice SET votes = votes + 1 WHERE id = {choice_id}")
    except (KeyError, Choice.DoesNotExist) as e:
        # Log the error
        logger.error(f"Error recording vote: {e}")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# The following sections should be uncommented and used for the forms-based approach if needed
# from django import forms
#
# class VoteForm(forms.Form):
#     choice = forms.ModelChoiceField(queryset=Choice.objects.all(), widget=forms.RadioSelect)
#
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == 'POST':
#         form = VoteForm(request.POST)
#         if form.is_valid():
#             selected_choice = form.cleaned_data['choice']
#             selected_choice.votes += 1
#             selected_choice.save()
#             return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
#     else:
#         form = VoteForm()
#     return render(request, 'polls/detail.html', {'question': question, 'form': form})

# Secure fix for the SQL injection issue
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         choice_id = request.POST['choice']
#         selected_choice = question.choice_set.get(pk=choice_id)  # Safe ORM query
#         # Log the voting attempt
#         logger.info(f"User {request.user.id} voting for choice_id: {choice_id} in question_id: {question_id}")
#         
#         # Safe parameterized query
#         with connection.cursor() as cursor:
#             cursor.execute("UPDATE polls_choice SET votes = votes + 1 WHERE id = %s", [choice_id])
#     except (KeyError, Choice.DoesNotExist) as e:
#         # Log the error
#         logger.error(f"Error recording vote: {e}")
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing with POST data.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
