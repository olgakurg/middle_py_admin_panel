from django.urls import path

from . import views

urlpatterns = [
    path('movies/', views.MoviesListAPIView.as_view()),
    path('movies/<uuid:pk>/', views.MoviesDetailApi.as_view()),
    #path('genres', views.GenresListAPIView.as_view()),
] 