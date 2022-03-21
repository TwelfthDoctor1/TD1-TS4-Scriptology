import services
from bucks.bucks_commands import get_bucks_tracker, get_bucks_types_without_invalid_gen, get_short_buck_type
from bucks.bucks_enums import BucksType
from bucks.bucks_utils import BucksUtils
from distributor.shared_messages import IconInfoData
from eco_footprint.eco_footprint_tuning import EcoFootprintTunables
from event_testing.resolver import SingleSimResolver
from protocolbuffers import Consts_pb2
from server_commands.argument_helpers import get_optional_target, OptionalTargetParam, OptionalSimInfoParam
from sims4.collections import FrozenAttributeDict, AttributeDict
from sims4.commands import Command, CommandType, CheatOutput, execute
from sims4.common import Pack
from sims4.localization import LocalizationHelperTuning
from sims4.resources import get_resource_key, Types
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from ui.ui_text_input import UiTextInput
from sims4.localization import _create_localized_string


class MasterSpellsEcoControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'MasterSpellsEcoControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('masterspells.modify_street_eco_footprint', command_type=CommandType.Live, pack=Pack.EP09)
def modify_street_eco_footprint(opt_sim: OptionalTargetParam = None, _connection=None, reason_for_modification=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)

    street = services.street_service()
    current_street = street.get_provider(services.current_street())

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        number_to_modify = float(dialog.text_input_responses.get("input_number"))
        output("User typed '{}'".format(number_to_modify))

        if current_street is not None:

            if -500 <= number_to_modify <= 500:

                output('Eco Footprint: {} will be the result after this operation.'.format(number_to_modify))

                current_street.force_set_eco_footprint_value(number_to_modify, True)

                if -500 <= number_to_modify <= -400:

                    eco_state = "Green"

                    loot_type = services.get_instance_manager(Types.ACTION).get(9865243489992686587)
                    resolver = SingleSimResolver(sim_info)
                    loot_type.apply_to_resolver(resolver)

                elif 400 <= number_to_modify <= 500:

                    eco_state = "Industrial"

                    loot_type = services.get_instance_manager(Types.ACTION).get(11472440913130947277)
                    resolver = SingleSimResolver(sim_info)
                    loot_type.apply_to_resolver(resolver)

                else:

                    eco_state = "Neutral"

                success_title = lambda **_: _create_localized_string(0x7F632D0A)  # LocalizationHelperTuning.get_raw_text("Eco Footprint Modification Success")
                success_text = lambda **_: _create_localized_string(0x1EBCCCD3, str(eco_state), number_to_modify)  # LocalizationHelperTuning.get_raw_text("The current Eco Footprint is now: " + str(eco_state) + " at Commodity Value: " + str(number_to_modify))

                notification_success = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=success_text,
                    title=success_title
                )
                notification_success.show_dialog()

            else:

                output('Eco Footprint: {} is out of range from -500 to 500.'.format(number_to_modify))

                failure_title = lambda **_: _create_localized_string(0x1BEDA3C1)  # LocalizationHelperTuning.get_raw_text("Modification Failure")
                failure_text = lambda **_: _create_localized_string(0x63D07BFA)  # LocalizationHelperTuning.get_raw_text("Eco Footprint not within specified range.")

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('Street Not Found.')

            return

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: _create_localized_string(0x45101872)  # LocalizationHelperTuning.get_raw_text("Modify Eco Footprint")
    localized_text = lambda **_: _create_localized_string(0x809F95E2)  # LocalizationHelperTuning.get_raw_text("Indicate the value of the Eco Footprint that is to be modified:\n<b>Green State: -500\nNeutral State: 0\nIndustrial State: 500</b>")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_eco_footprint = UiTextInput(sort_order=0, restricted_characters=None)
    input_eco_footprint.default_text = None
    input_eco_footprint.title = None
    input_eco_footprint.max_length = 30
    input_eco_footprint.initial_value = localized_initial_value
    input_eco_footprint.length_restriction = MasterSpellsEcoControl_TextInputLength()
    input_eco_footprint.check_profanity = False
    input_eco_footprint.height = False

    inputs = AttributeDict({'input_number': input_eco_footprint})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")


@Command('masterspells.modify_street_eco_footprint_failure', command_type=CommandType.Live, pack=Pack.EP09)
def modify_street_eco_footprint_failure(opt_sim: OptionalTargetParam = None, _connection=None, reason_for_modification=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)

    street = services.street_service()
    current_street = street.get_provider(services.current_street())

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        number_to_modify = float(dialog.text_input_responses.get("input_number"))

        number_to_modify = -number_to_modify  # Inverted for Spell Failure

        output("User typed '{}'".format(number_to_modify))

        if current_street is not None:

            if -500 <= number_to_modify <= 500:

                output('Eco Footprint: {} will be the result after this operation.'.format(number_to_modify))

                current_street.force_set_eco_footprint_value(number_to_modify, True)

                if -500 <= number_to_modify <= -400:

                    eco_state = "Green"

                    loot_type = services.get_instance_manager(Types.ACTION).get(9865243489992686587)
                    resolver = SingleSimResolver(sim_info)
                    loot_type.apply_to_resolver(resolver)

                elif 400 <= number_to_modify <= 500:

                    eco_state = "Industrial"

                    loot_type = services.get_instance_manager(Types.ACTION).get(11472440913130947277)
                    resolver = SingleSimResolver(sim_info)
                    loot_type.apply_to_resolver(resolver)

                else:

                    eco_state = "Neutral"

                success_title = lambda **_: _create_localized_string(0x7F632D0A)  # LocalizationHelperTuning.get_raw_text("Eco Footprint Modification Success")
                success_text = lambda **_: _create_localized_string(0x1EBCCCD3, str(eco_state), number_to_modify)  # LocalizationHelperTuning.get_raw_text("The current Eco Footprint is now: " + str(eco_state) + " at Commodity Value: " + str(number_to_modify))

                notification_success = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=success_text,
                    title=success_title
                )
                notification_success.show_dialog()

            else:

                output('Eco Footprint: {} is out of range from -500 to 500.'.format(number_to_modify))

                failure_title = lambda **_: _create_localized_string(0x1BEDA3C1)  # LocalizationHelperTuning.get_raw_text("Modification Failure")
                failure_text = lambda **_: _create_localized_string(0x63D07BFA)  # LocalizationHelperTuning.get_raw_text("Eco Footprint not within specified range.")

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('Street Not Found.')

            return

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: _create_localized_string(0x45101872)  # LocalizationHelperTuning.get_raw_text("Modify Eco Footprint")
    localized_text = lambda **_: _create_localized_string(0x809F95E2)  # LocalizationHelperTuning.get_raw_text("Indicate the value of the Eco Footprint that is to be modified:\n<b>Green State: -500\nNeutral State: 0\nIndustrial State: 500</b>")
    localized_initial_value = lambda **_: LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_eco_footprint = UiTextInput(sort_order=0, restricted_characters=None)
    input_eco_footprint.default_text = None
    input_eco_footprint.title = None
    input_eco_footprint.max_length = 30
    input_eco_footprint.initial_value = localized_initial_value
    input_eco_footprint.length_restriction = MasterSpellsEcoControl_TextInputLength()
    input_eco_footprint.check_profanity = False
    input_eco_footprint.height = False

    inputs = AttributeDict({'input_number': input_eco_footprint})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text, title=localized_title, text_inputs=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")
