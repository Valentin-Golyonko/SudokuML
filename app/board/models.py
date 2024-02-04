from django.db import models

from app.board.constants import BoardConstants


class Board(models.Model):

    title = models.CharField(
        max_length=20,
        default="",
    )

    data = models.JSONField(
        default=list,
    )

    difficulty = models.PositiveSmallIntegerField(
        choices=BoardConstants.DIFFICULTY_CHOICES,
    )

    class Meta:
        ordering = ("id",)
