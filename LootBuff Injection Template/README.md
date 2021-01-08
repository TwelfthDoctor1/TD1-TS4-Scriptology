# LootBuff Injector

The LootBuff Injector allows for the injection of `_loot_on_addition`, `_loot_on_instance` and `loot_on_removal` onto the buff.

The Injector references `buff_reference` and inject and adds the 3 loot lists (slated above) into the buffs own 3 loot lists.

### Snippet Tuning Reference

```xml

<T n="buff_reference"></T>
<!--buff_reference is the destination for the loot lists to be inject into.-->

<L n="loot_on_addition">
</L>
<!--List of loots that are to be injected into _loot_on_addition.-->

<L n="loot_on_instance">
</L>
<!--List of loots that are to be injected into _loot_on_instance.-->

<L n="loot_on_removal">
</L>
<!--List of loots that are to be injected into _loot_on_removal.-->

```
