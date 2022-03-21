import webbrowser
import injector
import services
import zone
from distributor.shared_messages import IconInfoData
from sims.sim_info_manager import SimInfoManager
from sims4.collections import make_immutable_slots_class
from sims4.commands import Command, CommandType, CheatOutput, execute
from sims4.localization import LocalizationHelperTuning, _create_localized_string
from sims4.log import Logger
from sims4.resources import Types, get_resource_key
from sims4.tuning.tunable import TunableReference, Tunable
from ui.ui_dialog import UiDialogResponse, ButtonType
from ui.ui_dialog_notification import UiDialogNotification

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 Mastery Spells & Alchemy Module Handler', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 Mastery Spells & Alchemy Module Handler', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Mastery Spells & Alchemy Module Handler', default_owner='TwelfthDoctor1')


class TD1MasterSpellsModuleHandler:
    MASTERSPELLS_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The notification to be used on game load, used on release versions'
    )
    MASTERSPELLS_DEVELOPER_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The developer notification to be used on game load, developer use only'
    )
    MASTERSPELLS_BETA_STARTUP_NOTIFICATION = UiDialogNotification.TunableFactory(
        description='The beta notification to be used on game load, mainly for beta testers'
    )
    MASTERSPELLS_ALLOW_STARTUP_NOTIFICATION = Tunable(
        description='Whether the startup should show up on load',
        tunable_type=bool,
        default=True
    )
    MASTERSPELLS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION = Tunable(
        description='Whether the developer startup should show up on load',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_ALLOW_BETA_STARTUP_NOTIFICATION = Tunable(
        description='Whether the beta startup should show up on load',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_STARTUP_NOTIFICATION_V2_USAGE = Tunable(
        description='Controls usage of which version of the Startup Notification should be used. If disabled, Version 1 will be used. If enabled, Version 2 will be used.',
        tunable_type=bool,
        default=True
    )
    MASTERSPELLS_MOD_VERSION = Tunable(
        description='Current mod version. Used for Mod Verification and Testing.',
        tunable_type=str,
        default=''
    )
    MASTERSPELLS_IGNORE_MOD_VERSION = Tunable(
        description='Controls the Version Mismatch Test. If ignored, Version Mismatch Test will not flag up errors should versions be different.',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_ALLOW_BUCKS_ENUM_INJECTION = Tunable(
        description='Controls whether the Custom Bucks Enums should be injected.',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_ALLOW_SI_BUCKS_TRACKER_INJECTION = Tunable(
        description='Controls whether the Custom Bucks should be injected into SI Bucks Tracker.',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_ALLOW_BUCKS_UTILS_TRACKER_MAP_INJECTION = Tunable(
        description='Controls whether the Custom Bucks should be injected into Bucks Utils Map Tracker.',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_ALLOW_BUCKS_UTILS_DISPLAY_DATA_INJECTION = Tunable(
        description='Controls whether the Custom Bucks should be injected into Bucks Utils Display Data.',
        tunable_type=bool,
        default=False
    )
    MASTERSPELLS_ALLOW_BUCKS_UTILS_WALLET_INJECTION = Tunable(
        description='Controls whether the Custom Bucks should be injected into Bucks Utils Wallet.',
        tunable_type=bool,
        default=False
    )
    notification_ran = False
    mod_version = "Version 2.14"


# Command Handling Section
# Note: Secnario Var - If 1, then Notif will show up, for all other numbers not 1 excluding 0, Notif will not show with Indication that Tuning is set to Disabled.

@Command('masterspells.show_version', command_type=CommandType.Live)
def show_version(scenario: int = 0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_STARTUP_NOTIFICATION is True:
            startup_notification = TD1MasterSpellsModuleHandler.MASTERSPELLS_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Startup Notification Disabled, it can be enabled via the TD1_MasterSpells_ModuleHandler Tuning')
    elif scenario is 1:
        startup_notification = TD1MasterSpellsModuleHandler.MASTERSPELLS_STARTUP_NOTIFICATION(None)
        startup_notification.show_dialog()
    else:
        output('Startup Notification Disabled, it can be enabled via the TD1_MasterSpells_ModuleHandler Tuning')


@Command('masterspells.show_dev_version', command_type=CommandType.Live)
def show_dev_version(scenario: int = 0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            startup_notification = TD1MasterSpellsModuleHandler.MASTERSPELLS_DEVELOPER_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Developer Startup Notification Disabled, it can be enabled via the TD1_MasterSpells_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')
    elif scenario is 1:
        developer_startup_notification = TD1MasterSpellsModuleHandler.MASTERSPELLS_DEVELOPER_STARTUP_NOTIFICATION(None)
        developer_startup_notification.show_dialog()
    else:
        output('Developer Startup Notification Disabled, it can be enabled via the TD1_MasterSpells_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')


@Command('masterspells.show_beta_version', command_type=CommandType.Live)
def show_dev_version(scenario: int = 0, _connection=None):
    output = CheatOutput(_connection)
    if scenario is 0:
        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BETA_STARTUP_NOTIFICATION is True:
            startup_notification = TD1MasterSpellsModuleHandler.MASTERSPELLS_BETA_STARTUP_NOTIFICATION(None)
            startup_notification.show_dialog()
        else:
            output('Beta Startup Notification Disabled, it can be enabled via the TD1_MasterSpells_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')
    elif scenario is 1:
        beta_startup_notification = TD1MasterSpellsModuleHandler.MASTERSPELLS_BETA_STARTUP_NOTIFICATION(None)
        beta_startup_notification.show_dialog()
    else:
        output('Beta Startup Notification Disabled, it can be enabled via the TD1_MasterSpells_ModuleHandler Tuning. However, this should only be done by TwelfthDoctor1.')


# Discord Server Invite Command to report-bugs

@Command('masterspells.td1_discord', command_type=CommandType.Live)
def td1_discord(_connection=None):
    output = CheatOutput(_connection)
    output('Please check your browser for the server invite.')
    webbrowser.open('https://discord.gg/waHpcSHZwb')  # This link opens up Discord to invite the user to TD1 Community Server (3.0) for bug reporting


@Command('masterspells.td1_patreon', command_type=CommandType.Live)
def td1_patreon(_connection=None):
    output = CheatOutput(_connection)
    output('Please check your browser for the server invite.')
    webbrowser.open('https://www.patreon.com/twelfthdoctor1')  # This link opens up the Patreon Page


@injector.inject_to(SimInfoManager, 'on_loading_screen_animation_finished')
def td1_masterspells_add_on_load_complete(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    if TD1MasterSpellsModuleHandler.notification_ran is True:

        return

    try:

        masterspells_version_control()
        masterspells_startup_notification_handler()

        TD1MasterSpellsModuleHandler.notification_ran = True

    except Exception as e:

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.error(f"Error found with Master Spells Startup Notification Module: {str(e)}",
                                    owner="TwelfthDoctor1")

        if master_logger is not False and apprentice_logger is not None:
            master_logger.error(f"Error found with Master Spells Startup Notification Module: {str(e)}",
                                owner="TwelfthDoctor1")

        raise Exception(f"Error found with Master Spells Startup Notification Module by TwelfthDoctor1: {str(e)}")

    return result


def masterspells_startup_notification_handler():

    if TD1MasterSpellsModuleHandler.MASTERSPELLS_STARTUP_NOTIFICATION_V2_USAGE is True:
        execute('masterspells.show_version_v2', None)

    else:
        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_STARTUP_NOTIFICATION is True:
            execute('masterspells.show_version 1', None)
        else:
            execute('masterspells.show_version 2', None)

        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            execute('masterspells.show_dev_version 1', None)
        else:
            execute('masterspells.show_dev_version 2', None)

        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BETA_STARTUP_NOTIFICATION is True:
            execute('masterspells.show_beta_version 1', None)
        else:
            execute('masterspells.show_beta_version 2', None)

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info("TD1 Sage of Mastery Magic Version Control\n\nPackage Version: {}\nScript Version: {}".format(
            TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION, TD1MasterSpellsModuleHandler.mod_version
        ))

    if master_logger is not None and master_logger is not False:
        master_logger.info("TD1 Sage of Mastery Magic Version Control\n\nPackage Version: {}\nScript Version: {}".format(
            TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION, TD1MasterSpellsModuleHandler.mod_version
        ))


def masterspells_version_control():
    client = services.client_manager().get_first_client()

    if str(TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION).find(TD1MasterSpellsModuleHandler.mod_version) != -1 or TD1MasterSpellsModuleHandler.MASTERSPELLS_IGNORE_MOD_VERSION is True:
        return
    else:
        message_title_test_fail = lambda **_: LocalizationHelperTuning.get_raw_text("TD1 Master Spells: Version Mismatch")
        message_text_test_fail = lambda **_: LocalizationHelperTuning.get_raw_text("Version Mismatch found. Please check if your mod package and script are updated correctly.\n\nPackage Version: " + str(TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION) + "\n\nScript Version: " + str(TD1MasterSpellsModuleHandler.mod_version))

        notification_test_fail = UiDialogNotification.TunableFactory().default(
            client.active_sim,
            text=message_text_test_fail,
            title=message_title_test_fail,
            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
            urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
        )
        notification_test_fail.show_dialog()

        if apprentice_logger is not False and apprentice_logger is not None:
            apprentice_logger.warn("TD1 Master Spells Version Mismatch Error: Please check if your version is correct.",
                                   owner="TwelfthDoctor1")

        if master_logger is not False and master_logger is not None:
            master_logger.warn("TD1 Master Spells Version Mismatch Error: Please rectify Script Version and Package Version or use Override.",
                               owner="TwelfthDoctor1")


@Command('masterspells.show_version_v2', command_type=CommandType.Live)
def mod_version_startup_notif_v2(scenario:int=0, _connection=None):
    client = services.client_manager().get_first_client()
    output = CheatOutput(_connection)
    button1_text = None
    button2_text = None
    button3_text = None
    notif_title = None
    notif_text = None
    info_level = None
    visual = None

    if TD1MasterSpellsModuleHandler.MASTERSPELLS_STARTUP_NOTIFICATION_V2_USAGE is False and scenario == 0:
        output("Version 2 Startup Notification Disabled, it can be changed via the TD1_MasterSpells_ModuleHandler Tuning. Note that it should only be done by TwelfthDoctor1.")
        if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True:
            output("\nFor Notification Testing, the Variable: Scenario can be modified to use values 1 to 3.")

    if TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_STARTUP_NOTIFICATION is True or scenario == 1:
        notif_title = lambda **_: _create_localized_string(0x0A2BD243)
        notif_text = lambda **_: _create_localized_string(0x0A2BD24D, str(TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION), str(TD1MasterSpellsModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.PLAYER
        visual = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        button1_text = lambda **_: _create_localized_string(0x0A2BD24B)
        button2_text = lambda **_: _create_localized_string(0x0A2BD24C)
        # button3_text = lambda **_: _create_localized_string(0xD45017CC)

    elif TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_DEVELOPER_STARTUP_NOTIFICATION is True or scenario == 2:
        notif_title = lambda **_: _create_localized_string(0x0A2BD245)
        notif_text = lambda **_: _create_localized_string(0x0A2BD24E, str(TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION), str(TD1MasterSpellsModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        visual = UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
        button1_text = lambda **_: _create_localized_string(0x0A2BD24B)
        button2_text = lambda **_: _create_localized_string(0x0A2BD24C)
        # button3_text = lambda **_: _create_localized_string(0xD45017CD)

    elif TD1MasterSpellsModuleHandler.MASTERSPELLS_ALLOW_BETA_STARTUP_NOTIFICATION is True or scenario == 3:
        notif_title = lambda **_: _create_localized_string(0x0A2BD247)
        notif_text = lambda **_: _create_localized_string(0x0A2BD24F, str(TD1MasterSpellsModuleHandler.MASTERSPELLS_MOD_VERSION), str(TD1MasterSpellsModuleHandler.mod_version))
        info_level = UiDialogNotification.UiDialogNotificationLevel.SIM
        visual = UiDialogNotification.UiDialogNotificationVisualType.INFORMATION
        button1_text = lambda **_: _create_localized_string(0x0A2BD24B)
        button2_text = lambda **_: _create_localized_string(0x0A2BD24C)
        # button3_text = lambda **_: _create_localized_string(0xD45017CC)

    # Button Control
    # 1. Discord
    # 2. Patreon

    button1_response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'masterspells.td1_discord'})
    button2_response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'masterspells.td1_patreon'})
    # button3_response_command = make_immutable_slots_class(set(['arguments', 'command']))({'arguments': (), 'command': 'masterspells.update'})

    button1_response = UiDialogResponse(
        dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
        response_command=button1_response_command,
        text=button1_text
    )
    button2_response = UiDialogResponse(
        dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
        ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
        response_command=button2_response_command,
        text=button2_text
    )
    # button3_response = UiDialogResponse(
    #    dialog_response_id=ButtonType.DIALOG_RESPONSE_OK,
    #    ui_request=UiDialogResponse.UiDialogUiRequest.SEND_COMMAND,
    #    response_command=button3_response_command,
    #    text=button3_text
    # )

    notification_startup = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        title=notif_title,
        text=notif_text,
        information_level=info_level,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=visual,
        icon=lambda _: IconInfoData(
            icon_resource=get_resource_key(
                0x9D293761EB2AC213, Types.PNG
            )
        ),
        ui_responses=(
            button1_response,
            button2_response,
            # button3_response
        )
    )
    notification_startup.show_dialog()
