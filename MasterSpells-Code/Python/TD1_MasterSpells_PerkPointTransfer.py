import services
from bucks.bucks_commands import get_bucks_tracker, get_bucks_types_without_invalid_gen, get_short_buck_type
from bucks.bucks_utils import BucksUtils
from distributor.shared_messages import IconInfoData
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


class PerkPointControl_TextInputLength(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = 'PerkPointControl_TextInputLength'

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 30
        msg.min_length = 1


@Command('masterspells.perkpointtransfer', pack=Pack.GP08, command_type=CommandType.Live)
def perk_point_transfer(actor_sim:int=None, target_sim:int=None, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()

    temp_bucks_type = 49153

    tracker_actor = get_bucks_tracker(temp_bucks_type, actor_sim, _connection, add_if_none=True)
    tracker_target = get_bucks_tracker(temp_bucks_type, target_sim, _connection, add_if_none=True)

    if tracker_actor is None:
        return False
    if tracker_target is None:
        return False

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        point_to_transfer = int(dialog.text_input_responses.get("input_number"))
        output("User typed '{}'".format(point_to_transfer))

        witch_perk_buck = 49153

        actor_init_buck_tracker = BucksUtils.get_tracker_for_bucks_type(witch_perk_buck, actor_sim)

        if actor_init_buck_tracker is not None:

            bucks_init_amount = actor_init_buck_tracker.get_bucks_amount_for_type(witch_perk_buck)

            bucks_amount_for_test = bucks_init_amount - point_to_transfer

            if bucks_amount_for_test > 0:

                output('{} Bucks will be left after this operation.'.format(bucks_amount_for_test))

            else:

                output('{} Bucks will lead to a negative Bucks Value which equates to: {} Bucks'.format(point_to_transfer, bucks_amount_for_test))

                failure_title = lambda **_: _create_localized_string(299169602)  # LocalizationHelperTuning.get_raw_text("Transfer Failure")
                failure_text = lambda **_: _create_localized_string(3748715972)  # LocalizationHelperTuning.get_raw_text("Not enough ▯Perk Points for a transfer.")

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('No Actor Sim specified. Please enter a valid Sim ID when running this command.')

            return

        deduction_point = point_to_transfer - 2 * point_to_transfer

        deduct_perk_point(deduction_point, actor_sim, witch_perk_buck)

        give_perk_point(point_to_transfer, target_sim, witch_perk_buck)

        # End of the callback

    # Create the dialog title and text from a raw text string
    """
    Note: Not all string are in use, most of the LocalizationHelperTunings are disabled. Only those with Variable amount will use it.
    """
    localized_title = lambda **_: _create_localized_string(419738413)  # LocalizationHelperTuning.get_raw_text("Transfer Perk Points")
    localized_text = lambda **_: _create_localized_string(507562398)  # LocalizationHelperTuning.get_raw_text("Indicate the number of ▯Talent Points that {0.SimFirstName} would like to transfer to {1.SimFirstName}")
    localized_initial_value = lambda **_: _create_localized_string(507562399)  # LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_points = UiTextInput(sort_order=0, restricted_characters=None)
    input_points.default_text = None
    input_points.title = None
    input_points.max_length = 30
    input_points.initial_value = localized_initial_value
    input_points.length_restriction = PerkPointControl_TextInputLength()
    input_points.check_profanity = False
    input_points.height = False

    inputs = AttributeDict({'input_number': input_points})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text,
                                                                title=localized_title, text_inputs=inputs, text_tokens=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")

    # Bucks Addition
    def give_perk_point(amount, owner_id, bucks_type):

        tracker = get_bucks_tracker(bucks_type, owner_id, _connection, add_if_none=True)

        if tracker is None:
            return False

        result = tracker.try_modify_bucks(bucks_type, amount, reason='Added Via Cheat.')

        if not result:

            failure_title = lambda **_: _create_localized_string(299169602)  # LocalizationHelperTuning.get_raw_text("Transfer Failure")
            failure_text = lambda **_: _create_localized_string(3748715972)  # LocalizationHelperTuning.get_raw_text("Not enough ▯Perk Points for a transfer.")

            notification_failure = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=failure_text,
                title=failure_title
            )
            notification_failure.show_dialog()

        else:

            success_title = lambda **_: _create_localized_string(0x20E85423)  # LocalizationHelperTuning.get_raw_text("Transfer Success")
            success_text = lambda **_: _create_localized_string(0xD2B49D14, amount)  # LocalizationHelperTuning.get_raw_text("▯" + str(amount) + " Perk Points has been transferred.")  # _create_localized_string(3535052052)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

    # Bucks Deduction
    def deduct_perk_point(amount, owner_id, bucks_type):

        tracker = get_bucks_tracker(bucks_type, owner_id, _connection, add_if_none=True)

        if tracker is None:
            return False

        result = tracker.try_modify_bucks(bucks_type, amount, reason='Added Via Cheat.')

        if not result:

            failure_title = lambda **_: _create_localized_string(299169602)  # LocalizationHelperTuning.get_raw_text("Transfer Failure")
            failure_text = lambda **_: _create_localized_string(3748715972)  # LocalizationHelperTuning.get_raw_text("Not enough ▯Perk Points for a transfer.")

            notification_failure = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=failure_text,
                title=failure_title
            )
            # notification_failure.show_dialog()

        else:

            success_title = lambda **_: _create_localized_string(0x20E85423)  # LocalizationHelperTuning.get_raw_text("Transfer Success")
            success_text = lambda **_: _create_localized_string(0xD2B49D14)  # LocalizationHelperTuning.get_raw_text("▯" + str(amount) + " Perk Points has been transferred.")  # _create_localized_string(3535052052)

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            # notification_success.show_dialog()


