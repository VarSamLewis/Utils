import unittest
from unittest.mock import patch, mock_open
import json
import os
from genreqs_tool.genreqs import (
    extract_from_py,
    extract_from_ipynb,
    find_files_and_extract,
    genreqs
)

class TestImportExtraction(unittest.TestCase):

    def test_extract_from_py(self):
        fake_code = "import os\nimport pandas as pd\nfrom math import sqrt"
        with patch("builtins.open", mock_open(read_data=fake_code)):
            result = extract_from_py("fake/path/script.py")
        self.assertEqual(set(result), {"os", "pandas", "math"})

    def test_extract_from_ipynb(self):
        notebook = {
            "cells": [
                {"cell_type": "code", "source": ["import json\nfrom sklearn import svm"]},
                {"cell_type": "code", "source": ["import os"]}
            ]
        }
        fake_json = json.dumps(notebook)
        with patch("builtins.open", mock_open(read_data=fake_json)):
            result = extract_from_ipynb("fake/notebook.ipynb")
        self.assertEqual(set(result), {"json", "sklearn", "os"})

    def test_find_files_and_extract(self):
        mock_files = ["script.py", "notebook.ipynb"]
        mock_walk = [("fake_root", [], mock_files)]
        py_code = "import numpy\nfrom datetime import datetime"
        ipynb_content = {
            "cells": [{"cell_type": "code", "source": ["import os\nimport sys"]}]
        }

        with patch("os.walk", return_value=mock_walk), \
             patch("builtins.open", mock_open()) as m_open:
            m_open.side_effect = [
                mock_open(read_data=py_code).return_value,
                mock_open(read_data=json.dumps(ipynb_content)).return_value
            ]
            result = find_files_and_extract("some/folder")
        self.assertCountEqual(result, ["numpy", "datetime", "os", "sys"])

    def test_genreqs_creates_file(self):
        mock_files = ["script.py"]
        py_code = "import requests"
        req_path = os.path.join("fake_root", "requirements.txt")

        with patch("os.walk", return_value=[("fake_root", [], mock_files)]), \
             patch("os.path.exists", return_value=False), \
             patch("builtins.open", mock_open(read_data=py_code)) as m_open:
            handle = m_open()
            handle.write = unittest.mock.Mock()
            genreqs("fake_root")
            m_open.assert_any_call(req_path, "w", encoding="utf-8")
            handle.write.assert_called_with("requests\n")

    def test_genreqs_skips_existing_file(self):
        with patch("os.path.exists", return_value=True), \
             patch("builtins.print") as mock_print:
            genreqs("fake_folder")
            mock_print.assert_called_with("requirements.txt already exists")

if __name__ == "__main__":
    unittest.main()
