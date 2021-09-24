# Custom MenuUIs

The Custom MenuUI and SettingsUI is a modified InteractionPicker designed to cater towards icon state switching, specialise on config changes through icons, etc.

#### Preface

Typically, most Menus can be achieved without custom python code (except injectors) through the use of InteractionPickers. InteractionPickers are pickers that allows a user to choose a specific interaction but it can be useful as menus. 

However InteractionPickers have a few drawbacks, one of the main ones being that you cannot specify different states of icons.

For this case, we will **clone** and modify the interaction_picker.py (note that clone is bolded).

#### Pure Python or Python-XML?

There are actually two ways to go about and achieve this. The pure python method of making a picker involves the picker and row classes, but the tunings are 100% python, meaning no XML. Depending on your expertise, knowledge, etc, it can be more way more dunting and complex to work it out in Python (I have tried it and I can tell you that it involves a lot of localisation mess, accountability for tokens, function calling, etc, its just messy). 

As for the case we will focus on Python-XML, reason for doing so is that it is friendlier and most parts can still be cross-referenced to the InteractionPicker class.

## Part I: Figuring out what you want to add/remove

After you cloned the interaction_picker.py, remember to give it a **new name** (obviously for colliding reasons).

Determine what new features you want added and/or removed. For this example, we are making a Menu Picker (or I call it MenuUI) and want to have icon switching functionality and a fallback icon structure if there are no icons tuned.

To add these new tunables, you first need to know that the interaction picker is tuned to allow literal/reference for its possible actions tunable through snippet definition and a class. It should be noted that you should change the class name and the TunableSnippetItem name.

```py3
class InteractionPickerItem(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        'icon': OptionalTunable(
            description='\n            If enabled, specify the icon to be displayed in UI.\n            ',
            tunable=TunableIconVariant()
        ),
        'name': OptionalTunable(
            description='\n            If enabled, display this name in the UI.\n            \n            Otherwise the display name of the first affordance\n            in the continuation will be used as the name.\n            ',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_description': OptionalTunable(
            description='\n            When enabled, the tuned string will be shown as a description.\n            ',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_tooltip': OptionalTunable(
            description='\n            When enabled, the tuned string will be shown as a tooltip.\n            ',
            tunable=TunableLocalizedStringFactory()
        ),
        'disable_tooltip': OptionalTunable(
            description='\n            When tuned, and the item is disabled, the tuned string \n            will be shown as a tooltip.\n            \n            Otherwise it will try to grab a tooltip off a failed test.\n            ',
            tunable=TunableLocalizedStringFactory()
        ),
        'continuation': TunableContinuation(
            description='\n            The continuation to push when this item is selected.\n            ',
            minlength=1
        ),
        'enable_tests': OptionalTunable(
            description='\n            Tests which would dictate if this option is enabled\n            in the pie menu.  ORs of ANDs.\n            \n            If disabled, it will default to the tests for the\n            first affordance in the continuation chain.\n            ',
            tunable=TunableTestSet()),
        'localization_tokens': OptionalTunable(
            description="\n            Additional localization tokens for this item\n            to use in the name/description.\n            \n            This is in addition to the display name tokens\n            tuned in the continuation's first affordance.\n            ",
            tunable=LocalizationTokens.TunableFactory()
        ),
        'visibility_tests': OptionalTunable(
            description='\n            Tests which would dictate if this option is visible\n            in the pie menu.  ORs of ANDs.\n            \n            If disabled, this item will always be visible.\n            ',
            tunable=TunableTestSet()
        )
    }
    

(_, TunableInteractionPickerItemSnippet) = define_snippet('interaction_picker_item', InteractionPickerItem.TunableFactory())
```

The reason for why this could be use is when you have a `possible_actions` from drfferent pickers and all using the same list, to simplify matters, deploying one snippet to all these pickers allows reducing code length.

Now make changes to the code (example method of wanting a `icon_disabled`, `icon_enabled`,`base_icon_enabled`, `base_icon_disabled` and `base_icon_locked`):

