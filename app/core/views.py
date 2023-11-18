import asyncio

from django.http import JsonResponse
from django.views import View

from app.core.view_logic.solve_vl import SolveVL
from app.core.view_logic.sudoku_vl import SudokuVL


class SudokuView(View):
    async def get(self, request, *args, **kwargs):
        await asyncio.sleep(0.3)
        game_data = await SudokuVL.get_sudoku_game()
        return JsonResponse(
            data={"data": game_data},
            safe=True,
            json_dumps_params={"ensure_ascii": False},
        )


class SolveView(View):
    async def get(self, request, *args, **kwargs):
        solved = await SolveVL.solve()
        return JsonResponse(
            data={"solved": solved},
            safe=True,
            json_dumps_params={"ensure_ascii": False},
        )
