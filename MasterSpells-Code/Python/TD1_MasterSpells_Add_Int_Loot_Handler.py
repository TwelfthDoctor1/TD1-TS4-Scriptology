"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's MasterSpellsAlchemy

> Loot Interaction Injector Tuning

(C) Copyright TD1 & TWoCC 2020 - 2021
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import services
from animation.animation_overrides_liability import AnimationOverridesLiability
from buffs.tunable import RemoveBuffLiability
from careers.career_event_liabilities import CareerEventTravelLiability
from crafting.crafting_station_liability import CraftingStationLiability
from interactions.base.basic import TunableBasicExtras
from interactions.object_liabilities import TemporaryHiddenInventoryTransferLiability
from interactions.object_retrieval_liability import ObjectRetrievalLiability
from interactions.rabbit_hole import HideSimLiability
from interactions.utils.custom_camera_liability import CustomCameraLiability
from interactions.utils.lighting_liability import LightingLiability
from interactions.utils.route_goal_suppression_liability import RouteGoalSuppressionLiability
from interactions.utils.teleport_liability import TeleportLiability
from interactions.utils.temporary_state_change_liability import TemporaryStateChangeLiability
from interactions.utils.tunable import TimeoutLiability, TunableStatisticAdvertisements, SaveLockLiability, \
    TunableContinuation, CriticalPriorityLiability, GameSpeedLiability, PushAffordanceOnRouteFailLiability
from interactions.utils.user_cancelable_chain_liability import UserCancelableChainLiability
from interactions.vehicle_liabilities import VehicleLiability
from objects.components.game.game_challenge_liability import GameChallengeLiability
from pets.missing_pets_liability import MissingPetLiability
from postures.proxy_posture_owner_liability import ProxyPostureOwnerLiability
from restaurants.restaurant_liabilities import RestaurantDeliverFoodLiability
from sims.daycare import DaycareLiability
from sims.outfits.outfit_change import ChangeOutfitLiability
from sims4.common import Pack, is_available_pack
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableReference, TunableList, TunableVariant, \
    HasTunableSingletonFactory, AutoFactoryInit, TunableMapping, Tunable, TunableTuple, TunableEnumEntry
from sims4.tuning.tunable_base import GroupNames
from situations.situation_liabilities import CreateSituationLiability
from teleport.teleport_type_liability import TeleportStyleLiability
from whims.whims_tracker import HideWhimsLiability

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Loot Int Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Loot Int Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Loot Int Injector', default_owner='TwelfthDoctor1')


