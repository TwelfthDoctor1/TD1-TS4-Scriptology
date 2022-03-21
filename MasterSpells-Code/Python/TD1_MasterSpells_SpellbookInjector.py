import services
from sims4.collections import FrozenAttributeDict
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableList, TunableMapping, TunableReference
from sims4.tuning.tunable_base import GroupNames
from ui.spellbook_tuning import SpellbookCategoryData, SpellbookRecipeData, SpellbookTuning
from sims4.log import Logger

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Spellbook Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Spellbook Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Spellbook Injector', default_owner="TwelfthDoctor1")


class TD1MasterSpellsSpellbookInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                       manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'spellbook_category_data': TunableList(
            description='A list of a spellbook category data.',
            tunable=SpellbookCategoryData.TunableFactory(),
            tuning_group=GroupNames.UI
        ),
        'potion_display_data': TunableMapping(
            description="A mapping of a potion's recipe to it's spellbook display data.",
            key_type=TunableReference(
                description="The potion's recipe.",
                manager=services.get_instance_manager(Types.RECIPE),
                class_restrictions=('Recipe',),
                pack_safe=True
            ),
            value_type=SpellbookRecipeData.TunableFactory(),
            tuning_group=GroupNames.UI
        )
    }

    __slots__ = ('spellbook_category_data', 'potion_display_data')

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.spellbook_category_data is not None:

            # DEBUGGING OUTPUT
            master_logger.debug(
                f"Data in cls.spellbook_category_data:\n{cls.spellbook_category_data}\n\nData in SpellbookTuning.CATEGORY_DATAS:\n{SpellbookTuning.CATEGORY_DATAS}"
            )

            for c_data in cls.spellbook_category_data:
                for sp_c_data in SpellbookTuning.CATEGORY_DATAS:
                    if c_data.category_name is not None and c_data.content is not None:
                        if c_data.content.category_type == sp_c_data.content.category_type or hasattr(c_data.content, 'category_type') is False:

                            sp_category_type_entries = set(sp_c_data.content.entries)

                            category_type_entries = set(c_data.content.entries)

                            final_c_type_entries = sp_category_type_entries.union(category_type_entries)

                            message1 = f"Injecting:\n{c_data.content.entries}\n\nTarget:\n{sp_c_data.content.entries}"

                            if apprentice_logger is not None and apprentice_logger is not False:
                                apprentice_logger.info(message1, owner="TwelfthDoctor1")

                            if master_logger is not None and master_logger is not False:
                                master_logger.info(message1, owner="TwelfthDoctor1")

                            logger.info(message1, owner="TwelfthDoctor1")

                            sp_c_data.content.entries = sp_c_data.content.clone_with_overrides(final_c_type_entries)

        if cls.potion_display_data is not None:

            message2 = f"Injecting:\n{cls.potion_display_data}\n\nTarget:\n{SpellbookTuning.POTION_DISPLAY_DATA}"

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message2, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message2, owner="TwelfthDoctor1")

            logger.info(message2, owner="TwelfthDoctor1")

            SpellbookTuning.POTION_DISPLAY_DATA = FrozenAttributeDict(
                {**dict(SpellbookTuning.POTION_DISPLAY_DATA), **cls.potion_display_data}
            )
