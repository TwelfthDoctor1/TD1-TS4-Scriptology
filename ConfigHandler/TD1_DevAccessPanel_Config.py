import os
import configparser
from pathlib import Path
import services
from sims4.commands import Command, CommandType, Output
from sims4.localization import LocalizationHelperTuning, _create_localized_string, TunableLocalizedStringFactoryVariant, \
    TunableLocalizedStringFactory
from sims4.tuning.tunable import TunableList, TunableMapping, Tunable, TunableTuple, TunableEnumEntry, TunableEnumFlags
from ui.ui_dialog import UiDialogStyle, UiDialogBGStyle, UiDialogOption, get_defualt_ui_dialog_response, \
    UiDialogOkCancel
from ui.ui_dialog_notification import UiDialogNotification

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Developer/Debug Access Panel Config', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Developer/Debug Access Panel Config', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

config_key_list = [
    'disable_notifs',
    'override_debug_menu',
    'force_debug_cheat_menu',
    'allow_selectable_pets',
    'override_pack_testset',
    'override_integration_testset',
    'override_version_testset',
    'cheat_debug_pie_menu'
]

preset_modifiers = [
    "False",
    "True",
    "True",
    "False",
    "False",
    "False",
    "False",
    "False"
]


class TD1DevAccessPanelConfigHandlerUI:
    CONFIG_UI_TEXT_DISPLAY = TunableMapping(
        description='List to hold the UI Text for each option.',
        key_name='option_type',
        key_type=Tunable(
            description='The option type for the UI to be associated with.',
            tunable_type=str,
            default=''
        ),
        value_name='ui_data',
        value_type=UiDialogOkCancel.TunableFactory(
            description='The Dialog for each Option.',
        )
    )


main_dir = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()

main_header = 'TD1 Developer Access Panel Config Settings'


def get_config_dir():
    """
    Gets the Configuration File Directory.

    No Params Required.
    """

    log_name = "TD1_AccessPanel_Settings.cfg"

    config_dir = os.path.join(main_dir, log_name)

    return config_dir


def config_prep_file():
    """
    Configures and creates a brand new Config File for use.
    :return:
    """
    with open(get_config_dir(), "w") as config_file:
        config_file.write("[TD1 Developer Access Panel Config Settings]")
        # Incrementor Int by default is presumed as 0 and increments from there.
        # List Assigns start off as 0 as well.
        for incrementor in range(len(config_key_list)):
            config_file.write("\n" + config_key_list[incrementor] + " = " + preset_modifiers[incrementor])

        config_file.close()


if os.path.exists(get_config_dir()) is True:
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("TD1 DevAccessPanel Config File Found.", owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("TD1 DevAccessPanel Config File Found.", owner="TwelfthDoctor1")

else:
    config_prep_file()
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("TD1 DevAccessPanel Config File Missing. Creating New Config File...",
                                   owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("TD1 DevAccessPanel Config File Missing. Creating New Config File...",
                               owner="TwelfthDoctor1")


@Command('td1devaccess.list_config', command_type=CommandType.Live)
def print_config_values(_connection=None):
    output = Output(_connection)
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            value = config.get(main_header, config_key_list[incrementor])
            output("{}: {}".format(config_key_list[incrementor], value))


@Command('td1devaccess.list_config_notif', command_type=CommandType.Live)
def print_config_values(_connection=None):
    client = services.client_manager().get_first_client()
    output = Output(_connection)
    text_final = ""
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            value = config.getboolean(main_header, config_key_list[incrementor])
            status = check_modifier_status(value)
            output("{}: {}".format(config_key_list[incrementor], status))
            text_final += f'[{config_key_list[incrementor]}]: {status}\n\n'
    text_final += 'These modifier tunings can be found inside the TD1_AccessPanel_Settings.cfg file. Use the Settings Panel to modify settings.'
    message_title = lambda **_: LocalizationHelperTuning.get_raw_text('TD1 Developer Access Panel Mod Configurations')
    message_text = lambda **_: LocalizationHelperTuning.get_raw_text(text_final)
    notification = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text,
        title=message_title,
        information_level=UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
    )
    notification.show_dialog()


def check_modifier_status(status):
    if status is True:
        result = "ENABLED"
        return result
    else:
        result = "DISABLED"
        return result


@Command('td1devaccess.set_option', command_type=CommandType.Live)
def set_option(option, _connection=None):
    output = Output(_connection)
    client = services.client_manager().get_first_client()
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        if config.has_option(main_header, option):
            orig_value = config.get(main_header, option)
            orig_value_bool = config.getboolean(main_header, option)
            config_file.close()

            for (option_type, dialog_data) in TD1DevAccessPanelConfigHandlerUI.CONFIG_UI_TEXT_DISPLAY.items():
                if option_type == option:
                    def on_response(dialog):
                        if dialog.accepted:
                            for key in config_key_list:
                                if key == option:
                                    option_toggle(config_key_list.index(key))

                    dialog = dialog_data(None)
                    dialog.add_listener(on_response)
                    dialog.show_dialog()

        else:
            output("Wrong Option Specified. Please refer to config list and try again.")
            config_file.close()


def config_init_check():
    """
    Runs an initial check on the config file for any missing options.
    Prudent on newer versions of the mod with config implementations.
    :return:
    """
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            if config.has_option(main_header, config_key_list[incrementor]) is False:
                append_option(incrementor)

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Config List Check Success.", owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("Config List Check Success.", owner="TwelfthDoctor1")


def append_option(identifier):
    """
    Appends missing options into the config file.
    :param identifier:
    :return:
    """
    option = config_key_list[identifier]
    modifier = preset_modifiers[identifier]
    with open(get_config_dir(), "a") as config_file:
        config_file.write("\n" + option + " = " + modifier)
        config_file.close()

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Option Key: {0} has been appended into Config File.".format(option),
                                   owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("Option Key: {0} has been appended into Config File.".format(option),
                               owner="TwelfthDoctor1")

    with open(get_config_dir(), "r") as config_file:
        return config_file


config_init_check()


def option_toggle(identifier):
    client = services.client_manager().get_first_client()
    option = config_key_list[identifier]

    if config.has_option(main_header, option) is False:
        append_option(identifier)
    else:
        with open(get_config_dir(), "r") as config_file:
            config.read_file(config_file)
            setting_value = config.getboolean(main_header, option)
            print("{0} {1}".format(option, setting_value))

            if setting_value is True:
                value = "False"
                config.set(main_header, option, value)
                config.write(open(get_config_dir(), "w"))

            elif setting_value is False:
                value = "True"
                config.set(main_header, option, value)
                config.write(open(get_config_dir(), "w"))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(
                "Option: {0} has been set to {1}. (Formerly {2})".format(option, value, setting_value),
                owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("Option: {0} has been set to {1}. (Formerly {2})".format(option, value, setting_value),
                               owner="TwelfthDoctor1")

        message_title_config_change = lambda **_: LocalizationHelperTuning.get_raw_text("Access Panel Option Change")
        message_text_config_change = lambda **_: LocalizationHelperTuning.get_raw_text(
            "The option: {} has been changed from {} to {}.\n\nA restart may be required for changes to take effect.".format(
                option, setting_value, value
            ))

        notification_config_change = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_config_change,
            title=message_title_config_change,
            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        notification_config_change.show_dialog()


def get_option_value(option):
    """
    Gets the value from the option (key) in the Config List.
    :param option:
    :return:
    """
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        value = config.getboolean(main_header, option)
        return value
