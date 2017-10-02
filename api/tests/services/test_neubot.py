import pytest
import src.services.neubot as nb


@pytest.fixture
def neubot_service():
    return nb.NeubotService()


def test_dash_data(neubot_service):
    x = neubot_service.dash_data()
    assert True