import event_testing
import services
from buffs.tunable import TunableBuffReference
from interactions.base.basic import TunableBasicExtras
from buffs.buff import Buff
from interactions.utils.loot import LootActions
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableReference, TunableList, TunableTuple, OptionalTunable, \
    TunableVariant, TunableEnumEntry, Tunable
from situations.additional_situation_sources import HolidayWalkbys, ZoneModifierSituations, NarrativeSituations
from situations.situation_curve import SituationCurve, ShiftlessDesiredSituations
from venues.scheduling_zone_director import SituationShiftStrictness

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 ZoneDirector Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 ZoneDirector Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 ZoneDirector Injector')


class TD1MasterSpellsZoneDirectorInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass, manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'zone_director_reference': TunableReference(
            description='The buff for the loots to inject into, only ONE buff can be used',
            manager=services.get_instance_manager(Types.ZONE_DIRECTOR),
            pack_safe=True,
            allow_none=False
        ),
        'situation_shifts': TunableList(
            description='A list of situation distributions and their strictness rules.',
            tunable=TunableTuple(
                shift_curve=TunableVariant(
                    curve_based=SituationCurve.TunableFactory(
                        get_create_params={'user_facing': True}
                    ),
                    shiftless=ShiftlessDesiredSituations.TunableFactory(
                        get_create_params={'user_facing': True}
                    ),
                    default='curve_based'
                ),
                shift_strictness=TunableEnumEntry(
                    description='\n                    Determine how situations on shift will be handled on shift change. Example: I want 3 customers between 10-12.  then after 12 I want only 1.  Having this checked will allow 3 customers to stay and will let situation duration kick the sim out when appropriate.  This will not create new situations if over the cap.',
                    tunable_type=SituationShiftStrictness,
                    default=SituationShiftStrictness.DESTROY
                ),
                additional_sources=TunableList(
                    description='Any additional sources of NPCs that we want to use to add into the possible situations of this shift curve.',
                    tunable=TunableVariant(
                        description='The different additional situation sources that we want to use to get additional situation possibilities that can be chosen.',
                        holiday=HolidayWalkbys.TunableFactory(),
                        zone_modifier=ZoneModifierSituations.TunableFactory(),
                        narrative=NarrativeSituations.TunableFactory(),
                        default='holiday'
                    )
                ),
                count_based_on_expected_sims=Tunable(
                    description='If checked then we will count based on the number of Sims that are expected to be in the Situation rather than the number of situations.',
                    tunable_type=bool,
                    default=False
                )
            )
        ),
    }

    __slots__ = ['zone_director_reference', 'situation_shifts']

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.situation_shifts is not None:
            cls.add_situation_shifts_to_zone_director(cls.zone_director_reference, cls.situation_shifts)

    # Injection Handling Section

    @staticmethod
    def add_situation_shifts_to_zone_director(zone_director, situation_shifts):
        zone_director.situation_shifts += situation_shifts

        logger.info("Zone Director: {} now has {}.".format(zone_director, situation_shifts))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Zone Director: {} now has {}.".format(zone_director, situation_shifts))

        if master_logger is not None and master_logger is not False:
            master_logger.info("Zone Director: {} now has {}.".format(zone_director, situation_shifts))
