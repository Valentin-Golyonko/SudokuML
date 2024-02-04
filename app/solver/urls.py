from django.urls import path

from app.solver.views import SolveView

urlpatterns = [
    path("solve/", SolveView.as_view(), name="solve"),
]
