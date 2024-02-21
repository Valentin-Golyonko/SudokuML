import json
import logging

import keras
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from app.board.constants import BoardConstants
from app.board.models import Board
from app.core.scripts.utils import time_it
from dj_config.settings import BASE_DIR

logger = logging.getLogger(__name__)


class PredictBoardNumbers:
    """
    from app.board.logic.predict_board_numbers import PredictBoardNumbers
    pbn = PredictBoardNumbers()
    pbn.process_board(difficulty="medium", board_number=11)

    for p in range(1, 8):
        for n in range(1, 5):
            pbn.process_board(difficulty="medium", board_number=f"{p}{n}")
    else:
        print("done")
    """

    def __init__(self):
        """Verify the installation"""

        logger.info(f"tf = {tf.__version__}")
        logger.info(tf.reduce_sum(tf.random.normal([1000, 1000])))
        logger.info(tf.config.list_physical_devices("GPU"))

        self.x_test_data = self.load_x_test_data()
        self.probability_model = self.load_model(self.x_test_data)
        logger.info(f"---init done---")

    @time_it
    def process_board(self, difficulty: str, board_number: str) -> None:
        board_name = f"{difficulty}_{board_number}"
        difficulty_id = BoardConstants.DIFFICULTY_DICT.get(difficulty)

        board_data = self.load_board_data(difficulty, board_name)

        # self.plot_board(board_name, board_data)

        predictions = self.predict_numbers(board_data)

        self.save_board(board_name, difficulty_id, predictions)

        logger.info(f"done; {board_name = }")
        return None

    @staticmethod
    def plot_image(i, predictions_array, img) -> None:
        _true_label = [0] * 81

        true_label, img = _true_label[i], img[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        plt.imshow(img, cmap=plt.cm.binary)

        predicted_label = np.argmax(predictions_array)
        if predicted_label == true_label:
            color = "blue"
        else:
            color = "red"

        plt.xlabel(
            "{} {:2.0f}% ({})".format(
                predicted_label, 100 * np.max(predictions_array), true_label
            ),
            color=color,
        )

        return None

    @staticmethod
    def plot_value_array(i, predictions_array) -> None:
        _true_label = [0] * 81

        true_label = _true_label[i]
        plt.grid(False)
        plt.xticks(range(10))
        plt.yticks([])
        this_plot = plt.bar(range(10), predictions_array, color="#777777")
        plt.ylim([0, 1])
        predicted_label = np.argmax(predictions_array)

        this_plot[predicted_label].set_color("red")
        this_plot[true_label].set_color("blue")

        return None

    @staticmethod
    def load_x_test_data() -> np.ndarray:
        """load x_test_combo data"""

        saved_x_test = "x_test_2024_02_09_10_18"
        x_test_path = f"{BASE_DIR}/data_sources/ml_data/{saved_x_test}.json"

        with open(x_test_path, "r") as report_file:
            x_test_data = json.load(report_file)

        x_test = np.array(x_test_data)
        logger.info(f"{x_test.shape = }")
        return x_test

    @staticmethod
    def load_model(x_test: np.ndarray) -> tf.keras.models:
        """Loading the model"""

        saved_model = "trained_mnist_2024_02_09_10_18"
        model_save_path = f"{BASE_DIR}/data_sources/ml_data/{saved_model}.keras"

        model = keras.models.load_model(model_save_path)

        probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
        predictions = probability_model.predict(x_test)

        return probability_model

    @staticmethod
    def load_board_data(difficulty: str, board_name: str) -> np.ndarray:
        """Load board data"""

        board_data_path = (
            f"{BASE_DIR}/data_sources/board_data/{difficulty}/{board_name}.json"
        )

        with open(board_data_path, "r") as report_file:
            _board_data = json.load(report_file)

        board_data = np.array(_board_data)
        logger.info(f"{board_data.shape = }")
        return board_data

    @staticmethod
    def plot_board(board_name: str, board_data: np.ndarray) -> None:
        plt.figure(figsize=(9, 9))
        plt.title(f"board data | {board_name}")
        for count, number_data in enumerate(board_data):
            plt.subplot(9, 9, count + 1)
            plt.imshow(number_data, cmap=plt.cm.binary)
        plt.show()
        return None

    def predict_numbers(self, board_data: np.ndarray) -> list[int]:
        prediction_numbers = []

        num_rows = 9
        num_cols = 9
        num_images = num_rows * num_cols
        plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
        plt.title("prediction data")
        for i in range(num_images):

            img_to_predict = np.expand_dims(board_data[i], axis=0)
            predictions_single = self.probability_model.predict(img_to_predict)

            plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
            self.plot_image(i, predictions_single[0], board_data)
            plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
            self.plot_value_array(i, predictions_single[0])

            if np.count_nonzero(board_data[i]) == 0:
                prediction_numbers.append(0)
            else:
                prediction_number = np.argmax(predictions_single[0])
                prediction_numbers.append(int(prediction_number))

        plt.tight_layout()
        plt.show()

        return prediction_numbers

    @staticmethod
    def save_board(
        board_name: str,
        difficulty_id: int,
        predictions: list[int],
    ) -> None:
        Board.objects.update_or_create(
            title=board_name,
            difficulty=difficulty_id,
            defaults={
                "data": predictions,
            },
        )
        return None
