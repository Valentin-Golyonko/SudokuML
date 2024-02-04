from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/v1/core/", include("app.core.urls")),
    path("api/v1/board/", include("app.board.urls")),
    path("api/v1/solver/", include("app.solver.urls")),
    #
    path("admin/", admin.site.urls),
]
