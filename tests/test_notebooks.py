# Standard
import sys
import logging

# Extra
from nbconvert import NotebookExporter
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import nbformat

# Own
from .context import notebooks

LOGGER = logging.getLogger(__name__)


def notebook_run(path):
    with open(path, "r") as f:
        nb = nbformat.read(f, as_version=4)

    try:
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        out = ep.preprocess(nb, {"metadata": {"path": "notebooks/"}})
    except CellExecutionError:
        out = None
        print(f"Error while executing notebook")
        raise
    finally:
        errors = [
            output
            for cell in nb.cells
            if "outputs" in cell
            for output in cell["outputs"]
            if output.output_type == "error"
        ]
        # print(f"Errors while executing notebook {path}: \n", errors)
        for idx, error in enumerate(errors):
            LOGGER.error("=" * 60)
            LOGGER.error(f"ERROR NO. {idx+1}:")
            for k, v in error.items():
                if k == "traceback":
                    LOGGER.error(f"{k}:")
                    sys.stdout.write("\n".join(v))
                else:
                    LOGGER.error(f"{k:<12}: {v}")
    return nb, errors


def test_execute_notebooks(nb_files):
    for nb_file in nb_files:
        LOGGER.info("Testing '" + nb_file + "' ...")
        nb, errors = notebook_run(nb_file)
        assert errors == []
