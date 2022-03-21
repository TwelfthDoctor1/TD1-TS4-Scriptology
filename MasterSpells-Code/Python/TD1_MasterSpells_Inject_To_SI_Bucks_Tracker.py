from bucks.bucks_enums import BucksType
from bucks.bucks_tracker import BucksTrackerBase
from distributor.ops import SetBuckFunds
from distributor.system import Distributor
from sims4.localization import TunableLocalizedString
from sims4.tuning.tunable import TunableEnumEntry, TunableMapping, Tunable, TunableTuple, TunableReference
from sims4.tuning.tunable_base import ExportModes
import services
import sims4
from bucks.sim_info_bucks_tracker import SimInfoBucksTracker
from sims4.log import Logger
from sims4.collections import FrozenAttributeDict
from sims4.resources import Types
from TD1_MasterSpells_ModuleHandler import TD1MasterSpellsModuleHandler

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Sim Info Bucks Tracker Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Sim Info Bucks Tracker Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


logger = Logger('TD1 Sim Info Bucks Tracker Injector')


class TD1SimInfoBucksTracker:
    BUCK_TYPE_TO_CATEGORIES_MAPPING_TO_INJECT = TunableMapping(
        description='\n        A mapping of buck type to the categorized buck perks. \n        ',
        key_type=TunableEnumEntry(
            description='\n            A type of bucks that this kind of tracker holds.\n            ',
            tunable_type=BucksType, default=BucksType.INVALID, pack_safe=True), value_type=TunableMapping(
            description='\n            Ordered list of buck perks categories that will appear in the \n            rewards UI along with the perks that belong in the category.\n            ',
            key_type=Tunable(
                description='\n                An integer value used to set the specific order of the categories\n                in the UI. the lower numbers are displayed first in the UI.\n                ',
                tunable_type=int, default=0), value_type=TunableTuple(
                description='\n                Tuning structure holding all of the localized string data for the \n                tuned Perk Category.        \n                ',
                category_name=TunableLocalizedString(
                    description='\n                    This is the localized name of the category that will show up \n                    in the bucks UI.\n                    '),
                category_tooltip=TunableLocalizedString(
                    description='\n                    This is the description that will show up when the user hovers\n                    over the catgory name for a while.\n                    '),
                rewards=TunableMapping(
                    description='\n                    An ordered list of the rewards that will appear in this\n                    category.\n                    ',
                    key_type=Tunable(
                        description='\n                        An integer value used to order the appearance of the rewards\n                        inside of the category. The smaller numbers are sorted to\n                        the front of the list.\n                        ',
                        tunable_type=int, default=0), value_type=TunableReference(
                        description='\n                        The Buck Perk (reward) to display in the category panel of\n                        the UI.\n                        ',
                        manager=services.get_instance_manager(sims4.resources.Types.BUCKS_PERK), pack_safe=True,
                        allow_none=True), allow_none=True, tuple_name='SimRewardCategoryMapping'),
                export_class_name='SimRewardCategoryInfoTuple'), tuple_name='SimCategoryMapping'),
        tuple_name='SimBuckToCategoryMapping', export_modes=ExportModes.ClientBinary)


def add_bucks_perk_list_to_tuning(self):
    if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_SI_BUCKS_TRACKER_INJECTION is True:
        if TD1SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING_TO_INJECT is not None:
            logger.info('Module Print: {}'.format(TD1SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING_TO_INJECT), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Print: {}'.format(TD1SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING_TO_INJECT), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Print: {}'.format(TD1SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING_TO_INJECT), owner="TwelfthDoctor1")

            SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING = FrozenAttributeDict(
                {**dict(SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING), **TD1SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING_TO_INJECT}
            )
            logger.info('Module Injection: {}'.format(SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING), owner="TwelfthDoctor1")

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Module Injection: {}'.format(SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING), owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info('Module Injection: {}'.format(SimInfoBucksTracker.BUCK_TYPE_TO_CATEGORIES_MAPPING), owner="TwelfthDoctor1")


services.get_instance_manager(Types.TUNING).add_on_load_complete(add_bucks_perk_list_to_tuning)
