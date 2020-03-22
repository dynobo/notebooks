import logging
import pytest

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def nb_files():
    prefix = "notebooks/"
    notebooks = ["2020-02-Alexa.ipynb", "2020-Tetris.ipynb"]
    return [prefix + nb for nb in notebooks]
