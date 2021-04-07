import event_testing
import interactions
import services
import statistics
from buffs.tunable import TunableBuffReference
from interactions import ParticipantType
from interactions.base import mixer_interaction
from interactions.base.basic import TunableBasicExtras
from buffs.buff import Buff
from interactions.utils.loot import LootActions
from interactions.utils.tunable import TunableAffordanceLinkList
from interactions.utils.tunable_provided_affordances import TunableProvidedAffordances
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableReference, TunableList, TunableTuple, OptionalTunable, \
    Tunable, TunableSet, TunableMapping
from sims4.tuning.tunable_base import GroupNames
from statistics import commodity


class TD1TMSLootBuffInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
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
        'add_test_sets': OptionalTunable(
            description='Tests to inject whether the referenced buff should be added',
            tunable=event_testing.tests.TunableTestSet(
                description='Test Set Reference: Check Buff.TDESC for full explanation'
            ),
            enabled_by_default=False,
            disabled_name='always_allowed',
            enabled_name='tests_set'
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
        'interactions': OptionalTunable(
            TunableTuple(
                weight=Tunable(
                    description=' The selection weight to apply to all interactions added by this buff. This takes the place of the SI weight that would be used on SuperInteractions.',
                    tunable_type=float,
                    default=1
                ),
                scored_commodity=commodity.Commodity.TunableReference(
                    description="The commodity that is scored when deciding whether or not to perform these interactions.  This takes the place of the commodity scoring for the SuperInteraction when Subaction Autonomy scores all of the SI's in the SI State.  If this is None, the default value of autonomy.autonomy_modes.SUBACTION_MOTIVE_UTILITY_FALLBACK_SCORE will be used.",
                    allow_none=True
                ),
                interaction_items=TunableAffordanceLinkList(
                    description='Mixer interactions to add to the Sim when this buff is active.',
                    class_restrictions=(mixer_interaction.MixerInteraction,)
                )
            ),
            tuning_group=GroupNames.ANIMATION
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
        )
    }

    __slots__ = ['loot_on_addition', 'loot_on_instance', 'loot_on_removal', 'buff_reference', 'add_test_sets',
                 'replace_loot_on_addition', 'replace_loot_on_instance', 'replace_loot_on_removal', 'trait_reference',
                 'buffs', 'interactions']

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.buff_reference is not None:
            if cls.loot_on_addition is not None:
                cls.add_loot_on_addition_to_buff(cls.buff_reference, cls.loot_on_addition, cls.replace_loot_on_addition)

            if cls.loot_on_instance is not None:
                cls.add_loot_on_instance_to_buff(cls.buff_reference, cls.loot_on_instance, cls.replace_loot_on_instance)

            if cls.loot_on_removal is not None:
                cls.add_loot_on_removal_to_buff(cls.buff_reference, cls.loot_on_removal, cls.replace_loot_on_removal)

            if cls.add_test_sets is not None:
                cls.add_test_sets_to_buff(cls.buff_reference, cls.add_test_sets)

            if cls.interactions is not None:
                cls.replace_interactions(cls.buff_reference, cls.interactions)

        if cls.trait_reference is not None:
            if cls.buffs is not None:
                cls.add_buffs_to_trait(cls.trait_reference, cls.buffs)

    # Injection Handling Section

    @staticmethod
    def add_loot_on_addition_to_buff(buff, loot_to_inject, replace):
        if replace is False:
            buff._loot_on_addition += loot_to_inject
        else:
            buff._loot_on_addition = loot_to_inject

    @staticmethod
    def add_loot_on_instance_to_buff(buff, loot_to_inject, replace):
        if replace is False:
            buff._loot_on_instance += loot_to_inject
        else:
            buff._loot_on_instance = loot_to_inject

    @staticmethod
    def add_loot_on_removal_to_buff(buff, loot_to_inject, replace):
        if replace is False:
            buff._loot_on_removal += loot_to_inject
        else:
            buff._loot_on_removal = loot_to_inject

    @staticmethod
    def add_test_sets_to_buff(buff, test_set):
        buff._add_test_set += test_set

    @staticmethod
    def add_buffs_to_trait(trait, buff_list):
        trait.buffs += buff_list

    @staticmethod
    def replace_interactions(buff, idle_interactions):
        buff.interactions = idle_interactions
