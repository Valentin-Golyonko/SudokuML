from django.urls import path

from app.board.views import SudokuView

urlpatterns = [
    path("sudoku/<int:difficulty>/<int:current>/", SudokuView.as_view(), name="sudoku"),
]
