from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Robot, Trash, BASE_X, BASE_Y, run_simulation, start_simulation
from .serializers import RobotSerializer, TrashSerializer


class SimulationView(APIView):
    def get(self, request):
        robots = Robot.objects.all()
        trash = Trash.objects.all()
        return Response({
            'robots': RobotSerializer(robots, many=True).data,
            'trash': TrashSerializer(trash, many=True).data,
            'base': { "x": BASE_X, "y": BASE_Y } 
        })

    def post(self, request):
        for robot in Robot.objects.all():
            robot.randomly()
        return Response({"message": "One turn finished."}, status=status.HTTP_200_OK)

class RunFullSimulationView(APIView):
    def post(self, request):
        run_simulation()
        return Response({"message": "No trash left. Simulation complete"}, status=status.HTTP_200_OK)

class StartSimulationView(APIView):
    def post(self, request):
        start_simulation()
        return Response({"message": "Start"}, status=status.HTTP_200_OK)