class TD1MasterSpellsIntLootInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'interaction_instance': TunableReference(
            description='The interaction to be injected',
            manager=services.affordance_manager(),
            allow_none=False,
            pack_safe=True
        ),
        'basic_extras': TunableBasicExtras(tuning_group=GroupNames.CORE),
        'basic_liabilities': TunableList(
            description="Use basic_liablities to tune a list of tunable liabilities. A liability is a construct that is associated to an interaction the moment it is added to the queue. This is different from\n            basic_content and basic_extras, which only affect interactions that\n            have started running.\n            \n            e.g. The 'timeout' tunable is a liability, because its behavior is\n            triggered the moment the SI is enqueued - by keeping track of how\n            long it takes for it to start running and canceling if the timeout\n            is hit.\n            ",
            tunable=TunableVariant(
                timeout=TimeoutLiability.TunableFactory(),
                save_lock=SaveLockLiability.TunableFactory(),
                teleport=TeleportLiability.TunableFactory(),
                lighting=LightingLiability.TunableFactory(),
                crafting_station=CraftingStationLiability.TunableFactory(),
                daycare=DaycareLiability.TunableFactory(),
                critical_priority=CriticalPriorityLiability.TunableFactory(),
                career_event_travel=CareerEventTravelLiability.TunableFactory(),
                game_speed=GameSpeedLiability.TunableFactory(),
                hide_whims=HideWhimsLiability.TunableFactory(),
                remove_buff=RemoveBuffLiability.TunableFactory(),
                push_affordance_on_route_fail=PushAffordanceOnRouteFailLiability.TunableFactory(),
                route_goal_suppression=RouteGoalSuppressionLiability.TunableFactory(),
                outfit_change=ChangeOutfitLiability.TunableFactory(),
                object_retrieval=ObjectRetrievalLiability.TunableFactory(),
                game_challenge_liability=GameChallengeLiability.TunableFactory(),
                restaurant_deliver_food_liability=RestaurantDeliverFoodLiability.TunableFactory(),
                teleport_style_liability=TeleportStyleLiability.TunableFactory(),
                animation_overrides=AnimationOverridesLiability.TunableFactory(),
                hide_sim_liability=HideSimLiability.TunableFactory(),
                user_cancelable_chain=UserCancelableChainLiability.TunableFactory(),
                create_situation=CreateSituationLiability.TunableFactory(),
                missing_pet=MissingPetLiability.TunableFactory(),
                proxy_posture_owner=ProxyPostureOwnerLiability.TunableFactory(),
                vehicles=VehicleLiability.TunableFactory(),
                temporary_state_change=TemporaryStateChangeLiability.TunableFactory(),
                temporary_hidden_inventory_transfer=TemporaryHiddenInventoryTransferLiability.TunableFactory(),
                enable_custom_camera=CustomCameraLiability.TunableFactory()),
            tuning_group=GroupNames.STATE
        ),
        'replace_basic_extras': Tunable(
            description='Modifier to determine should the interaction basic_extras be overridden.',
            tunable_type=bool,
            default=False
        ),
        'replace_basic_liabilities': Tunable(
            description='Modifier to determine should the interaction basic_liabilities be overridden.',
            tunable_type=bool,
            default=False
        ),
        'pack': TunableEnumEntry(
            description='The pack to test for.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        )
    }

    __slots__ = ['interaction_instance', 'tms_loot_on_addition', 'tms_loot_on_remove', 'basic_extras',
                 'basic_liabilities', 'replace_basic_extras', 'replace_basic_liabilities', 'pack']

    @classmethod
    def _tuning_loaded_callback(cls):
        if is_available_pack(cls.pack):
            if cls.basic_extras is not None:
                if cls.replace_basic_extras is False:
                    cls.interaction_instance.basic_extras += cls.basic_extras

                    logger.info('Replaced Basic Extras in {} with {}.'.format(cls.interaction_instance, cls.basic_extras))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Replaced Basic Extras in {} with {}.'.format(cls.interaction_instance, cls.basic_extras))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Replaced Basic Extras in {} with {}.'.format(cls.interaction_instance, cls.basic_extras))

                else:
                    cls.interaction_instance.basic_extras = cls.basic_extras

                    logger.info('Injecting Basic Extras {} into Interaction {}'.format(cls.basic_extras, cls.interaction_instance))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Injecting Basic Extras {} into Interaction {}'.format(cls.basic_extras, cls.interaction_instance))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Injecting Basic Extras {} into Interaction {}'.format(cls.basic_extras, cls.interaction_instance))

            if cls.basic_liabilities is not None:
                if cls.replace_basic_liabilities is False:
                    cls.interaction_instance.basic_liabilities += cls.basic_liabilities

                    logger.info('Replaced Basic Liabilities in {} with {}.'.format(cls.interaction_instance, cls.basic_liabilities))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Replaced Basic Liabilities in {} with {}.'.format(cls.interaction_instance, cls.basic_liabilities))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Replaced Basic Liabilities in {} with {}.'.format(cls.interaction_instance, cls.basic_liabilities))

                else:
                    cls.interaction_instance.basic_liabilities = cls.basic_liabilities

                    logger.info('Injecting Basic Liabilities {} into Interaction {}'.format(cls.basic_liabilities, cls.interaction_instance))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Injecting Basic Liabilities {} into Interaction {}'.format(cls.basic_liabilities, cls.interaction_instance))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Injecting Basic Liabilities {} into Interaction {}'.format(cls.basic_liabilities, cls.interaction_instance))


