from http import HTTPStatus

from django.http import JsonResponse
from django.views import View

from app.solver.view_logic.solve_vl import SolveVL


class SolveView(View):
    async def get(self, request, *args, **kwargs):
        solved = await SolveVL.solve()
        return JsonResponse(
            data={"solved": solved},
            safe=True,
            json_dumps_params={"ensure_ascii": False},
            status=HTTPStatus.OK,
        )
