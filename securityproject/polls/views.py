from django.shortcuts import render
from .models import Choice, Question
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone


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
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        #choice_id = request.POST['choice']
        #with connection.cursor() as cursor:
            #cursor.execute("UPDATE polls_choice SET votes = votes + 100 WHERE id = %s", [choice_id])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
# fix to the SQL injection
# from django import forms

#class VoteForm(forms.Form):
#    choice = forms.ModelChoiceField(queryset=Choice.objects.all(), widget=forms.RadioSelect)

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
