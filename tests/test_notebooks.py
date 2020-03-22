# Standard
import sys
import logging

# Extra
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import nbformat

LOGGER = logging.getLogger(__name__)


def log_error_list(errors):
    for idx, error in enumerate(errors):
        LOGGER.error("=" * 60)
        LOGGER.error(f"ERROR NO. {idx+1}:")
        for k, v in error.items():
            if k == "traceback":
                LOGGER.error(f"{k}:")
                sys.stdout.write("\n".join(v))
            else:
                LOGGER.error(f"{k:<12}: {v}")


def notebook_run(nb_file):
    """Load an ipynb file, execute it, and log traceback in case of error.

    Arguments:
        nb_file {str} -- Path to ipynb file

    Returns:
        tuple ({Notebook}, {list}) -- Executed Notebook object and list of errors
    """
    with open(nb_file, "r") as f:
        nb = nbformat.read(f, as_version=4)

    try:
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": "notebooks/"}})
    except CellExecutionError:
        LOGGER.error(f"Error while executing notebook!")
        raise
    finally:
        errors = [
            output
            for cell in nb.cells
            if "outputs" in cell
            for output in cell["outputs"]
            if output.output_type == "error"
        ]
        log_error_list(errors)

    return nb, errors


def test_execute_notebooks(nb_files):
    """Test list of ipynb-files get executed without errors

    Arguments:
        nb_files {list} -- List of Paths of ipynb to test
    """
    for nb_file in nb_files:
        LOGGER.info("Testing '" + nb_file + "' ...")
        nb, errors = notebook_run(nb_file)
        assert errors == []
