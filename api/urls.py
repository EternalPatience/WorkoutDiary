from django.urls import path

from main.models import Exercise
from .views import WorkoutDetailView, workouts, setdescription

urlpatterns = [
    path('workouts/<int:workout_pk>/<int:exercise_id>/', setdescription),
    path('workouts/<int:pk>/', WorkoutDetailView.as_view()),
    path('workouts/', workouts),
]
