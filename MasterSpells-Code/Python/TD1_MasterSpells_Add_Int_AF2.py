"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's MasterSpellsAlchemy

> Affordance Injector 2/3 [AF2/AF3] Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import services
from objects.definition_manager import DefinitionManager
import sims4.resources
from sims4.resources import Types
from sims4.common import Pack, is_available_pack
from sims4.log import Logger
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableList, Tunable, TunableReference, TunableEnumEntry, \
    TunableTuple

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Affordance Injector Version 2', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Affordance Injector Version 2', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Affordance Injector Version 2', default_owner='TwelfthDoctor1')

OBJECT_SIM = 14965
TERRAIN = 14982


class TD1MasterSpellsAffordanceInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                          manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'object_list': TunableList(
            description='List of objects that are to be injected.',
            tunable=Tunable(
                description='Object Instance ID of the Object.',
                tunable_type=int,
                default=None
            )
        ),
        'pack': TunableEnumEntry(
            description='The pack used to test.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        ),
        'affordances': TunableList(
            description='List of interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'affordance_reference': TunableReference(
            description='The affordance used to find the object lists should the object super affordances have that affordance.',
            manager=services.get_instance_manager(Types.INTERACTION),
            pack_safe=True,
            allow_none=True
        ),
        'sim_affordances': TunableList(
            description='List of sim interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'phone_affordances': TunableList(
            description='List of phone interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'terrain_affordances': TunableList(
            description='List of terrain interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'affordances_to_snippet': TunableList(
            description='List of mixer interactions that are to be added onto the Sim. Requires snippet_reference to function.',
            tunable=TunableReference(
                description='The mixer interaction to be injected.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'snippet_reference': TunableReference(
            description='The mixer snippet for mixer interactions to be injected into.',
            manager=services.get_instance_manager(Types.SNIPPET),
            pack_safe=True,
            allow_none=True
        )
    }

    __slots__ = ['object_list', 'pack', 'affordances', 'affordance_reference', 'phone_affordances',
                 'terrain_affordances', 'sim_affordances', 'affordances_to_snippet', 'snippet_reference']

    @classmethod
    def _tuning_loaded_callback(cls):
        if is_available_pack(cls.pack):
            if len(cls.sim_affordances) > 0:
                inject_sa_into_sim(cls.sim_affordances)

            if len(cls.phone_affordances) > 0:
                inject_sa_into_phone_sa(cls.phone_affordances)

            if len(cls.terrain_affordances) > 0:
                inject_sa_into_terrain(cls.terrain_affordances)

            if len(cls.object_list) > 0:
                for object_id in cls.object_list:
                    inject_sa_into_object(object_id, cls.affordances)

            if cls.affordance_reference is not None:
                inject_sa_through_sa_reference(cls.affordance_reference, cls.affordances)

            if len(cls.affordances_to_snippet) > 0 and cls.snippet_reference is not None:
                inject_mixer_int_through_mixer_snippet(cls.snippet_reference, cls.affordances_to_snippet)

            else:
                logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                            owner='TwelfthDoctor1')

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                           owner='TwelfthDoctor1')

                if master_logger is not None and master_logger is not False:
                    master_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                       owner='TwelfthDoctor1')
        else:
            logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                        owner='TwelfthDoctor1')

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                       owner='TwelfthDoctor1')

            if master_logger is not None and master_logger is not False:
                master_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                   owner='TwelfthDoctor1')


