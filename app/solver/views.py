from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from app.solver.view_logic.solve_vl import SolveVL


class SolveView(View):
    async def get(self, request, *args, **kwargs):
        is_ok, out_data, detail = await SolveVL.solve(kwargs.get("board_id"))
        return JsonResponse(
            data={"solved": out_data},
            safe=True,
            json_dumps_params={"ensure_ascii": False},
            status=HTTPStatus.OK if is_ok else HTTPStatus.BAD_REQUEST,
        )
