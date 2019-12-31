import pytest
from auger.app import AugerApplication

@pytest.fixture(scope='session')
def qapp(qapp):
    any_args = qapp.arguments()
    return AugerApplication(any_args)
