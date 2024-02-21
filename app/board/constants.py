""""""


class BoardConstants:
    """BoardConstants"""

    """difficulty ->"""
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3
    DIFFICULTY_VERY_HARD = 4

    DIFFICULTY_CHOICES = (
        (DIFFICULTY_EASY, "Easy"),
        (DIFFICULTY_MEDIUM, "Medium"),
        (DIFFICULTY_HARD, "Hard"),
        (DIFFICULTY_VERY_HARD, "Very hard"),
    )
    DIFFICULTY_DICT = {i[1].lower().replace(" ", "_"): i[0] for i in DIFFICULTY_CHOICES}
    """<- difficulty"""
