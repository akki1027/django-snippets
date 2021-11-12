# urls.pyファイルを新規作成

from django.urls import path
from snippets import views


urlpatterns = [
    path('<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
    path('<int:snippet_id>/edit', views.snippet_edit, name='snippet_edit'),
    path('new', views.snippet_new, name='snippet_new'),
]
