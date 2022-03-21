from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from caches import cached_test
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry, Tunable
from sims4.common import Pack, is_available_pack


class TD1MasterSpellsPackTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):

    FACTORY_TUNABLES = {
        'pack': TunableEnumEntry(
            description='The Pack to test for.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        ),
        'is_installed': Tunable(
            description='Modifier to determine if the pack is installed.',
            tunable_type=bool,
            default=True
        ),
    }

    __slots__ = ('pack', 'is_installed')

    def get_expected_args(self):
        return {}

    @cached_test
    def __call__(self):
        if self.pack is not None:
            if is_available_pack(self.pack):
                if self.is_installed is True:
                    return TestResult.TRUE
                else:
                    return TestResult(False, f'{self.pack} exists in pack list.', tooltip=self.tooltip)
            else:
                if self.is_installed is False:
                    return TestResult.TRUE
                else:
                    return TestResult(False, f'{self.pack} is not found within the pack list.', tooltip=self.tooltip)
        else:
            return TestResult(False, f'No pack specified.', tooltip=self.tooltip)
