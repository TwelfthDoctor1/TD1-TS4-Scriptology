# Config Handler

### What is the Config Handler?

The Config Handler is a Python Script that handles Configuration files (.cfg).

Besides that it can handle the following:

* Auto Generation of Config File (if it does not exist in directory or is deleted)
* Addition of config options when updated
* Read and parse values from config file (Boolean specifically)

#### Note: You require some prior knowledge on [Python's ConfigParser Library](https://docs.python.org/3/library/configparser.html) and File Handling.

### Starters

The base is that we need the config options and their base values:

```py3
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
```
Which it should result in:
```cfg
[TD1 Developer Access Panel Config Settings]
# ^ Main Header
# Presume we only need one Header

# Config Options
# You can use = or :, its your choice

disable_notifs = False
override_debug_menu = True
force_debug_cheat_menu = True
allow_selectable_pets = True
override_pack_testset = False
override_integration_testset = False
override_version_testset = False
cheat_debug_pie_menu = False
```

Obviously there is no way for all that to instantly become the config file, thats where code come in.

### Setting the Base Structure

```py3
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
```

`main_dir` is the place where we want the file to be in. 2 `.parent`s are required as one is leaping from | script file > script directory | and another from | script directory > mod folder |.

**Note: Based on how you structure your mod, you may require more than 2 `.parent`s.**

`config` is to hold the ConfigParser class so that we can use some of its functions. At this stage, you can set up `configparser.ConfigParser()` to whatever variables you require (see ConfigParser for info).

`main_header` is the name of the Header you plan to use. You can have more headers if need be, but it will require more code to handle switching of headers. FOr 1 headers, I recommend using the Mod Name to identify it.

Function `get_config_dir() *No Vars` is used to get the file location/directory of the config file and return to when required. The `log_name` is the name of the config file (_I forgot to change it from MasterApprentice Logger, oh well_).

### Prepping a Config File

In order to prepare a Config File if non-existent, we need some code to write to it.

```py3
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
```

Function `config_prep_file()` is used to prep the comfig file. You need to change the header preset to the one in `main_header` but with []. e.g. [TD1 Settings]. Everything in here is in _write mode_.

The `if...else` conditional statement below handles whether the config file needs to be prepped or not. As part of my logging procedure, I have my loggers to logg the process here. After the prepping or no prepping, we open up the file as read mode, this will be necessary for the ConfigParser to read.

### Init Checking

```py3
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

config_init_check()
```

Function `config_init_check()` is used to check if the config file is missing any config options which is prudent on future versions of your mod (if you added any options).
You will need to call it with `config_init_check()` after the function structure as nothing is calling it without that line.

### Toggling Options [True -> False | False -> True]

```py3
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
```
Function `option_toggle()` is responsible for switching an option into another state. In this state, we still use `r: read` to handle the file instead of `a: append`. We use the ConfigParser to read and change values of options under `getboolean()`, `set()` and `write()` (`get()` could be used but will return as string value. For specific data types, use `getint()`, `getfloat` and `getboolean`.).

At the end of all this, we use a notification to tell the user that an option has been changed to let them know.

Of course, as of right now you cannot use this function without some form of command.

### Commands

```py3
@Command('td1devaccess.list_config', command_type=CommandType.Live)
def print_config_values(_connection=None):
    output = Output(_connection)
    with open(get_config_dir(), "r") as config_file:
        config.read_file(config_file)
        for incrementor in range(len(config_key_list)):
            value = config.get(main_header, config_key_list[incrementor])
            output("{}: {}".format(config_key_list[incrementor], value))


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
```
Command `td1devaccess.list_config` is used to list the config options and their current value. Useful for checking the current state.

Command `td1devaccess.set_option` is used to change the config option value on a specified option. Note that there is a Handler UI present, we will get to that in a lil bit.

### Config Handler UI (TunableUIDialogOkCancel)

```py3
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
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<M n="TD1_DevAccessPanel_Config" s="12143312186674213107">
  <C n="TD1DevAccessPanelConfigHandlerUI">
    <L n="CONFIG_UI_TEXT_DISPLAY">
      <U>
        <T n="option_type">disable_notifs</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D47<!--Startup Notifications--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D0661B<!--This Setting modifies whether the Startup Notifications should show up on load complete.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">force_debug_cheat_menu</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D48<!--Force Debug Interactions Into Cheat Pie Menu--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D0661C<!--This Setting modifies whether Debug Interactions should be seen in Release Versions of the Game via turning Debug Display Type in the Interactions off.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">override_debug_menu</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D49<!--Override Debug Interactions--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D0661D<!--This Setting modifies whether Debug Interactions without a Cheat Display Type Enabled to be enabled whilst being turned into a Cheat Interaction.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">allow_selectable_pets</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D4A<!--Make Pets Selectable--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D0661E<!--This Setting modifies whether Pet Sims can be Selectable and Controlled in the game.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">override_pack_testset</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D4B<!--Override Pack TestSets--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D0661F<!--This Setting modifies whether to override all Pack TestSets to Pass. This will also give access to imcompleted or depreciated sections.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">override_integration_testset</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D4C<!--Override Integration TestSets--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D06620<!--This Setting modifies whether to override all Integration TestSets to Pass. Note: Certain Integrations do not rely on this and would instead not appear on load should the corresponding mod be not installed.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">override_version_testset</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D4D<!--Override Version TestSets--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D06621<!--This Setting modifies whether to override all Version TestSets to Pass. This should be unused by default.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
      <U>
        <T n="option_type">cheat_debug_pie_menu</T>
        <U n="ui_data">
          <V n="title" t="enabled">
      	    <T n="enabled">0xC1855D4E<!--Force Cheats into Cheat/Debug Pie Menu--></T>
      	  </V>
      	  <V n="text" t="single">
            <T n="single">0x96D06622<!--This Setting modifies whether cheats should either appear on the Main Pie Menu or on the Cheat/Debug Pie Menu (Shift + Click) which would require testingcheats to be enabled.--></T>
          </V>
          <T n="text_ok">0xBE404130<!--Change Option--></T>
          <E n="dialog_style">DEFAULT</E>
          <E n="dialog_bg_style">BG_DEFAULT</E>
          <L n="dialog_options">
            <E>DISABLE_CLOSE_BUTTON</E>
          </L>
        </U>
      </U>
    </L>
  </C>
</M>
```

The class `TD1DevAccessPanelConfigHandlerUI` is a Module tuning to hold the UI Structure and data of how should the UIDialogOkCancel will look like when called by the command as a means for the player to make their own choice on whether to change the option or not. You would obviously need an XML Module Tuning to go along with the script.

As this uses TunableMapping (which is a dictionary {'key': 'value'}), we need to use `items()` to open it. (See [Access Dictionary Items By W3Schools](https://www.w3schools.com/python/python_dictionaries_access.asp) for more info.)

### Final Thoughts

There are more than one way to write a Config Handler, there is JSON which Python can handle as an object in JSON is a dictionary in Python. Preface for handling is different but reading and writing the file would also have some changes as you will be writing and reading to the file directly.

ConfigParser is a module that can be hard to master if you are not advanced enough. You would need to learn the basics and fundementals of Python File Handling in order to do so.

In my codes, I use `with open (get_config_dir(),"r") as config_file:` however you can use `config_file.open(get_config_dir(), "r")` if you choose to, in the end its all about flexibity and your own choices.

I recommend that you read through the ConfigParser Information and looking at examples when trying to do this.

#### If you require assistance on this, feel free to discuss with me if needed.
