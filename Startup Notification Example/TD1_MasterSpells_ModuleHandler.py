import webbrowser
import injector
import services
from sims.sim_info_manager import SimInfoManager
from sims4.commands import Command, CommandType, CheatOutput, execute
from sims4.localization import LocalizationHelperTuning
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.tunable import TunableReference, Tunable
from ui.ui_dialog_notification import UiDialogNotification

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
    notification_ran = False


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


@injector.inject_to(SimInfoManager, 'on_loading_screen_animation_finished')
def td1_masterspells_add_on_load_complete(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    if TD1MasterSpellsModuleHandler.notification_ran is True:
        
        return
    
    try:
        masterspells_startup_notification_handler()
        
        TD1MasterSpellsModuleHandler.notification_ran = True
    except Exception as e:

        raise Exception(f"Error found with Master Spells Startup Notification Module by TwelfthDoctor1: {str(e)}")

    return result


def masterspells_startup_notification_handler():

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
