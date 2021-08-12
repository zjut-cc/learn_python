from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.template import loader

from .models import Choice, Question

# Create your views here.

# 注意函数的参数
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        '''Return the last five published questions.'''
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def result(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ','.join([q.question_text for q in latest_question_list])
#     # template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list':latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#         abc="ahsdfoashd"
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist.")
#     return render(request, "polls/detail.html", {'question':question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


# def runoob(request):
#     # context = {}
#     # context['hello'] = 'Hello World!'
#     # return HttpResponse("Hello, world!")
#     # view_name = "菜鸟教程"
#     views_list = ["菜鸟教程1", "菜鸟教程2", "菜鸟教程3"]
#     return render(request, 'runoob.html', {"views_list":views_list})




