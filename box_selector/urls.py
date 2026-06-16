from django.urls import path
from .views import BoxRecommendationAPI, frontend_view

urlpatterns = [
    path('', frontend_view, name='frontend'),
    path('api/v1/recommend-box/', BoxRecommendationAPI.as_view(), name='recommend_box_api'),
]
