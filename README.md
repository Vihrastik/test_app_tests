# test_app_tests

Tested app: https://github.com/dgusakov/test_app

Tests are divided into two groups:
- src/tests/api_tests;
- src/tests/web_ui_tests.

To run all tests use: 
pytest

Tu run tests class use direct path and class name: 
pytest src/tests/api_tests/test_api_template.py::TestUploadTemplates

To run single test use direct path, class name and test name: 
pytest src/tests/api_tests/test_api_template.py::TestUploadTemplates::test_success_put_with_file_and_id

To save logs use additional argument: pytest --junit-xml=xml-path

If there are problems starting CromeDriver check executable_path in conftest.py.

good luck have fun :)
