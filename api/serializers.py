from rest_framework import serializers

from main.models import Workout, Exercise, SetDescription


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ('__all__')


class WorkoutDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('__all__')


class SetDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SetDescription
        fields = ('__all__')
