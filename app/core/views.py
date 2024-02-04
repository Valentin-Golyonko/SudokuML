import asyncio
from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from app.core.view_logic.sudoku_vl import SudokuVL


class SudokuView(View):
    async def get(self, request, *args, **kwargs):
        await asyncio.sleep(0.3)
        game_data = await SudokuVL.get_sudoku_game()
        return JsonResponse(
            data={"data": game_data},
            safe=True,
            json_dumps_params={"ensure_ascii": False},
            status=HTTPStatus.OK,
        )
