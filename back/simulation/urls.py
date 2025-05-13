from django.urls import path
from .views import SimulationView, RunFullSimulationView, StartSimulationView

urlpatterns = [
    path('', SimulationView.as_view(), name='simulation'),
    path('start/', StartSimulationView.as_view(), name='start_simulation'),
    path('run/', RunFullSimulationView.as_view(), name='run_simulation'),
]