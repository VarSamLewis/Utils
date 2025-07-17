import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from pathlib import Path

from genreqs_tool.genreqs import (
    extract_from_py,
    extract_from_ipynb,
    find_files_and_extract,
    genreqs
)

class TestImportExtraction(unittest.TestCase):

    def test_extract_from_py(self):
        fake_code = "import os\nimport pandas as pd\nfrom math import sqrt"
        with patch("pathlib.Path.open", mock_open(read_data=fake_code)):
            result = extract_from_py(Path("fake/path/script.py"))
        self.assertEqual(set(result), {"os", "pandas", "math"})

    def test_extract_from_ipynb(self):
        notebook = {
            "cells": [
                {"cell_type": "code", "source": ["import json\nfrom sklearn import svm"]},
                {"cell_type": "code", "source": ["import os"]}
            ]
        }
        fake_json = json.dumps(notebook)
        with patch("pathlib.Path.open", mock_open(read_data=fake_json)):
            result = extract_from_ipynb(Path("fake/notebook.ipynb"))
        self.assertEqual(set(result), {"json", "sklearn", "os"})

    def test_find_files_and_extract(self):
        py_code = "import numpy\nfrom datetime import datetime"
        ipynb_content = {
            "cells": [{"cell_type": "code", "source": ["import os\nimport sys"]}]
        }

        # Create fake .py and .ipynb paths
        fake_py = Path("some/folder/script.py")
        fake_ipynb = Path("some/folder/notebook.ipynb")

        def fake_rglob(_):
            return [fake_py, fake_ipynb]

        with patch("pathlib.Path.rglob", side_effect=fake_rglob), \
             patch("pathlib.Path.open", mock_open()) as m_open:
            # side_effect to return content for each file
            m_open.side_effect = [
                mock_open(read_data=py_code).return_value,
                mock_open(read_data=json.dumps(ipynb_content)).return_value
            ]
            result = find_files_and_extract("some/folder")
        self.assertCountEqual(result, ["numpy", "datetime", "os", "sys"])

    @patch("genreqs_tool.genreqs.find_files_and_extract", return_value=["requests"])
    @patch("pathlib.Path.exists", return_value=False)
    @patch("pathlib.Path.open", new_callable=mock_open)
    @patch("builtins.print")  # optional: suppress or check print output
    def test_genreqs_creates_file(self, mock_print, mock_open_func, mock_exists, mock_find):
        # Act
        genreqs("fake_root")

        # Assert the file was opened correctly
        mock_open_func.assert_called_once_with("w", encoding="utf-8")

        # Assert that 'requests\n' was written to the file
        mock_open_func().write.assert_called_with("requests\n")

        # Optional debug print
        print("WRITE CALLS:", mock_open_func().write.call_args_list)


    def test_genreqs_skips_existing_file(self):
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.unlink"), \
             patch("genreqs_tool.genreqs.find_files_and_extract", return_value=["os"]), \
             patch("pathlib.Path.open", mock_open()) as m_open:
            handle = m_open()
            handle.write = unittest.mock.Mock()
            genreqs("fake_folder")
            handle.write.assert_called_with("os\n")

if __name__ == "__main__":
    unittest.main()
