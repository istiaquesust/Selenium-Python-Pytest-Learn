# run this command in terminal: pytest -v -s code/test.py

import pytest


# fixture is used to run a method before a method.
# If you add yield, the following code will run after a method.
@pytest.fixture()
def before_method():
    print(' I run before a method')
    yield
    print(' I run after this method')


def test_method_1(before_method):
    print('Test 1')


# You can send parameters for test through mark.parametrize
@pytest.mark.parametrize("number, output", [(1, 11), (2, 21)])
def test_method_2(number, output):
    assert 11 * number == output


# mark.xfail just display pass fail
@pytest.mark.xfail
def test_method_3():
    print('I will not be printed')


# mark.skip will skip the test
@pytest.mark.skip
def test_method_4():
    print('I will be skipped')
