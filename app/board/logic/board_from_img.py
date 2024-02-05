""""""

from pathlib import Path

import skimage as ski
from numpy import ndarray

from dj_config.settings import BASE_DIR


class BoardFromImg:
    """BoardFromImg"""

    @classmethod
    def process_board_img(cls) -> None:
        """
        debug:
            from app.board.logic.board_from_img import BoardFromImg
            BoardFromImg.process_board_img()
        :return:
        """

        ski_board = cls.load_board_img()

        return None

    @staticmethod
    def load_board_img() -> ndarray | None:
        """
        https://scikit-image.org/docs/stable/user_guide/getting_started.html
        """
        img_path = f"{BASE_DIR}/media/easy/easy_21.png"
        if not Path(img_path).exists():
            return None
        if not Path(img_path).is_file():
            return None

        ski_board: ndarray = ski.io.imread(img_path)

        return ski_board
