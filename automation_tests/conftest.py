import pytest


def pytest_addoption(parser):
    parser.addoption('--ident', metavar='ident')
    parser.addoption('--precondition_file_path', metavar='precondition_file_path', default=None,
                     help="path for file with precondition variables")
    parser.addoption('--env', metavar='env', type=str, default=None)
    parser.addoption('--execution_id', metavar='execution_id', default=0,
                     help="current execution id for precondition case")
    parser.addoption("--precondition", action="store_true",
                     help="current run is precondition or not")


@pytest.fixture(scope='session')
def ident(request):
    return request.config.getoption('--ident')


@pytest.fixture(scope='session')
def execution_id(request):
    return request.config.getoption('--execution_id')


@pytest.fixture(scope='session')
def precondition_file_path(request, is_precondition):
    return request.config.getoption('--precondition_file_path')


@pytest.fixture(scope='session')
def is_precondition(request):
    return bool(request.config.getoption('--precondition'))


@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption('--env')
