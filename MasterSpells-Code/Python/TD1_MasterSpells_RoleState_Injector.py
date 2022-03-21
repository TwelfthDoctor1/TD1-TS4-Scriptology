import services
from buffs.tunable import TunableBuffReference
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableList, HasTunableReference, TunableReference

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 RoleState Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 RoleState Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 RoleState Injector')


class TD1MasterSpellsRoleStateInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                       manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'role_state_reference': TunableList(
            description='A list of role states to have an injection.',
            tunable=TunableReference(
                manager=services.get_instance_manager(Types.ROLE_STATE),
                pack_safe=True,
                allow_none=False
            )
        ),
        'buffs': TunableList(
            description='Buffs that will be added to sim when role is active.',
            tunable=TunableBuffReference(
                pack_safe=True
            )
        ),
        'loot_on_load': TunableList(
            description='A list of loots that will be applied if a sim is in this role state during zone spin up.',
            tunable=TunableReference(
                manager=services.get_instance_manager(Types.ACTION),
                class_restrictions=('LootActions', 'RandomWeightedLoot'),
                pack_safe=True
            )
        ),
        'preroll_affordances': TunableList(
            description='A list of affordances that are available for sims to consider when running pre-roll. Objects related to role can specify preroll autonomy, but there are some roles that may not have an object associated with it e.g. Romance guru in romance festival preroll to an attractor point. ',
            tunable=TunableReference(
                manager=services.affordance_manager(),
                class_restrictions=('SuperInteraction',),
                pack_safe=True
            )
        ),
        'role_affordances': TunableList(
            description="A list of affordances that are available on the Sim in this Role State. e.g: when a Maid is in the working Role State, he or she will have the 'Dismiss' and 'Fire' affordances available in the Pie Menu.",
            tunable=TunableReference(
                manager=services.affordance_manager(),
                class_restrictions=('SuperInteraction',),
                pack_safe=True
            )
        ),
        'role_target_affordances': TunableList(
            description='A list of affordances that are available on other Sims when the actor Sim is in this Role State. e.g. a Sim in a specific Role State could have an "Invite to Situation" interaction available when bringing up other Sims Pie Menus.',
            tunable=TunableReference(
                manager=services.affordance_manager(),
                class_restrictions=('SuperInteraction',),
                pack_safe=True
            )
        ),
    }

    __slots__ = ['role_state_reference', 'buffs', 'loot_on_load', 'preroll_affordances', 'role_affordances', 'role_target_affordances']

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.role_state_reference is not None:
            for role_state in cls.role_state_reference:
                if cls.buffs is not None:
                    cls.inject_buffs_into_rolestate(role_state, cls.buffs)

                if cls.loot_on_load is not None:
                    cls.inject_loot_on_load_onto_rolestate(role_state, cls.loot_on_load)

                if cls.preroll_affordances is not None:
                    cls.inject_preroll_af_into_rolestate(role_state, cls.preroll_affordances)

                if cls.role_affordances is not None:
                    cls.inject_role_af_into_rolestate(role_state, cls.role_affordances)

                if cls.role_target_affordances is not None:
                    cls.inject_role_target_af_into_rolestate(role_state, cls.role_target_affordances)

    @staticmethod
    def inject_buffs_into_rolestate(role_state, buff_list):
        role_state._buffs += buff_list

        logger.info("Role State: {} now has {}".format(role_state, buff_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Role State: {} now has {}".format(role_state, buff_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Role State: {} now has {}".format(role_state, buff_list))

    @staticmethod
    def inject_loot_on_load_onto_rolestate(role_state, loot_on_load):
        role_state.loot_on_load += loot_on_load

        logger.info("Role State: {} now has {}".format(role_state, loot_on_load))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Role State: {} now has {}".format(role_state, loot_on_load))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Role State: {} now has {}".format(role_state, loot_on_load))

    @staticmethod
    def inject_preroll_af_into_rolestate(role_state, preroll_af):
        role_state.preroll_affordances += preroll_af

        logger.info("Role State: {} now has {}".format(role_state, preroll_af))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Role State: {} now has {}".format(role_state, preroll_af))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Role State: {} now has {}".format(role_state, preroll_af))

    @staticmethod
    def inject_role_af_into_rolestate(role_state, role_af):
        role_state.role_affordances += role_af

        logger.info("Role State: {} now has {}".format(role_state, role_af))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Role State: {} now has {}".format(role_state, role_af))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Role State: {} now has {}".format(role_state, role_af))

    @staticmethod
    def inject_role_target_af_into_rolestate(role_state, target_af):
        role_state.role_target_affordances += target_af

        logger.info("Role State: {} now has {}".format(role_state, target_af))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Role State: {} now has {}".format(role_state, target_af))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Role State: {} now has {}".format(role_state, target_af))
