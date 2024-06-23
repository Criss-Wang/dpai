import pytest
import pandas as pd


@pytest.fixture(scope="session")
def inputs():
    return pd.read_csv("tests/fixtures/services_tests_resource.csv")


@pytest.fixture(name="mock_output", scope="session")
def mock_output():
    return pd.read_csv("tests/fixtures/services_tests_resource.csv")
