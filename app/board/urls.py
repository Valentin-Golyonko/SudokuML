from django.urls import path

from app.board.views import SudokuView, AllBoardsView

urlpatterns = [
    path(
        "sudoku/<int:board_id>/",
        SudokuView.as_view(),
        name="sudoku",
    ),
    path(
        "boards/<int:difficulty>/",
        AllBoardsView.as_view(),
        name="boards",
    ),
]
