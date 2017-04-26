import pytest
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
from py_backwards import files


class TestGetInputPath(object):
    @pytest.fixture(autouse=True)
    def exists(self, mocker):
        exists_mock = mocker.patch('py_backwards.files.Path.exists')
        exists_mock.return_value = True
        return exists_mock

    def test_dir_to_file(self):
        with pytest.raises(files.InvalidInputOutput):
            list(files.get_input_output_paths('src/', 'out.py'))

    def test_non_exists_input(self, exists):
        exists.return_value = False
        with pytest.raises(files.InputDoesntExists):
            list(files.get_input_output_paths('src/', 'out/'))

    def test_file_to_dir(self):
        assert list(files.get_input_output_paths('test.py', 'out/')) == [
            files.InputOutput(Path('test.py'), Path('out/test.py'))]

    def test_file_to_file(self):
        assert list(files.get_input_output_paths('test.py', 'out.py')) == [
            files.InputOutput(Path('test.py'), Path('out.py'))]

    def test_dir_to_dir(self, mocker):
        glob_mock = mocker.patch('py_backwards.files.Path.glob')
        glob_mock.return_value = [Path('src/main.py'), Path('src/const/const.py')]
        assert list(files.get_input_output_paths('src', 'out')) == [
            files.InputOutput(Path('src/main.py'), Path('out/main.py')),
            files.InputOutput(Path('src/const/const.py'), Path('out/const/const.py'))]
