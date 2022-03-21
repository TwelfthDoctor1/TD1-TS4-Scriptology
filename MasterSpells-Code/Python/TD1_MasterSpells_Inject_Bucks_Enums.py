from bucks import bucks_enums
from sims4.log import Logger
from TD1_MasterSpells_ModuleHandler import TD1MasterSpellsModuleHandler

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Bucks Enums Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Bucks Enums Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Bucks Enums Injector', default_owner='TwelfthDoctor1')


def add_category_tags(name, number):
    with bucks_enums.BucksType.make_mutable():
        bucks_enums.BucksType._add_new_enum_value(name, number)

        logger.info("Bucks Enum: {} | {} is now injected.".format(name, number))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Bucks Enum: {} | {} is now injected.".format(name, number))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Bucks Enum: {} | {} is now injected.".format(name, number))


# Add the following EnumValue (FNV24) and its respective tag below as name, number.
# Example: add_category_tags('BucksTagName', EnumValue)
if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BUCKS_ENUM_INJECTION is True:
    add_category_tags('TD1LightPerkBucks', 12529885)
    add_category_tags('TD1DarkPerkBucks', 4897332)
