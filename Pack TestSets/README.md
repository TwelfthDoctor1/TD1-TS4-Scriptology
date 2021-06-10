# TD1 Pack TestSets

The TD1 Pack TestSet allows for a mass override from a Module Tuning.

### Snippet Tuning
```xml
<?xml version="1.0" encoding="utf-8"?>
<I c="TD1FrameworkStructureTestSetInstance" i="snippet" m="TD1_DevAccessPanel_TestSet" n="TD1:testSet_FrameworkStructure_Pack_EP10" s="11981296632196519527">
  <L n="test">
    <L>
      <V t="pack_test">
        <U n="pack_test">
          <!--pack: The Pack to test. Refer to sims4.common.py for Pack IDs.-->
          <E n="pack">EP10</E>
          <!--is_installed: Modifier to determine if the pack is installed.-->
          <T n="is_installed">True</T>
          <!--tooltip: The tooltip to display if test fails. Used in TestGlobals.-->
          <V n="tooltip" t="enabled">
            <T n="enabled">0x2DBFFFC0<!--Pack Not Installed or Found.--></T>
          </V>
        </U>
      </V>
    </L>
  </L>
</I>
```

### Module Tuning
```xml
<?xml version="1.0" encoding="utf-8"?>
<M n="TD1_FrameworkStructure_TestSet_Pack" s="3117759969792224241">
  <C n="TD1FrameworkStructurePackTestOverride">
    <!--Pack TestSet FrameworkStructure-->
    <!--The Pack TestSet is a TestSet that allows for Pack Tests.-->
    <!--Pack Tests can be initiated either by testing if it is installed or testing if it can be not installed.-->
    <!--TestSet Control-->
    <!--Do not modify the values stated here unless required. Modification can lead to access to unowned pack/integration cheats and may possibly flag LEs should the player use unowned pack/integration cheats.-->
    <!--Overrides all Pack TestSets to Pass. This will also give access to imcompleted or depreciated sections.-->
    <T n="FRAMEWORKSTRUCTURE_OVERRIDE_PACK_TESTSET">False</T>
  </C>
</M>
```

When the tunable in the Module Tuning is True, all Pack TestSets will be set to TRUE despite not meeting Pack Requirements.

Instead of using a Module Tuning, you could use a config to check if a certain tunable is True or False. In the Case of the AccessPanel and TMS mods, I have a function called get_option_value(option_name_in_string) that gets the boolean value of the config (getboolean(), see [Python Configparser Library](https://docs.python.org/3/library/configparser.html)).
