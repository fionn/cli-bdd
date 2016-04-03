import unittest
import re

from mock import Mock, patch
from hamcrest import (
    assert_that,
    equal_to,
)

from cli_bdd.behave import steps as behave_steps_root_module
from cli_bdd.lettuce import steps as lettuce_steps_root_module
from cli_bdd.lettuce.steps.mixins import LettuceStepMixin


class TestCase(unittest.TestCase):
    pass


class StepsSentenceRegexTestMixin(object):
    step_experiments = None
    steps = None

    def test_experiments(self):
        for step_func_name, step_exp in self.step_experiments.items():
            sentence = self.steps[step_func_name].sentence
            for exp in step_exp:
                result = re.search(sentence, exp['value'])
                assert_that(result.groups(), equal_to(exp['expected']['args']))


class StepsTestMixin(object):
    module = None
    root_module = None

    def execute_module_step(self, name, context=None, args=[], table=[], text=None):
        assert_that(
            getattr(self.module, name),
            equal_to(getattr(self.root_module, name))
        )
        context = context or Mock()
        return self._execute_module_step(
            name,
            context=context,
            args=args,
            table=table,
            text=text,
        )

    def _execute_module_step(self, name, context, args, table, text):
        raise NotImplementedError()


class BehaveStepsTestMixin(StepsTestMixin):
    module = None
    root_module = behave_steps_root_module

    def _execute_module_step(self, name, context, args, table, text):
        context.table = table
        context.text = text
        getattr(self.module, name)(context, *args)
        return context


class LettuceStepsTestMixin(StepsTestMixin):
    module = None
    root_module = lettuce_steps_root_module

    def _execute_module_step(self, name, context, args, table, text):
        step_context = Mock()
        step_context.hashes = table
        step_context.multiline = text

        with patch.object(LettuceStepMixin, 'get_scenario_context', lambda self: context):
            getattr(self.module, name)(step_context, *args)
        return context