class TD1MasterSpellsIntLootInjectorV2(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                                       manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'interaction_injector': TunableList(
            description='Lists of interaction basics to be injected.',
            tunable=TunableTuple(
                description='Data to be injected into the specified interaction.',
                interaction_instance=TunableList(
                    description='A lists of interactions to be injected.',
                    tunable=TunableReference(
                        description='The interaction to be injected',
                        manager=services.affordance_manager(),
                        allow_none=False,
                        pack_safe=True
                    ),
                ),
                basic_extras=TunableBasicExtras(tuning_group=GroupNames.CORE),
                basic_liabilities=TunableList(
                    description="Use basic_liablities to tune a list of tunable liabilities. A liability is a construct that is associated to an interaction the moment it is added to the queue. This is different from\n            basic_content and basic_extras, which only affect interactions that\n            have started running.\n            \n            e.g. The 'timeout' tunable is a liability, because its behavior is\n            triggered the moment the SI is enqueued - by keeping track of how\n            long it takes for it to start running and canceling if the timeout\n            is hit.\n            ",
                    tunable=TunableVariant(
                        timeout=TimeoutLiability.TunableFactory(),
                        save_lock=SaveLockLiability.TunableFactory(),
                        teleport=TeleportLiability.TunableFactory(),
                        lighting=LightingLiability.TunableFactory(),
                        crafting_station=CraftingStationLiability.TunableFactory(),
                        daycare=DaycareLiability.TunableFactory(),
                        critical_priority=CriticalPriorityLiability.TunableFactory(),
                        career_event_travel=CareerEventTravelLiability.TunableFactory(),
                        game_speed=GameSpeedLiability.TunableFactory(),
                        hide_whims=HideWhimsLiability.TunableFactory(),
                        remove_buff=RemoveBuffLiability.TunableFactory(),
                        push_affordance_on_route_fail=PushAffordanceOnRouteFailLiability.TunableFactory(),
                        route_goal_suppression=RouteGoalSuppressionLiability.TunableFactory(),
                        outfit_change=ChangeOutfitLiability.TunableFactory(),
                        object_retrieval=ObjectRetrievalLiability.TunableFactory(),
                        game_challenge_liability=GameChallengeLiability.TunableFactory(),
                        restaurant_deliver_food_liability=RestaurantDeliverFoodLiability.TunableFactory(),
                        teleport_style_liability=TeleportStyleLiability.TunableFactory(),
                        animation_overrides=AnimationOverridesLiability.TunableFactory(),
                        hide_sim_liability=HideSimLiability.TunableFactory(),
                        user_cancelable_chain=UserCancelableChainLiability.TunableFactory(),
                        create_situation=CreateSituationLiability.TunableFactory(),
                        missing_pet=MissingPetLiability.TunableFactory(),
                        proxy_posture_owner=ProxyPostureOwnerLiability.TunableFactory(),
                        vehicles=VehicleLiability.TunableFactory(),
                        temporary_state_change=TemporaryStateChangeLiability.TunableFactory(),
                        temporary_hidden_inventory_transfer=TemporaryHiddenInventoryTransferLiability.TunableFactory(),
                        enable_custom_camera=CustomCameraLiability.TunableFactory()),
                    tuning_group=GroupNames.STATE
                ),
                replace_basic_extras=Tunable(
                    description='Modifier to determine should the interaction basic_extras be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                replace_basic_liabilities=Tunable(
                    description='Modifier to determine should the interaction basic_liabilities be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            ),
        )
    }

    __slots__ = 'interaction_injector'

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.interaction_injector is not None:
            for injector_data in cls.interaction_injector:
                if is_available_pack(injector_data.pack):
                    if injector_data.interaction_instance is not None:
                        for interaction in injector_data.interaction_instance:
                            if injector_data.basic_extras is not None:
                                if injector_data.replace_basic_extras is False:
                                    interaction.basic_extras += injector_data.basic_extras

                                    logger.info(
                                        'Replaced Basic Extras in {} with {}.'.format(interaction,
                                                                                      injector_data.basic_extras))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Replaced Basic Extras in {} with {}.'.format(interaction,
                                                                                          injector_data.basic_extras))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info('Replaced Basic Extras in {} with {}.'.format(
                                            injector_data.interaction_instance,
                                            injector_data.basic_extras))

                                else:
                                    interaction.basic_extras = injector_data.basic_extras

                                    logger.info(
                                        'Injecting Basic Extras {} into Interaction {}'.format(injector_data.basic_extras,
                                                                                               interaction))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Injecting Basic Extras {} into Interaction {}'.format(
                                                injector_data.basic_extras,
                                                interaction))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info('Injecting Basic Extras {} into Interaction {}'.format(
                                            injector_data.basic_extras,
                                            interaction))

                            if injector_data.basic_liabilities is not None:
                                if injector_data.replace_basic_liabilities is False:
                                    interaction.basic_liabilities += injector_data.basic_liabilities

                                    logger.info('Replaced Basic Liabilities in {} with {}.'.format(interaction,
                                                                                                   injector_data.basic_liabilities))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Replaced Basic Liabilities in {} with {}.'.format(interaction,
                                                                                               injector_data.basic_liabilities))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info(
                                            'Replaced Basic Liabilities in {} with {}.'.format(interaction,
                                                                                               injector_data.basic_liabilities))

                                else:
                                    injector_data.interaction_instance.basic_liabilities = injector_data.basic_liabilities

                                    logger.info('Injecting Basic Liabilities {} into Interaction {}'.format(
                                        injector_data.basic_liabilities,
                                        interaction))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Injecting Basic Liabilities {} into Interaction {}'.format(
                                                injector_data.basic_liabilities,
                                                interaction))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info(
                                            'Injecting Basic Liabilities {} into Interaction {}'.format(
                                                injector_data.basic_liabilities,
                                                interaction))