```py3
class DevAccessPanelMenuUIStructure(HasTunableSingletonFactory, AutoFactoryInit):
    """
    Menu UI Structure for Interaction and Snippet.
    """
    FACTORY_TUNABLES = {
        'icon_enabled': OptionalTunable(
            description='If enabled, specify the icon to be displayed in UI for enabled state.',
            tunable=TunableIconVariant()
        ),
        'icon_disabled': OptionalTunable(
            description='If enabled, specify the icon to be displayed in UI for disabled state.',
            tunable=TunableIconVariant()
        ),
        'name': OptionalTunable(
            description='If enabled, display this name in the UI. Otherwise the display name of the first affordance in the continuation will be used as the name.',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_description': OptionalTunable(
            description='When enabled, the tuned string will be shown as a description.',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_tooltip': OptionalTunable(
            description='When enabled, the tuned string will be shown as a tooltip.',
            tunable=TunableLocalizedStringFactory()
        ),
        'disable_tooltip': OptionalTunable(
            description='When tuned, and the item is disabled, the tuned string will be shown as a tooltip. Otherwise it will try to grab a tooltip off a failed test.',
            tunable=TunableLocalizedStringFactory()
        ),
        'continuation': TunableContinuation(
            description='The continuation to push when this item is selected.',
            minlength=1
        ),
        'enable_tests': OptionalTunable(
            description='Tests which would dictate if this option is enabled in the pie menu.  ORs of ANDs. If disabled, it will default to the tests for the first affordance in the continuation chain.',
            tunable=TunableTestSet()
        ),
        'localization_tokens': OptionalTunable(
            description="Additional localization tokens for this item to use in the name/description. This is in addition to the display name tokens tuned in the continuation's first affordance.",
            tunable=LocalizationTokens.TunableFactory()
        ),
        'visibility_tests': OptionalTunable(
            description='Tests which would dictate if this option is visible in the pie menu.  ORs of ANDs. If disabled, this item will always be visible.',
            tunable=TunableTestSet()
        ),
        'base_icon_enabled': TunableEnumEntry(
            description="The base icon to use for enabled state if icon_enabled is unused.",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.MENU_MISSING
        ),
        'base_icon_disabled': TunableEnumEntry(
            description="The base icon to use for disabled state if icon_disabled is unused.",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.NONE
        ),
        'base_icon_locked': TunableEnumEntry(
            description="The base icon to use if the interaction is locked (failed test).",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.MENU_LOCKED
        ),
        'icon_state_change_tests': OptionalTunable(
            description="Tests to determine whether the enabled or disabled state should be chosen.",
            tunable=TunableTestSet()
        )
    }
```

Something I forgot to explain earlier, how would the icon be changed? I could wire it up to `enable_tests` but I decided to make a whole new test (possibly to ensure different tests for different functions). Also, do remember to rename the class name and the define snippet area to avoid code confusion.

## Part II: The Picker

```py3
class InteractionPickerSuperInteraction(PickerSuperInteraction):
    INSTANCE_TUNABLES = {
        'picker_dialog': UiItemPicker.TunableFactory(
            description='\n            The item picker dialog.\n            ',
            tuning_group=GroupNames.PICKERTUNING
        ),
        'possible_actions': TunableList(
            description='\n            A list of the interactions that will show up in the dialog picker\n            ',
            tunable=TunableInteractionPickerItemSnippet(),
            minlength=1,
            tuning_group=GroupNames.PICKERTUNING
        )
    }
```

This code above is the XML Framework for the InteractionPicker. Note that the tunable for the `possible_actions` needs to be changed thereafter to whatever Tunable...Snippet name you give it to earlier.

Now about the `picker_dialog`, it is using a UiItemPicker, thereby locking `picker_type` as `ObjectPickerType.ITEM`. If you want it as an object picker, you can change the UiItemPicker as UiObjectPicker. However doing so requires that the BasePickerRow be changed into ObjectPickerRow.

Also, if you are wondering where are the tunables such as `display_name`, note that they exist, but are being referenced via the parent of the current class and so on and so forth.

## Part III: What makes the Picker Tick and Work

```py3
    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim, target_sim=self.sim)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = cls if inst is None else inst
        cloned_context = context.clone_for_insert_next(source=InteractionSource.SCRIPT_WITH_USER_INTENT)
        for choice in inst_or_cls.possible_actions:
            first_continuation = next(iter(choice.continuation), None)
            if first_continuation is None:
                pass
            else:
                affordance = first_continuation.affordance
                resolver = affordance.get_resolver(target=target, context=cloned_context, **kwargs)

                if not choice.visibility_tests or not choice.visibility_tests.run_tests(resolver):
                    pass
                else:
                    tokens = tuple() if choice.localization_tokens is None else choice.localization_tokens.get_tokens(
                        resolver)

                    display_name = affordance.get_name(
                        target=target,
                        context=cloned_context
                    ) if choice.name is None else affordance.create_localized_string(
                        choice.name,
                        tokens,
                        target=target,
                        context=cloned_context,
                        **kwargs
                    )

                    icon_info = None if choice.icon is None else choice.icon(resolver)
                    display_description = None if choice.item_description is None else affordance.create_localized_string(
                        choice.item_description, tokens, target=target, context=cloned_context, **kwargs)
                    row_tooltip = None
                    tag = choice
                    if choice.enable_tests:
                        test_result = choice.enable_tests.run_tests(resolver)
                    else:
                        test_result = affordance.test(target=target, context=cloned_context)
                    row_tooltip = choice.item_tooltip
                    row_tooltip = test_result.tooltip
                    is_enabled = bool(test_result)
                    row_tooltip = choice.disable_tooltip
                    row = BasePickerRow(is_enable=is_enabled, name=display_name, icon_info=icon_info,
                                        row_description=display_description, tag=tag, row_tooltip=row_tooltip)
                    yield row

    def on_choice_selected(self, choice, **kwargs):
        if choice is not None:
            self.push_tunable_continuation(choice.continuation)
```

