from django.contrib import admin

from app.board.models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "difficulty",
    )
    list_filter = ("difficulty",)
