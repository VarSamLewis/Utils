import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import tempfile
import shutil
from pathlib import Path
from io import StringIO

from genreqs_tool.genreqs import (
    extract_from_py,
    extract_from_ipynb,
    find_files_and_extract,
    genreqs,
    printreqs,
    check_module_against_stdlib
)

class TestImportExtraction(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_extract_from_py(self):
        py_file = self.temp_dir / "script.py"
        py_file.write_text("import os\nimport pandas as pd\nfrom math import sqrt")
        result = extract_from_py(py_file)
        self.assertEqual(set(result), {"os", "pandas", "math"})

    def test_extract_from_ipynb(self):
        ipynb_file = self.temp_dir / "notebook.ipynb"
        notebook = {
            "cells": [
                {"cell_type": "code", "source": ["import json\nfrom sklearn import svm"]},
                {"cell_type": "code", "source": ["import os"]}
            ]
        }
        ipynb_file.write_text(json.dumps(notebook))
        result = extract_from_ipynb(ipynb_file)
        self.assertEqual(set(result), {"json", "sklearn", "os"})

    def test_find_files_and_extract(self):
        py_file = self.temp_dir / "script.py"
        py_file.write_text("import numpy\nfrom datetime import datetime")

        ipynb_file = self.temp_dir / "notebook.ipynb"
        notebook = {
            "cells": [{"cell_type": "code", "source": ["import os\nimport sys"]}]
        }
        ipynb_file.write_text(json.dumps(notebook))

        result = find_files_and_extract(self.temp_dir)
        self.assertCountEqual(result, ["numpy", "datetime", "os", "sys"])

    def test_genreqs_creates_file(self):
        py_file = self.temp_dir / "script.py"
        py_file.write_text("import requests\nimport os")

        genreqs(self.temp_dir)
        req_file = self.temp_dir / "requirements.txt"
        self.assertTrue(req_file.exists())

        content = req_file.read_text().strip().splitlines()
        self.assertIn("requests", content)
        self.assertNotIn("os", content)

    def test_printreqs_outputs_third_party_only(self):
        py_file = self.temp_dir / "script.py"
        py_file.write_text("import requests\nimport os")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            printreqs(self.temp_dir)
            output = mock_stdout.getvalue().strip().splitlines()

        self.assertIn("requests", output)
        self.assertNotIn("os", output)

    def test_check_module_against_stdlib(self):
        self.assertTrue(check_module_against_stdlib("os"))
        self.assertFalse(check_module_against_stdlib("pandas"))


if __name__ == "__main__":
    unittest.main()
