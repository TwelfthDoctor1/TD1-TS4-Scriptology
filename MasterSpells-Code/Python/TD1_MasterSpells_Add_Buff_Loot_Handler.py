"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's MasterSpellsAlchemy

> Loot Buff/Trait Injector Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import event_testing
import services
from buffs.tunable import TunableBuffReference
from interactions.base import mixer_interaction
from interactions.base.basic import TunableBasicExtras
from buffs.buff import Buff
from interactions.utils.loot import LootActions
from interactions.utils.tunable import TunableAffordanceLinkList
from sims4.common import Pack, is_available_pack
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableReference, TunableList, TunableTuple, OptionalTunable, \
    Tunable, TunableEnumEntry
from sims4.tuning.tunable_base import GroupNames
from statistics import commodity

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Loot Buff Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Loot Buff Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Loot Buff Injector', default_owner='TwelfthDoctor1')


class TD1MasterSpellsLootBuffInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                      manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'buff_reference': TunableReference(
            description='The buff for the loots to inject into, only ONE buff can be used',
            manager=services.get_instance_manager(Types.BUFF),
            pack_safe=True,
            allow_none=True
        ),
        'loot_on_addition': TunableList(
            description='A list of loots on add to be injected onto the mentioned buff on load',
            tunable=LootActions.TunableReference(pack_safe=True)
        ),
        'loot_on_instance': TunableList(
            description='A list of loots on instance to be injected onto the mentioned buff on load',
            tunable=LootActions.TunableReference(pack_safe=True)
        ),
        'loot_on_removal': TunableList(
            description='A list of loots on removal to be injected onto the mentioned buff on load',
            tunable=LootActions.TunableReference(pack_safe=True)
        ),
        'replace_loot_on_addition': Tunable(
            description='Modifier to determine should the referenced buff loot_on_addition should be replaced.',
            tunable_type=bool,
            default=False
        ),
        'replace_loot_on_instance': Tunable(
            description='Modifier to determine should the referenced buff loot_on_instance should be replaced.',
            tunable_type=bool,
            default=False
        ),
        'replace_loot_on_removal': Tunable(
            description='Modifier to determine should the referenced buff loot_on_removal should be replaced.',
            tunable_type=bool,
            default=False
        ),
        'trait_reference': TunableReference(
            description='The trait instance to reference from to add the respective buffs into the trait.',
            manager=services.get_instance_manager(Types.TRAIT),
            pack_safe=True,
            allow_none=True
        ),
        'buffs': TunableList(
            description='Buffs that should be added to the Sim whenever this trait is equipped.',
            tunable=TunableBuffReference(
                pack_safe=True
            ),
            unique_entries=True
        ),
        'is_npc_only': Tunable(
            description='If checked, this trait will get removed from Sims that have a home when the zone is loaded or whenever they switch to a household that has a home zone.',
            tunable_type=bool,
            default=False,
            tuning_group=GroupNames.AVAILABILITY
        ),
        'pack': TunableEnumEntry(
            description='The pack to test for.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        )
    }

    __slots__ = ['loot_on_addition', 'loot_on_instance', 'loot_on_removal', 'buff_reference', 'add_test_sets',
                 'replace_loot_on_addition', 'replace_loot_on_instance', 'replace_loot_on_removal', 'trait_reference',
                 'buffs', 'interactions', 'is_npc_only', 'pack']

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.buff_reference is not None:
            if is_available_pack(cls.pack):
                if cls.loot_on_addition is not None:
                    add_loot_on_addition_to_buff(cls.buff_reference, cls.loot_on_addition, cls.replace_loot_on_addition)

                if cls.loot_on_instance is not None:
                    add_loot_on_instance_to_buff(cls.buff_reference, cls.loot_on_instance, cls.replace_loot_on_instance)

                if cls.loot_on_removal is not None:
                    add_loot_on_removal_to_buff(cls.buff_reference, cls.loot_on_removal, cls.replace_loot_on_removal)

        if cls.trait_reference is not None:
            if is_available_pack(cls.pack):
                if cls.buffs is not None:
                    add_buffs_to_trait(cls.trait_reference, cls.buffs)

                if cls.is_npc_only is not None:
                    replace_npc_status(cls.trait_reference, cls.is_npc_only)


