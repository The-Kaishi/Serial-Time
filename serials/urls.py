from django.urls import path

from . import views

urlpatterns = [
    path('', views.SerialsView.as_view()),
    path('filter/', views.FilterSerialsView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path('json-filter/', views.JsonFilterSerialsView.as_view(), name='json_filter'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", views.SerialDetailView.as_view(), name='serial_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', views.ActorView.as_view(), name='actor_detail'),
]
