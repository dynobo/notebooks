from .context import notebooks


def test_app(capsys, example_fixture):
    # pylint: disable=W0612,W0613
    notebooks.Blueprint.run()
    captured = capsys.readouterr()

    assert "Hello World..." in captured.out