class TD1MasterSpellsLootBuffInjectorV2(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                        manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'buff_injector': TunableList(
            description='Lists to inject to the specified buffs.',
            tunable=TunableTuple(
                description='Data to be injected.',
                buff_reference=TunableList(
                    description='The specified buffs to be injected.',
                    tunable=TunableReference(
                        description='The buff for the loots to inject into, only ONE buff can be used',
                        manager=services.get_instance_manager(Types.BUFF),
                        pack_safe=True,
                        allow_none=True
                    ),
                ),
                loot_on_addition=TunableList(
                    description='A list of loots on add to be injected onto the mentioned buff on load',
                    tunable=LootActions.TunableReference(pack_safe=True)
                ),
                loot_on_instance=TunableList(
                    description='A list of loots on instance to be injected onto the mentioned buff on load',
                    tunable=LootActions.TunableReference(pack_safe=True)
                ),
                loot_on_removal=TunableList(
                    description='A list of loots on removal to be injected onto the mentioned buff on load',
                    tunable=LootActions.TunableReference(pack_safe=True)
                ),
                replace_loot_on_addition=Tunable(
                    description='Modifier to determine should the referenced buff loot_on_addition should be replaced.',
                    tunable_type=bool,
                    default=False
                ),
                replace_loot_on_instance=Tunable(
                    description='Modifier to determine should the referenced buff loot_on_instance should be replaced.',
                    tunable_type=bool,
                    default=False
                ),
                replace_loot_on_removal=Tunable(
                    description='Modifier to determine should the referenced buff loot_on_removal should be replaced.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            )
        ),
        'trait_injector': TunableList(
            description='Lists to inject to the specified traits.',
            tunable=TunableTuple(
                description='Data to be injected.',
                trait_reference=TunableList(
                    tunable=TunableReference(
                        description='The trait instance to reference from to add the respective buffs into the trait.',
                        manager=services.get_instance_manager(Types.TRAIT),
                        pack_safe=True,
                        allow_none=True
                    ),
                ),
                buffs=TunableList(
                    description='Buffs that should be added to the Sim whenever this trait is equipped.',
                    tunable=TunableBuffReference(
                        pack_safe=True
                    ),
                    unique_entries=True
                ),
                is_npc_only=Tunable(
                    description='If checked, this trait will get removed from Sims that have a home when the zone is loaded or whenever they switch to a household that has a home zone.',
                    tunable_type=bool,
                    default=False,
                    tuning_group=GroupNames.AVAILABILITY
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            )
        )
    }

    __slots__ = ('buff_injector', 'trait_injector')

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.buff_injector is not None:
            for buff_injector_data in cls.buff_injector:
                if buff_injector_data.buff_reference is not None:
                    if is_available_pack(buff_injector_data.pack):
                        for buff in buff_injector_data.buff_reference:
                            if buff_injector_data.loot_on_addition is not None:
                                add_loot_on_addition_to_buff(buff, buff_injector_data.loot_on_addition,
                                                             buff_injector_data.replace_loot_on_addition)

                            if buff_injector_data.loot_on_instance is not None:
                                add_loot_on_instance_to_buff(buff, buff_injector_data.loot_on_instance,
                                                             buff_injector_data.replace_loot_on_instance)

                            if buff_injector_data.loot_on_removal is not None:
                                add_loot_on_removal_to_buff(buff, buff_injector_data.loot_on_removal,
                                                            buff_injector_data.replace_loot_on_removal)

        if cls.trait_injector is not None:

            # DEBUG TESTING | REMOVE WHEN COMPLETE
            if master_logger is not None and master_logger is not False:
                master_logger.debug(f'LOOT INT INJECTOR: DEBUGGING INFORMATION\n\nExtraction of Trait Injector in Loot Buff Injector\n\n{cls.trait_injector}')

            for trait_injector_data in cls.trait_injector:
                if trait_injector_data.trait_reference is not None:
                    if is_available_pack(trait_injector_data.pack):
                        for trait in trait_injector_data.trait_reference:
                            if trait_injector_data.buffs is not None:

                                # DEBUG TESTING | REMOVE WHEN COMPLETE
                                if master_logger is not None and master_logger is not False:
                                    master_logger.debug(f'LOOT INT INJECTOR: DEBUGGING INFORMATION\n\nExtraction of buffs Tunable\n\n{trait_injector_data.buffs}')

                                add_buffs_to_trait(trait, trait_injector_data.buffs)

                            if trait_injector_data.is_npc_only is not None:
                                replace_npc_status(trait, trait_injector_data.is_npc_only)


# Injection Handling Section
def add_loot_on_addition_to_buff(buff, loot_to_inject, replace):
    if replace is False:
        buff._loot_on_addition += loot_to_inject

        logger.info("Replacing Loot On Addition on {} into {}.".format(buff, loot_to_inject))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Replacing Loot On Addition on {} into {}.".format(buff, loot_to_inject))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Replacing Loot On Addition on {} into {}.".format(buff, loot_to_inject))

    else:
        buff._loot_on_addition = loot_to_inject

        logger.info("Adding Loot On Addition {} into {}.".format(loot_to_inject, buff))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Adding Loot On Addition {} into {}.".format(loot_to_inject, buff))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Adding Loot On Addition {} into {}.".format(loot_to_inject, buff))


def add_loot_on_instance_to_buff(buff, loot_to_inject, replace):
    if replace is False:
        buff._loot_on_instance += loot_to_inject

        logger.info("Replacing Loot On Instance on {} into {}.".format(buff, loot_to_inject))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Replacing Loot On Instance on {} into {}.".format(buff, loot_to_inject))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Replacing Loot On Instance on {} into {}.".format(buff, loot_to_inject))

    else:
        buff._loot_on_instance = loot_to_inject

        logger.info("Adding Loot On Instance {} into {}.".format(loot_to_inject, buff))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Adding Loot On Instance {} into {}.".format(loot_to_inject, buff))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Adding Loot On Instance {} into {}.".format(loot_to_inject, buff))


