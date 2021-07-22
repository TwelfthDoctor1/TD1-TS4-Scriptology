from event_testing.results import TestResult
from event_testing.test_base import BaseTest
from caches import cached_test
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableEnumEntry, Tunable
from sims4.common import Pack, is_available_pack


class TD1FrameworkStructurePackTestOverride:
    # Module Tuning
    FRAMEWORKSTRUCTURE_OVERRIDE_PACK_TESTSET = Tunable(
        description='Controls the overridding of Pack TestSets. If enabled, any pack testset that is supposedly to be set as False will be inverted to True. This can allow access to certain sections even though the player does not own the specified pack.',
        tunable_type=bool,
        default=False
    )


class TD1FrameworkStructurePackTest(HasTunableSingletonFactory, AutoFactoryInit, BaseTest):
    # Snippet Tuning
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
            # Case 1: If enabled ALL Pack TestSets will be TRUE. You can attach or change to use a config option instead.
            # DevAccessPanel: or get_option_value('override_pack_testset') is True
            if TD1FrameworkStructurePackTestOverride.FRAMEWORKSTRUCTURE_OVERRIDE_PACK_TESTSET is True:
                return TestResult.TRUE
            # Case 2: Regular Pack Testing If Available
            if is_available_pack(self.pack):
                # Case 2a: Specified Pack is Installed
                if self.is_installed is True:
                    return TestResult.TRUE
                # Case 2b: Specified Pack is Not Installed
                else:
                    return TestResult(False, f'{self.pack} exists in pack list.', tooltip=self.tooltip)
            # Case 3: Regular Pack Testing if Not available
            else:
                # Case 3a: If Pack is not installed
                if self.is_installed is False:
                    return TestResult.TRUE
                # Case 3b: If Pack is installed
                else:
                    return TestResult(False, f'{self.pack} is not found within the pack list.', tooltip=self.tooltip)
        else:
            return TestResult(False, f'No pack specified.', tooltip=self.tooltip)
