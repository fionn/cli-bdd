import subprocess
import os

from hamcrest import (
    assert_that,
    equal_to,
)

from testutils import TestCase


BASE_PATH = os.path.dirname(os.path.normpath(__file__))
FEATURES_PATH = os.path.join(BASE_PATH, 'features/')


class TestLettuceFunctional(TestCase):
    def test_me(self):
        stdout = subprocess.Popen(
            'lettuce %s -v 1' % FEATURES_PATH,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).communicate()[0].strip()
        stdout_lines = stdout.split('\n')
        assert_that(stdout_lines[-3], equal_to('1 feature (1 passed)'), stdout)
        assert_that(stdout_lines[-2], equal_to('1 scenario (1 passed)'), stdout)
        assert_that(stdout_lines[-1], equal_to('7 steps (7 passed)'), stdout)