def add_loot_on_removal_to_buff(buff, loot_to_inject, replace):
    if replace is False:
        buff._loot_on_removal += loot_to_inject

        logger.info("Replacing Loot On Removal on {} into {}.".format(buff, loot_to_inject))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Replacing Loot On Removal on {} into {}.".format(buff, loot_to_inject))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Replacing Loot On Removal on {} into {}.".format(buff, loot_to_inject))

    else:
        buff._loot_on_removal = loot_to_inject

        logger.info("Adding Loot On Removal {} into {}.".format(loot_to_inject, buff))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Adding Loot On Removal {} into {}.".format(loot_to_inject, buff))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Adding Loot On Removal {} into {}.".format(loot_to_inject, buff))


def add_buffs_to_trait(trait, buff_list):
    trait.buffs += buff_list

    logger.info("Adding Buffs {} onto {}.".format(buff_list, trait))

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info("Adding Buffs {} onto {}.".format(buff_list, trait))

    if master_logger is not None and master_logger is not False:
        master_logger.info("Adding Buffs {} onto {}.".format(buff_list, trait))


def replace_npc_status(trait, modifier):
    trait.is_npc_only = modifier

    logger.info("Modifying NPC Status {} onto {}.".format(modifier, trait))

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info("Modifying NPC Status {} onto {}.".format(modifier, trait))

    if master_logger is not None and master_logger is not False:
        master_logger.info("Modifying NPC Status {} onto {}.".format(modifier, trait))
