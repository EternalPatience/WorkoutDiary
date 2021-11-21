from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from main.models import Exercise, Workout, SetDescription
from .serializers import SetDescriptionSerializer, WorkoutSerializer, WorkoutDetailSerializer


@api_view(['GET'])
def workouts(request):
    if request.method == 'GET':
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)


class WorkoutDetailView(RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = WorkoutDetailSerializer


@api_view(['GET'])
def setdescription(request, workout_pk, exercise_id):
    if request.method == 'GET':
        sets = SetDescription.objects.filter(id=exercise_id)
        serializer = SetDescriptionSerializer(sets, many=True)
        return Response(serializer.data)
