from django.urls import path

from app.solver.views import SolveView

urlpatterns = [
    path("solve/<int:board_id>/", SolveView.as_view(), name="solve"),
]
