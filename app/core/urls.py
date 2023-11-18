from django.urls import path

from app.core.views import SudokuView, SolveView

urlpatterns = [
    path("sudoku/", SudokuView.as_view(), name="sudoku"),
    path("solve/", SolveView.as_view(), name="solve"),
]