class TD1MasterSpellsAffordanceInjectorV3(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                            manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'affordance_injector': TunableList(
            description='Lists of affordances to be injected.',
            tunable=TunableTuple(
                description='The data to be injected.',
                object_list=TunableList(
                    description='List of objects that are to be injected.',
                    tunable=Tunable(
                        description='Object Instance ID of the Object.',
                        tunable_type=int,
                        default=None
                    )
                ),
                affordances=TunableList(
                    description='List of interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                affordance_reference=TunableReference(
                    description='The affordance used to find the object lists should the object super affordances have that affordance.',
                    manager=services.get_instance_manager(Types.INTERACTION),
                    pack_safe=True,
                    allow_none=True
                ),
                sim_affordances=TunableList(
                    description='List of sim interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                phone_affordances=TunableList(
                    description='List of phone interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                terrain_affordances=TunableList(
                    description='List of terrain interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                snippet_reference=TunableReference(
                    description='The snippet for interactions to be injected into. Applicable to MixerInteractions and Mixer Snippets.',
                    manager=services.get_instance_manager(Types.SNIPPET),
                    pack_safe=True,
                    allow_none=True
                ),
                affordances_to_snippet=TunableList(
                    description='List of mixer interactions that are to be added onto the Sim. Requires snippet_reference to function.',
                    tunable=TunableReference(
                        description='The mixer interaction to be injected.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                pack=TunableEnumEntry(
                    description='The pack used to test.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                ),
            )
        )
    }

    __slots__ = 'affordance_injector'

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.affordance_injector is not None:
            for injector_data in cls.affordance_injector:
                if is_available_pack(injector_data.pack):
                    if len(injector_data.sim_affordances) > 0:
                        inject_sa_into_sim(injector_data.sim_affordances)

                    if len(injector_data.phone_affordances) > 0:
                        inject_sa_into_phone_sa(injector_data.phone_affordances)

                    if len(injector_data.terrain_affordances) > 0:
                        inject_sa_into_terrain(injector_data.terrain_affordances)

                    if len(injector_data.object_list) > 0:
                        for object_id in injector_data.object_list:
                            inject_sa_into_object(object_id, injector_data.affordances)

                    if injector_data.affordance_reference is not None:
                        inject_sa_through_sa_reference(injector_data.affordance_reference, injector_data.affordances)

                    if len(injector_data.affordances_to_snippet) > 0 and injector_data.snippet_reference is not None:
                        inject_mixer_int_through_mixer_snippet(injector_data.snippet_reference, injector_data.affordances_to_snippet)

                    else:
                        logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                    owner='TwelfthDoctor1')

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                                   owner='TwelfthDoctor1')

                        if master_logger is not None and master_logger is not False:
                            master_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                               owner='TwelfthDoctor1')
                else:
                    logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                owner='TwelfthDoctor1')

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                           owner='TwelfthDoctor1')

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                           owner='TwelfthDoctor1')


def inject_sa_into_object(object_id, sa_tuning_list):
    """
    Injects Affordances into the Object ID inside the Object List.
    :param object_id:
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    object_sim = super(DefinitionManager, definition_manager).get(object_id)
    for affordance in sa_tuning_list:
        if not affordance in object_sim._super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        object_sim._super_affordances += tuple(sa_list)


def inject_sa_into_sim(sa_tuning_list):
    """
    Injects Affordances into the Sim Object (14965).
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    object_sim = super(DefinitionManager, definition_manager).get(OBJECT_SIM)
    for affordance in sa_tuning_list:
        if not affordance in object_sim._super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        object_sim._super_affordances += tuple(sa_list)


def inject_sa_into_phone_sa(sa_tuning_list):
    """
    Injects Affordances into the phone located inside the Sim Object (14965).
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    object_sim = super(DefinitionManager, definition_manager).get(OBJECT_SIM)
    for affordance in sa_tuning_list:
        if not affordance in object_sim._phone_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        object_sim._phone_affordances += tuple(sa_list)


def inject_sa_into_terrain(sa_tuning_list):
    """
    Injects Affordances into Terrain Object (14982).
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    obj_terrain = super(DefinitionManager, definition_manager).get(TERRAIN)
    for affordance in sa_tuning_list:
        if not affordance in obj_terrain._super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(obj_terrain, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(obj_terrain, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(obj_terrain, sa_list))

        obj_terrain._super_affordances += tuple(sa_list)


def inject_sa_through_sa_reference(sa_ref, sa_tuning_list):
    """
    Injects Affordances into any object that has the specified affordance to refer to search.
    :param sa_ref:
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    obj_list = []
    definition_manager = services.definition_manager()
    for tuning in definition_manager._tuned_classes.values():
        if hasattr(tuning, '_super_affordances') and sa_ref in tuning._super_affordances:
            obj_list.append(tuning)

    for affordance in sa_tuning_list:
        sa_list.append(affordance)

    if len(sa_list) > 0:
        for object_id in obj_list:
            logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if master_logger is not None and master_logger is not False:
                master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            object_id._super_affordances += tuple(sa_list)


def inject_mixer_int_through_mixer_snippet(mixer_reference, mixer_list):
    """
    Injects Affordances into a Snippet.
    Note: This can also be used on non-mixer affordances.
    :param mixer_reference:
    :param mixer_list:
    :return:
    """
    sa_list = []

    for affordance in mixer_list:
        if not affordance in mixer_reference.value:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(mixer_reference, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(mixer_reference, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(mixer_reference, sa_list))

        mixer_reference.value += tuple(sa_list)
