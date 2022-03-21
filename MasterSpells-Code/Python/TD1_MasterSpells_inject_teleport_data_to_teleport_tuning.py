from interactions.utils.animation_reference import TunableAnimationReference
from sims4.tuning.geometric import TunableDistanceSquared
from sims4.tuning.tunable import TunableMapping, TunableEnumEntry, TunableTuple, Tunable, TunableReference, \
    TunableRange, OptionalTunable, TunableSimMinute, TunableList
from teleport.teleport_enums import TeleportStyle
from tunable_multiplier import TunableMultiplier
from tunable_utils.tested_list import TunableTestedList
from vfx import PlayEffect
import services
import sims4
from sims4.log import Logger
from teleport.teleport_tuning import TeleportTuning
from sims4.collections import FrozenAttributeDict
from sims4.resources import Types

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Teleport Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Teleport Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Teleport Injector')


class TD1MasterSpellsTeleportTuning:
    TELEPORT_DATA_MAPPING_TO_INJECT = TunableMapping(
        description='\n        A mapping from a a teleport style to the animation, xevt and vfx data\n        that the Sim will use when a teleport is triggered.\n        ',
        key_type=TunableEnumEntry(description='\n            Teleport style.\n            ', tunable_type=TeleportStyle,
                                  default=TeleportStyle.NONE, pack_safe=True, invalid_enums=(TeleportStyle.NONE,)),
        value_type=TunableTuple(
            description='\n            Animation and vfx data data to be used when the teleport is \n            triggered.\n            ',
            animation_outcomes=TunableList(
                description='\n                One of these animations will be played when the teleport\n                happens, and weights + modifiers can be used to determine\n                exactly which animation is played based on tests.\n                ',
                tunable=TunableTuple(
                    description='\n                    A pairing of animation and weights that determine which\n                    animation is played when using this teleport style.  Any\n                    tests in the multipliers will be using the context from\n                    the interaction that plays the teleportStyle.\n                    ',
                    animation=TunableAnimationReference(
                        description='\n                        Reference of the animation to be played when the teleport is\n                        triggered.\n                        ',
                        pack_safe=True, callback=None), weight=TunableMultiplier.TunableFactory(
                        description='\n                        A tunable list of tests and multipliers to apply to the \n                        weight of the animation that is selected for the teleport.\n                        '))),
            start_teleport_vfx_xevt=Tunable(
                description='\n                Xevent when the Sim starts teleporting to play the fade out\n                VFX.\n                ',
                tunable_type=int, default=100), start_teleport_fade_sim_xevt=Tunable(
                description='\n                Xevent when the sim starts teleporting to start the fading\n                of the Sim.\n                ',
                tunable_type=int, default=100), fade_out_effect=OptionalTunable(
                description='\n                If enabled, play an additional VFX on the specified \n                fade_out_xevt when fading out the Sim.\n                ',
                tunable=PlayEffect.TunableFactory(
                    description='\n                    The effect to play when the Sim fades out before actual\n                    changing its position.\n                    This effect will not be parented to the Sim, but instead will\n                    play on the bone position without attachment.  This will\n                    guarantee the VFX will not become invisible as the Sim \n                    disappears.\n                    i.e. Vampire bat teleport spawns VFX on the Sims position\n                    '),
                enabled_name='play_effect', disabled_name='no_effect'), tested_fade_out_effect=TunableTestedList(
                description='\n                A list of possible fade out effects to play tested against\n                the Sim that is teleporting.\n                ',
                tunable_type=PlayEffect.TunableFactory(
                    description='\n                    The effect to play when the Sim fades out before actual\n                    changing its position.\n                    This effect will not be parented to the Sim, but instead will\n                    play on the bone position without attachment.  This will\n                    guarantee the VFX will not become invisible as the Sim \n                    disappears.\n                    i.e. Vampire bat teleport spawns VFX on the Sims position\n                    ')),
            teleport_xevt=Tunable(
                description='\n                Xevent where the teleport should happen.\n                ',
                tunable_type=int, default=100), teleport_effect=OptionalTunable(
                description='\n                If enabled, play an additional VFX on the specified \n                teleport_xevt when the teleport (actual movement of the \n                position of the Sim) happens.\n                ',
                tunable=PlayEffect.TunableFactory(
                    description='\n                    The effect to play when the Sim is teleported.\n                    '),
                enabled_name='play_effect', disabled_name='no_effect'), teleport_min_distance=TunableDistanceSquared(
                description='\n                Minimum distance between the Sim and its target to trigger\n                a teleport.  If the distance is lower than this value, the\n                Sim will run a normal route.\n                ',
                default=5.0), teleport_cost=OptionalTunable(
                description='\n                If enabled, the teleport will have an statistic cost every\n                time its triggered. \n                ',
                tunable=TunableTuple(
                    description='\n                    Cost and statistic to charge for a teleport event.\n                    ',
                    teleport_statistic=TunableReference(
                        description='\n                        The statistic we are operating on when a teleport \n                        happens.\n                        ',
                        manager=services.get_instance_manager(sims4.resources.Types.STATISTIC), pack_safe=True),
                    cost=TunableRange(
                        description='\n                        On teleport, subtract the teleport_statistic by this\n                        amount. \n                        ',
                        tunable_type=int, default=1, minimum=0), cost_is_additive=Tunable(
                        description='\n                        If checked, the cost is additive.  Rather than deducting the cost, it will be added to\n                        the specified teleport statistic.  Additionally, cost will be checked against the max value\n                        of the statistic rather than the minimum value when determining if the cost is affordable\n                        ',
                        tunable_type=bool, default=False)), disabled_name='no_teleport_cost',
                enabled_name='specify_cost'), fade_duration=TunableSimMinute(
                description='\n                Default fade time (in sim minutes) for the fading of the Sim\n                to happen.',
                default=0.5)))


def add_teleport_data_to_teleport_tuning(self):
    if TD1MasterSpellsTeleportTuning.TELEPORT_DATA_MAPPING_TO_INJECT is not None:
        logger.info('Module Print: {}'.format(TD1MasterSpellsTeleportTuning.TELEPORT_DATA_MAPPING_TO_INJECT), owner="TwelfthDoctor1")

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('Module Print: {}'.format(TD1MasterSpellsTeleportTuning.TELEPORT_DATA_MAPPING_TO_INJECT), owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info('Module Print: {}'.format(TD1MasterSpellsTeleportTuning.TELEPORT_DATA_MAPPING_TO_INJECT), owner="TwelfthDoctor1")

        TeleportTuning.TELEPORT_DATA_MAPPING = FrozenAttributeDict(
            {**dict(TeleportTuning.TELEPORT_DATA_MAPPING), **TD1MasterSpellsTeleportTuning.TELEPORT_DATA_MAPPING_TO_INJECT}
        )
        logger.info('Module Injection: {}'.format(TeleportTuning.TELEPORT_DATA_MAPPING), owner="TwelfthDoctor1")

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('Module Injection: {}'.format(TeleportTuning.TELEPORT_DATA_MAPPING), owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info('Module Injection: {}'.format(TeleportTuning.TELEPORT_DATA_MAPPING), owner="TwelfthDoctor1")


services.get_instance_manager(Types.TUNING).add_on_load_complete(add_teleport_data_to_teleport_tuning)
