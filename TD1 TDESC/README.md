# TD1 Tuning Descriptions (TDESCs)

![TD1 TDESC Info Picture](https://github.com/TwelfthDoctor1/TD1-TS4-Scriptology/blob/main/repo_images/TD1%20TDESC%20Picture.png)

Currently WIP. TDESCs will be released slowly.

The TD1 TDESC holds all modding documentation to TD1 Mods ranging from Modules to Injectors, each explaining on how it works and how it should be used.

## Using TDESCs

You need a TDESC viewer to read the TDESCs with ease. You don't want to read XML don't you?

Download TDESC Viewer: [Windows (Scumbumbo)](https://modthesims.info/d/618199/ts4-tuning-description-browser-windows-only.html) | [macOS (Lebbion)](https://modthesims.info/d/649060/tuning-description-browser-for-macos.html)

To view the TDESCs, unzip and put the TDESCs into your TDESC Root Folder. For macOS, **do not unzip the archive**, instead use the application to select a new TDESC Library.

### List of TDESCs

* DevAccessPanel
* SharedTunings
* TMS

### DevAccessPanel

Most of the new, work in progress and currently used scripts are in the DevAccessPanel. These scripts are the foundation for other mods such as the Startup Notification and the Config Handler.

Mods derived from the DevAccessPanel should cross-reference the DevAccessPanel for TDESC information such the Travel To Venue Standalone Mod. However other mods that uses certain elements from this group of TDESCs can also be cross referenced here.

### SharedTunings

The SharedTunings TDESC is a compile of Documentation for scripts that are used throughout mods such as the AF2 or the LootBuff/Int Injector. These shared tunings all follow a common theme of [FRAMEWORK_NAME]. The [FRAMEWORK_NAME] denotes the name of the mod used to fill in the class and module name.

#### Example:

```xml
<Instance class="TD1_[FRAMEWORK_NAME]_Add_Int_AF2" module="[FRAMEWORK_NAME].FrameworkLib.TD1_[FRAMEWORK_NAME]_Add_Int_AF2 OR TD1_[FRAMEWORK_NAME]_Add_Int_AF2" />
```

In the case of `module`, there are two paths that leads to the script. Depending on the mod, the path may be [FRAMEWORK_NAME].FrameworkLib or directly on the base script folder. FrameworkLib is currently used by the DevAccessPanel and TMS whilst other mods use the base script folder method. It is recommended to check through the XML scripts that I have created for the mod or by decompiling the TS4SCRIPT to verify the folder path.

### Usage of Injectors

Certain injectors have a V1 and a V2 (or V2 and a V3) which may lead to confusion. It is recommended to use the **Newer Version** as the newer version supports multiple instances into one instance through `TunableList-TunableTuple Iteration <L><U>`. The older version may be removed in later updates but will remain for compatibility with some XML scripts that use the older version.

#### Older Version Injectors

The Older Version Injectors only allows one injection per instance, thus using up a lot of XML Instances. **If you are only planning to use one instance, it is recommended to use this otherwise please use the newer version that supports multiple injections on one instance.** Otherwise they should provide the same functions and Tunables as its newer counterparts (unless I forgot to add them in). The older version TDESCs are referenced through `TD1[InjectorName].tdesc (Example: TD1LootBuffIntInjector.tdesc)`.

#### Newer Version Injectors

The Newer Version Injectors allows for mutiple injections on one instance therefore saving up on multiple XML Instances (though it is always recommended to classify them through instances). The TDESCs for these Injectors follow this context: `TD1[InjectorName]V[VersionNumber].tdesc OR TD1[InjectorName][VersionNumber].tdesc (Example: TD1LootIntInjectorV2.tdesc | TD1AffordanceInjector3.tdesc)`

### TMS

The TMS TDESC caters to the Teleport Memory System Mod. Parts of its scripts are derived from the DevAccessPanel, if there are any modules referenced in XML but not in TDESC, do check the DevAccessPanel for said information (if available).
