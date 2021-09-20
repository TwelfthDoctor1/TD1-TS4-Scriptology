# TD1 Tuning Descriptions (TDESCs)

Currently WIP. TDESCs will be released slowly.

The TD1 TDESC holds all modding documentation to TD1 Mods ranging from Modules to Injectors, each explaining on how it works and how it should be used.

### List of TDESCs

* DevAccessPanel
* SharedTunings

### DevAccessPanel

WIP

### SharedTunings

The SharedTunings TDESC is a compile of Documentation for scripts that are used throughout mods such as the AF2 or the LootBuff/Int Injector. These shared tunings all follow a common theme of [FRAMEWORK_NAME]. The [FRAMEWORK_NAME] denotes the name of the mod used to fill in the class and module name.

#### Example:

```xml
<Instance class="TD1_[FRAMEWORK_NAME]_Add_Int_AF2" module="[FRAMEWORK_NAME].FrameworkLib.TD1_[FRAMEWORK_NAME]_Add_Int_AF2 OR TD1_[FRAMEWORK_NAME]_Add_Int_AF2" />
```

In the case of `module`, there are two paths that leads to the script. Depending on the mod, the path may be [FRAMEWORK_NAME].FrameworkLib or directly on the base script folder. FrameworkLib is currently used by the DevAccessPanel and TMS whilst other mods use the base script folder method. It is recommended to check through the XML scripts that I have created for the mod or by decompiling the TS4SCRIPT to verify the folder path.
