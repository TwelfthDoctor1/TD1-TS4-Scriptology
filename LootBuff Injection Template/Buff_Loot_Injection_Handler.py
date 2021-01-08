import services
from buffs.tunable import TunableBuffReference
from interactions.base.basic import TunableBasicExtras
from buffs.buff import Buff
from interactions.utils.loot import LootActions
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, TunableReference, TunableList, TunableTuple;


class LootBuffInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                       manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'buff_reference': TunableReference(
            description='The buff for the loots to inject into, only ONE buff can be used',
            manager=services.get_instance_manager(Types.BUFF),
            pack_safe=True,
            allow_none=False
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
    }

    __slots__ = ['buff_reference', 'loot_on_addition', 'loot_on_instance', 'loot_on_removal']

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.loot_on_addition is not None:
            cls.add_loot_on_addition_to_buff(cls.buff_reference, cls.loot_on_addition)

        if cls.loot_on_instance is not None:
            cls.add_loot_on_instance_to_buff(cls.buff_reference, cls.loot_on_instance)

        if cls.loot_on_removal is not None:
            cls.add_loot_on_removal_to_buff(cls.buff_reference, cls.loot_on_removal)

    # Injection Handling Section
    @staticmethod
    def add_loot_on_addition_to_buff(buff, loot_to_inject):
        buff._loot_on_addition += loot_to_inject

    @staticmethod
    def add_loot_on_instance_to_buff(buff, loot_to_inject):
        buff._loot_on_instance += loot_to_inject

    @staticmethod
    def add_loot_on_removal_to_buff(buff, loot_to_inject):
        buff._loot_on_removal += loot_to_inject
