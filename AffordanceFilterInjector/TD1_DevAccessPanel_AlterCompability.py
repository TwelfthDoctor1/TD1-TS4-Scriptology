import services
from _sims4_collections import frozendict
from interactions.interaction_cancel_compatibility import InteractionCancelReason, InteractionCancelCompatibility
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableMapping, TunableEnumEntry, HasTunableReference, TunableList, TunableReference, \
    TunableTuple
from snippets import TunableAffordanceFilterSnippet, TunableAffordanceListReference


class TD1AffordanceFilterInjector(HasTunableReference, metaclass=HashedTunedInstanceMetaclass,
                               manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        "affordance_filter_injector": TunableMapping(
            description="The Affordance Filter Injector Data.",
            key_name="buffs",
            key_type=TunableList(
                description="A list of buffs that are to be injected.",
                tunable=TunableReference(
                    description="The buff that is to be injected.",
                    manager=services.get_instance_manager(Types.BUFF),
                    pack_safe=True,
                    allow_none=False
                )
            ),
            value_name="injection_data",
            value_type=TunableTuple(
                exclude_affordances=TunableList(
                    description="A list of affordances that are to be excluded.",
                    tunable=TunableReference(
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                exclude_list=TunableList(
                    description="A list of AffordanceLists that contains blacklisted affordances.",
                    tunable=TunableAffordanceListReference()
                ),
                include_affordances=TunableList(
                    description="A list of affordances that are to be allowed.",
                    tunable=TunableReference(
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                include_list=TunableList(
                    description="A list of AffordanceLists that contains whitelisted affordances.",
                    tunable=TunableAffordanceListReference()
                )
            )

        )

    }

    __slots__ = ["affordance_filter_injector"]

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.affordance_filter_injector is not None:
            for (buffs, injection_data) in cls.affordance_filter_injector.items():
                if buffs is not None:
                    for buff in buffs:
                        game_effect_modifiers_slots = buff.game_effect_modifier._tuned_values
                        game_effect_modifiers_values = game_effect_modifiers_slots._game_effect_modifiers

                        if len(injection_data.include_affordances) > 0:
                            for index, element in enumerate(game_effect_modifiers_values):
                                provided_affordance = getattr(element, '_provided_affordance_compatibility', None)
                                if not provided_affordance:
                                    continue
                                provided_affordance_slots = provided_affordance._tuned_values
                                default_inclusion_slots = provided_affordance_slots.default_inclusion

                                include_affordances_list = list(default_inclusion_slots.include_affordances)
                                include_affordances_list.append(injection_data.include_affordances)

                                default_inclusion_slots = default_inclusion_slots.clone_with_overrides(
                                    include_affordances=tuple(include_affordances_list)
                                )
                                provided_affordance_slots = provided_affordance_slots.clone_with_overrides(
                                    default_inclusion=default_inclusion_slots
                                )
                                game_effect_modifiers_values[
                                    index]._provided_affordance_compatibility._tuned_values = provided_affordance_slots

                                game_effect_modifiers_slots = game_effect_modifiers_slots.clone_with_overrides(
                                    _game_effect_modifiers=game_effect_modifiers_values
                                )
                                buff.game_effect_modifier._tuned_values = game_effect_modifiers_slots

                        if len(injection_data.include_list) > 0:
                            for index, element in enumerate(game_effect_modifiers_values):
                                provided_affordance = getattr(element, '_provided_affordance_compatibility', None)
                                if not provided_affordance:
                                    continue
                                provided_affordance_slots = provided_affordance._tuned_values
                                default_inclusion_slots = provided_affordance_slots.default_inclusion

                                include_lists_list = list(default_inclusion_slots.include_lists)
                                include_lists_list.append(injection_data.include_list)

                                default_inclusion_slots = default_inclusion_slots.clone_with_overrides(
                                    include_lists=tuple(include_lists_list)
                                )
                                provided_affordance_slots = provided_affordance_slots.clone_with_overrides(
                                    default_inclusion=default_inclusion_slots
                                )
                                game_effect_modifiers_values[
                                    index]._provided_affordance_compatibility._tuned_values = provided_affordance_slots

                                game_effect_modifiers_slots = game_effect_modifiers_slots.clone_with_overrides(
                                    _game_effect_modifiers=game_effect_modifiers_values
                                )
                                buff.game_effect_modifier._tuned_values = game_effect_modifiers_slots

                        if len(injection_data.exclude_affordances) > 0:
                            for index, element in enumerate(game_effect_modifiers_values):
                                provided_affordance = getattr(element, '_provided_affordance_compatibility', None)
                                if not provided_affordance:
                                    continue
                                provided_affordance_slots = provided_affordance._tuned_values
                                default_inclusion_slots = provided_affordance_slots.default_inclusion

                                exclude_affordances_list = list(default_inclusion_slots.exclude_affordances)
                                exclude_affordances_list.append(injection_data.exclude_affordances)

                                default_inclusion_slots = default_inclusion_slots.clone_with_overrides(
                                    exclude_affordances=tuple(exclude_affordances_list)
                                )
                                provided_affordance_slots = provided_affordance_slots.clone_with_overrides(
                                    default_inclusion=default_inclusion_slots
                                )
                                game_effect_modifiers_values[
                                    index]._provided_affordance_compatibility._tuned_values = provided_affordance_slots

                                game_effect_modifiers_slots = game_effect_modifiers_slots.clone_with_overrides(
                                    _game_effect_modifiers=game_effect_modifiers_values
                                )
                                buff.game_effect_modifier._tuned_values = game_effect_modifiers_slots

                        if len(injection_data.exclude_list) > 0:
                            for index, element in enumerate(game_effect_modifiers_values):
                                provided_affordance = getattr(element, '_provided_affordance_compatibility', None)
                                if not provided_affordance:
                                    continue
                                provided_affordance_slots = provided_affordance._tuned_values
                                default_inclusion_slots = provided_affordance_slots.default_inclusion

                                exclude_lists_list = list(default_inclusion_slots.exclude_lists)
                                exclude_lists_list.append(injection_data.exclude_list)

                                default_inclusion_slots = default_inclusion_slots.clone_with_overrides(
                                    exclude_lists=tuple(exclude_lists_list)
                                )
                                provided_affordance_slots = provided_affordance_slots.clone_with_overrides(
                                    default_inclusion=default_inclusion_slots
                                )
                                game_effect_modifiers_values[
                                    index]._provided_affordance_compatibility._tuned_values = provided_affordance_slots

                                game_effect_modifiers_slots = game_effect_modifiers_slots.clone_with_overrides(
                                    _game_effect_modifiers=game_effect_modifiers_values
                                )
                                buff.game_effect_modifier._tuned_values = game_effect_modifiers_slots


'''
# Original Code by Kuttoe

import services
from sims4.resources import get_resource_key, Types

buff_ids = (10094, 285810)
interaction_ids = (130218,)


def InjectProvidedAffordances(_):
    buff_manager = services.get_instance_manager(Types.BUFF)
    interaction_manager = services.get_instance_manager(Types.INTERACTION)
    for buff_id in buff_ids:
        loaded_buff = buff_manager.get(get_resource_key(buff_id, Types.BUFF))
        if not loaded_buff:
            continue
        for interaction in interaction_ids:
            loaded_interaction = interaction_manager.get(get_resource_key(interaction, Types.INTERACTION))
            if not loaded_interaction:
                continue
            game_effect_modifiers_slots = loaded_buff.game_effect_modifier._tuned_values
            game_effect_modifiers_values = game_effect_modifiers_slots._game_effect_modifiers
            for index, element in enumerate(game_effect_modifiers_values):
                provided_affordance = getattr(element, '_provided_affordance_compatibility', None)
                if not provided_affordance:
                    continue
                provided_affordance_slots = provided_affordance._tuned_values
                default_inclusion_slots = provided_affordance_slots.default_inclusion
                include_affordances_list = list(default_inclusion_slots.include_affordances)
                include_affordances_list.append(loaded_interaction)
                default_inclusion_slots = default_inclusion_slots.clone_with_overrides(
                    include_affordances=tuple(include_affordances_list)
                )
                provided_affordance_slots = provided_affordance_slots.clone_with_overrides(
                    default_inclusion=default_inclusion_slots
                )
                game_effect_modifiers_values[index]._provided_affordance_compatibility._tuned_values = provided_affordance_slots

                game_effect_modifiers_slots = game_effect_modifiers_slots.clone_with_overrides(
                    _game_effect_modifiers=game_effect_modifiers_values
                )
                loaded_buff.game_effect_modifier._tuned_values = game_effect_modifiers_slots


services.get_instance_manager(Types.INTERACTION).add_on_load_complete(InjectProvidedAffordances)
'''
