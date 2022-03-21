from bucks.bucks_enums import BucksType, BucksTrackerType
import services
from sims4.localization import TunableLocalizedStringFactory
from sims4.tuning.tunable import TunableMapping, TunableEnumEntry, TunableTuple, OptionalTunable, TunableEnumSet, \
    TunableReference
from sims4.tuning.tunable_base import ExportModes, EnumBinaryExportType
import sims4
from sims4.collections import FrozenAttributeDict
from sims4.resources import Types
from sims4.log import Logger
from bucks.bucks_utils import BucksUtils
from TD1_MasterSpells_ModuleHandler import TD1MasterSpellsModuleHandler

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Bucks Utils Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Bucks Utils Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger("TD1 Bucks Utils Injector")


class TD1BucksUtils:
    BUCK_TYPE_TO_TRACKER_MAP_TO_INJECT = TunableMapping(
        description='\n        Maps a buck type to the tracker that uses that bucks type.\n        ',
        key_type=TunableEnumEntry(
            tunable_type=BucksType,
            default=BucksType.INVALID,
            invalid_enums=BucksType.INVALID,
            pack_safe=True), key_name='Bucks Type',
        value_type=BucksTrackerType,
        value_name='Bucks Tracker'
    )
    BUCK_TYPE_TO_DISPLAY_DATA_TO_INJECT = TunableMapping(
        description='\n        For each supplied Bucks, a set of UI display data to be used when displaying\n        information related to this bucks in the UI.\n        ',
        key_type=TunableEnumEntry(
            tunable_type=BucksType,
            default=BucksType.INVALID,
            invalid_enums=BucksType.INVALID,
            pack_safe=True),
        key_name='Bucks Type',
        value_type=TunableTuple(
            description='\n            A set of UI display data for one bucks type.\n            ',
            ui_name=TunableLocalizedStringFactory(),
            cost_string=OptionalTunable(
                description='\n                Format for displaying interaction names on interactions that\n                have this buck as a cost. 0.String is the interaction name. 1 will be the the cost\n                amount.\n                ',
                tunable=TunableLocalizedStringFactory()),
            gain_string=OptionalTunable(
                description='\n                Format for displaying interaction names on interactions that\n                have this buck as a gain. 0.String is the interaction name. 1 will be the the gain\n                amount.\n                ',
                tunable=TunableLocalizedStringFactory()),
            headline=OptionalTunable(
                description='\n                If enabled when this buck updates we will display\n                a headline update to the UI for selectable sims.\n                ',
                tunable=TunableReference(
                    description='\n                    The headline that we want to send down.\n                    ',
                    manager=services.get_instance_manager(sims4.resources.Types.HEADLINE)))),
        value_name='Bucks UI Data'
    )
    WALLET_BUCK_TYPES_TO_INJECT = TunableEnumSet(
        description='\n        A list of buck types whose values will be displayed in the wallet\n        tooltip.\n        ',
        enum_type=BucksType,
        invalid_enums=BucksType.INVALID,
        pack_safe=True,
        export_modes=ExportModes.ClientBinary,
        binary_type=EnumBinaryExportType.EnumUint32
    )


def add_utils_to_bucks_utils(self):
    if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BUCKS_UTILS_TRACKER_MAP_INJECTION is True:
        if TD1BucksUtils.BUCK_TYPE_TO_TRACKER_MAP_TO_INJECT is not None:
            logger.info('Module Print: {}'.format(TD1BucksUtils.BUCK_TYPE_TO_TRACKER_MAP_TO_INJECT), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Print: {}'.format(TD1BucksUtils.BUCK_TYPE_TO_TRACKER_MAP_TO_INJECT), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Print: {}'.format(TD1BucksUtils.BUCK_TYPE_TO_TRACKER_MAP_TO_INJECT), owner="TwelfthDoctor1")

            BucksUtils.BUCK_TYPE_TO_TRACKER_MAP = FrozenAttributeDict(
                {**dict(BucksUtils.BUCK_TYPE_TO_TRACKER_MAP), **TD1BucksUtils.BUCK_TYPE_TO_TRACKER_MAP_TO_INJECT}
            )
            logger.info('Module Injection: {}'.format(BucksUtils.BUCK_TYPE_TO_TRACKER_MAP), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Injection: {}'.format(BucksUtils.BUCK_TYPE_TO_TRACKER_MAP), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Injection: {}'.format(BucksUtils.BUCK_TYPE_TO_TRACKER_MAP), owner="TwelfthDoctor1")

    if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BUCKS_UTILS_DISPLAY_DATA_INJECTION is True:
        if TD1BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA_TO_INJECT is not None:
            logger.info('Module Print: {}'.format(TD1BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA_TO_INJECT), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Print: {}'.format(TD1BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA_TO_INJECT), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Print: {}'.format(TD1BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA_TO_INJECT), owner="TwelfthDoctor1")

            BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA = FrozenAttributeDict(
                {**dict(BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA), **TD1BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA_TO_INJECT}
            )
            logger.info('Module Injection: {}'.format(BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Injection: {}'.format(BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Injection: {}'.format(BucksUtils.BUCK_TYPE_TO_DISPLAY_DATA), owner="TwelfthDoctor1")

    if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BUCKS_UTILS_WALLET_INJECTION is True:
        if TD1BucksUtils.WALLET_BUCK_TYPES_TO_INJECT is not None:
            logger.info('Module Print: {}'.format(TD1BucksUtils.WALLET_BUCK_TYPES_TO_INJECT), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Print: {}'.format(TD1BucksUtils.WALLET_BUCK_TYPES_TO_INJECT), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Print: {}'.format(TD1BucksUtils.WALLET_BUCK_TYPES_TO_INJECT), owner="TwelfthDoctor1")

            BucksUtils.WALLET_BUCK_TYPES = FrozenAttributeDict(
                {**dict(BucksUtils.WALLET_BUCK_TYPES), **TD1BucksUtils.WALLET_BUCK_TYPES_TO_INJECT}
            )
            logger.info('Module Injection: {}'.format(BucksUtils.WALLET_BUCK_TYPES), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Injection: {}'.format(BucksUtils.WALLET_BUCK_TYPES), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Injection: {}'.format(BucksUtils.WALLET_BUCK_TYPES), owner="TwelfthDoctor1")


services.get_instance_manager(Types.TUNING).add_on_load_complete(add_utils_to_bucks_utils)