@Command('masterspells.perkpointtransmute', pack=Pack.GP04, command_type=CommandType.Live)
def perk_point_transmute(actor_sim:int=None, _connection=None):
    output = CheatOutput(_connection)
    client = services.client_manager().get_first_client()


    temp_bucks_type = 49153

    tracker_actor = get_bucks_tracker(temp_bucks_type, actor_sim, _connection, add_if_none=True)

    if tracker_actor is None:
        return False

    def get_inputs_callback(dialog):
        if not dialog.accepted:
            output("Dialog was cancelled")
            return
        point_to_transfer = int(dialog.text_input_responses.get("input_number"))
        output("User typed '{}'".format(point_to_transfer))

        witch_perk_buck = 49153

        vampire_power_buck = 40961

        actor_init_buck_tracker = BucksUtils.get_tracker_for_bucks_type(vampire_power_buck, actor_sim)

        if actor_init_buck_tracker is not None:

            bucks_init_amount = actor_init_buck_tracker.get_bucks_amount_for_type(vampire_power_buck)

            bucks_amount_for_test = bucks_init_amount - point_to_transfer

            if bucks_amount_for_test > 0:

                output('{} Bucks will be left after this operation.'.format(bucks_amount_for_test))

            else:

                output(
                    '{} Bucks will lead to a negative Bucks Value which equates to: {} Bucks'.format(point_to_transfer, bucks_amount_for_test))

                failure_title = lambda **_: _create_localized_string(299169602)  # LocalizationHelperTuning.get_raw_text("Transfer Failure")
                failure_text = lambda **_: _create_localized_string(3748715972)  # LocalizationHelperTuning.get_raw_text("Not enough ▯Perk Points for a transfer.")

                notification_failure = UiDialogNotification.TunableFactory().default(
                    client.active_sim,
                    text=failure_text,
                    title=failure_title
                )
                notification_failure.show_dialog()

                return

        else:

            output('No Actor Sim specified. Please enter a valid Sim ID when running this command.')

            return

        give_perk_point(point_to_transfer, actor_sim, witch_perk_buck)

        deduction_point = point_to_transfer - 2 * point_to_transfer

        deduct_perk_point(deduction_point, actor_sim, vampire_power_buck)
        # End of the callback

    # Create the dialog title and text from a raw text string

    localized_title = lambda **_: _create_localized_string(2317492683)  # LocalizationHelperTuning.get_raw_text("Transmute Perk Points")
    localized_text = lambda **_: _create_localized_string(2548902337)  # LocalizationHelperTuning.get_raw_text("Indicate the number of ▯Power Points that {0.SimFirstName} would like to transmute into ▯Talent Points")
    localized_initial_value = lambda **_: _create_localized_string(2548902338)  # LocalizationHelperTuning.get_raw_text("")

    # This defines our input fields
    input_points = UiTextInput(sort_order=0, restricted_characters=None)
    input_points.default_text = None
    input_points.title = None
    input_points.max_length = 30
    input_points.initial_value = localized_initial_value
    input_points.length_restriction = PerkPointControl_TextInputLength()
    input_points.check_profanity = False
    input_points.height = False

    inputs = AttributeDict({'input_number': input_points})

    # Create the actual dialog object...
    dialog = UiDialogTextInputOkCancel.TunableFactory().default(client.active_sim, text=localized_text,
                                                                title=localized_title, text_inputs=inputs, text_tokens=inputs)
    icon = get_resource_key(0, Types.PNG)

    dialog.add_listener(get_inputs_callback)
    dialog.show_dialog(icon_override=IconInfoData(icon_resource=icon))
    output("Main function done")

    # Bucks Addition
    def give_perk_point(amount, owner_id, bucks_type):

        tracker = get_bucks_tracker(bucks_type, owner_id, _connection, add_if_none=True)

        if tracker is None:
            return False

        result = tracker.try_modify_bucks(bucks_type, amount, reason='Added Via Cheat.')

        if not result:

            failure_title = lambda **_: _create_localized_string(3370434524)  # LocalizationHelperTuning.get_raw_text("Transmute Failure")
            failure_text = lambda **_: _create_localized_string(3748715972)  # LocalizationHelperTuning.get_raw_text("{Not enough ▯Perk Points for a transfer.")

            notification_failure = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=failure_text,
                title=failure_title
            )
            notification_failure.show_dialog()

        else:

            success_title = lambda **_: _create_localized_string(552096803)  # LocalizationHelperTuning.get_raw_text("Transmute Success")
            success_text = lambda **_: _create_localized_string(1956515011, amount)  # LocalizationHelperTuning.get_raw_text("▯" + str(amount) + " Power Points have been transmuted into ▯Talent Points.")

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            notification_success.show_dialog()

    # Bucks Deduction
    def deduct_perk_point(amount, owner_id, bucks_type):

        tracker = get_bucks_tracker(bucks_type, owner_id, _connection, add_if_none=True)

        if tracker is None:
            return False

        result = tracker.try_modify_bucks(bucks_type, amount, reason='Added Via Cheat.')

        if not result:

            failure_title = lambda **_: LocalizationHelperTuning.get_raw_text("Transmute Failure")
            failure_text = lambda **_: LocalizationHelperTuning.get_raw_text("{0.SimFirstName} does not have enough ▯Perk Points for a transfer.")

            notification_failure = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=failure_text,
                title=failure_title
            )
            # notification_failure.show_dialog()

        else:

            success_title = lambda **_: LocalizationHelperTuning.get_raw_text("Transmute Success")
            success_text = lambda **_: LocalizationHelperTuning.get_raw_text("{0.SimFirstName} has transmuted ▯" + str(amount) + " Power Points into ▯Talent Points.")

            notification_success = UiDialogNotification.TunableFactory().default(
                client.active_sim,
                text=success_text,
                title=success_title
            )
            # notification_success.show_dialog()
