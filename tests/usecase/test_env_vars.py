import os

from basetest import BaseTest


class FooTest(BaseTest):
    def test_expose_env_vars(self):
        env_vars = (
            os.environ["CF_ENDPOINT"],
            os.environ["CF_USER"],
            os.environ["CF_ORG"],
            os.environ["CF_SPACE"],
        )
        self.assertEqual(env_vars, "foobar")
