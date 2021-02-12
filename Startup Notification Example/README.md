# Startup Notification Example

The Startup Notification uses Module Tuning with Python Scripting in order to show a notification on load finished.

The original structure was from Scumbumbo, which you can look here: [URL=https://modthesims.info/showthread.php?t=622129]

### XML Tuning Example
```xml
<U n="MASTERSPELLS_STARTUP_NOTIFICATION">
  <V n="icon" t="enabled">
    <V n="enabled" t="resource_key">
      <U n="resource_key">
        <T n="key">2f7d0004:00000000:9D293761EB2AC213</T>
      </U>
    </V>
  </V>
  <V n="title" t="enabled">
    <T n="enabled">0x0A2BD243<!--Sage of Mastery Magic + Mastery Spells + Ghost Butler + Alchemy: Release Version--></T>
  </V>
  <V n="text" t="single">
    <T n="single">0x0A2BD244<!--Current Version: <b>Version 2.00</b> \n\nFound any bugs or issues? Do report it over on MTS or on the TD1 Community Server under #report-bugs.--></T>
  </V>
  <E n="visual_type">INFORMATION</E>
  <E n="information_level">PLAYER</E>
  <E n="expand_behavior">FORCE_EXPAND</E>
  <L n="ui_responses">
    <U>
      <V t="enabled" n="response_command">
        <U n="enabled">
          <T n="command">masterspells.td1_discord</T>
        </U>
      </V>
      <T n="text">0x0A2BD249<!--Report Issue To #report-bugs In TD1 CS--></T>
      <E n="ui_request">SEND_COMMAND</E>
    </U>   
  </L>
</U>
```
### Python Scripting Example
```python
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

```
For a in depth view, you can look at the XML and Py files, it will have a clear view of the entire code.