These are functions contained within the class. These code will run when a XML Tuning of that class is called. 

The first function `_run_interaction_gen(self, timeline)` is used to call the picker. If you want to add any code before the execution of the picker, put it there.

The second function `picker_rows_gen(cls, inst, context, **kwargs)` is what builds the picker from the XML data that is tuned. This function gets the data from the instance, denote from cls (or class) and breaks it down into its tunable forms to then be processed into the picker.

The third function `on_choice_selected` runs when a choice is selected (the close button of the picker does not count). Any code you want run after a choice is selected should be written here.

Most of the mentioned additions and changes will be made on the second function. Based from the defined class, the handling of parsing to the picker would become:
```py3
def handle_menu_icon(is_enable, state_test, resolver, choice):
    if is_enable:
        if state_test:
            test_result = bool(state_test.run_tests(resolver))
        else:
            test_result = True

        if test_result is True:
            return choice.icon_enabled if choice.icon_enabled is not None else \
                parse_ui_icon_enum_to_data(choice.base_icon_enabled)
        else:
            return choice.icon_disabled if choice.icon_disabled is not None else \
                parse_ui_icon_enum_to_data(choice.base_icon_disabled)

    else:
        return MenuUIBaseIcons.UI_ICON_MENU_LOCKED if choice.base_icon_locked == MenuUIBaseIconsEnums.NONE else \
            parse_ui_icon_enum_to_data(choice.base_icon_locked)


def handle_settings_icon(config_option, is_enable, version_type, choice):

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = cls if inst is None else inst
        cloned_context = context.clone_for_insert_next(source=InteractionSource.SCRIPT_WITH_USER_INTENT)
        for choice in inst_or_cls.possible_actions:
            first_continuation = next(iter(choice.continuation), None)

            if master_logger is not None and master_logger is not False:
                master_logger.debug(
                    f"Current Choice:\n{choice}\n\nFirst Continuation:\n{first_continuation}\n\nFull Context:"
                    f"\n{inst_or_cls.possible_actions}"
                )

            if first_continuation is None:

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"First Continuation is unexpectedly None. Skipping....."
                    )

            else:
                affordance = first_continuation.affordance
                resolver = affordance.get_resolver(target=target, context=cloned_context, **kwargs)

                if choice.visibility_tests is None or choice.visibility_tests.run_tests(resolver) is not None:
                    tokens = tuple() if choice.localization_tokens is None else choice.localization_tokens.get_tokens(
                        resolver)

                    display_name = affordance.get_name(
                        target=target,
                        context=cloned_context
                    ) if choice.name is None else affordance.create_localized_string(
                        choice.name,
                        tokens,
                        target=target,
                        context=cloned_context,
                        **kwargs
                    )

                    display_description = None if choice.item_description is None else \
                        affordance.create_localized_string(
                            choice.item_description, tokens, target=target, context=cloned_context, **kwargs
                        )
                    # row_tooltip = None  # No Tooltip to satisfy interactions without tooltips
                    tag = choice
                    if choice.enable_tests:
                        test_result = choice.enable_tests.run_tests(resolver)
                    else:
                        test_result = affordance.test(target=target, context=cloned_context)
                    # row_tooltip = choice.item_tooltip  # item_tooltip
                    # row_tooltip = test_result.tooltip  # affordance failed test tooltip
                    is_enabled = bool(test_result)
                    # row_tooltip = choice.disable_tooltip  # disable_tooltip

                    row_tooltip = choice.disable_tooltip if is_enabled is False and choice.disable_tooltip is not None \
                        else test_result.tooltip if test_result.tooltip is not None and is_enabled is False else \
                        choice.item_tooltip

                    icon_state = handle_menu_icon(is_enabled, choice.icon_state_change_tests, resolver, choice)

                    icon_info = None if icon_state is None else icon_state(resolver)

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"ICON: {icon_info}\n\n"
                            f"SPECIFIC RESULT: {icon_state}\n\n"
                            f"ROW ENABLED: {is_enabled}"
                        )

                    row = BasePickerRow(
                        is_enable=is_enabled,
                        name=display_name,
                        icon_info=icon_info,
                        row_description=display_description,
                        tag=tag,
                        row_tooltip=row_tooltip
                    )

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(row)

                    yield row

                else:
                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"Affordance Choice [{affordance}] tuned to not be visible due to Test Failure. "
                            f"Skipping....."
                        )

                        master_logger.info(
                            f"[VISIBILITY TESTS DATA]\n{choice.visibility_tests}\n\n"
                            f"{choice.visibility_tests.run_tests(resolver) if choice.visibility_tests is not None else 'Test returns NoneType. Cannot run test.....'}"
                        )
```

**Note: My code uses Custom Loggers to aid in logging. It is highly recommended to log your processes to determine if they are working or when debugging. You can use the sims4.log.Logger Class to log the data being parsed.**

## Part IV: xxx
