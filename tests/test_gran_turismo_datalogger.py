#!/usr/bin/env python3.5

"""
tests for ../gran_turismo_datalogger.py

Note:
    general pattern for test function arguments:
        test_func(patch1, ..., patchN, fixture1, ..., fixutreN

Documentation:
    pytest: https://docs.pytest.org/en/3.0.1/contents.html
    unittest.mock: https://docs.python.org/3.5/
                           library/unittest.mock.html#unittest.mock.MagicMock

Vim grabs:
--------------------------------
@patch("gran_turismo_datalogger.
--------------------------------
"""

from unittest.mock import MagicMock, patch, call

import pytest
import gran_turismo_datalogger as gt

@patch("gran_turismo_datalogger.DataLogger")
@patch("gran_turismo_datalogger.cd_to_project_root")
@patch("gran_turismo_datalogger.parse_args")
class TestMain(object):
    """
    tests for main function
    """
    def test_main_parses_arguments(
            self, parse_args, cd_to_project_root, data_logger_constructor
        ):
        gt.main()
        assert parse_args.called == True

    def test_main_changes_working_diretory_to_project_root(
            self, parse_args, cd_to_project_root, data_logger_constructor
        ):
        gt.main()
        assert cd_to_project_root.called == True

        cd_to_project_root()
    def test_main_starts_datalogger(
            self, parse_args, cd_to_project_root, data_logger_constructor
        ):
        data_logger = MagicMock()
        data_logger_constructor.return_value = data_logger

        gt.main()
        assert data_logger.start.called == True

class TestImageCompare(object):
    """
    tests for ImageCompare class
    """
    def test_image_similarity_returns_known_results(
            self,
        ):
        gt.cd_to_project_root()
        from PIL import Image
        exemplar_image = Image.open("./exemplars/exit.png")
        similar_image = Image.open("./tests/img/exit_similar.png")
        unsimilar_image = Image.open("./tests/img/exit_unsimilar.png")

        # test similar
        comparison = gt.ImageCompare(exemplar_image, similar_image)
        assert round(comparison.similarity(), 2) == 97.41

        # test unsimilar
        comparison = gt.ImageCompare(exemplar_image, unsimilar_image)
        assert round(comparison.similarity(), 2) == 59.05
