from django.urls import path

from app.board.views import SudokuView

urlpatterns = [
    path("sudoku/", SudokuView.as_view(), name="sudoku"),
]
