from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from app.board.crud.crud_board import CRUDBoard
from app.board.view_logic.sudoku_vl import SudokuVL


class SudokuView(View):
    async def get(self, request, *args, **kwargs):
        is_ok, out_data, detail = await SudokuVL.get_sudoku_game(kwargs.get("board_id"))
        return JsonResponse(
            data={
                "data": out_data,
                "detail": detail,
            },
            safe=True,
            json_dumps_params={"ensure_ascii": False},
            status=HTTPStatus.OK if is_ok else HTTPStatus.BAD_REQUEST,
        )


class AllBoardsView(View):
    async def get(self, request, *args, **kwargs):
        boards_ids = await CRUDBoard.boards_ids(kwargs.get("difficulty"))

        return JsonResponse(
            data={
                "data": boards_ids,
                "detail": "",
            },
            safe=True,
            json_dumps_params={"ensure_ascii": False},
            status=HTTPStatus.OK,
        )
