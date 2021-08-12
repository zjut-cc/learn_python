from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # 例如：/polls/
    path('', views.IndexView.as_view(), name = 'index'),

    # 例如：/polls/5
    # path('<int:question_id>/', views.detail, name = 'detail'),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    # 例如：/polls/5/results
    path('<int:pk>/results/', views.ResultsView.as_view(), name = 'results'),

    # 例如：/polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name = 'vote'),

    # 添加新的单词'specifics'
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
]

