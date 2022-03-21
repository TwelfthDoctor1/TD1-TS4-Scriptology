import services
from sims4 import resources, collections
from sims4.collections import FrozenAttributeDict
from sims4.log import Logger
from whims.whims_tracker import WhimsTracker
from sims4.tuning.instance_manager import InstanceManager
import injector

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Rewards Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Rewards Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Rewards Injector', default_owner='TwelfthDoctor1')


def register_satisfaction_store_reward(reward_id, cost, award_type=WhimsTracker.WhimAwardTypes.TRAIT):
    """
    Register satisfaction store reward of given type.
    This method retains the original classes state and won't conflict when adding multiple of different rewards.
    The 'award_type' keyword is set to 'TRAIT' as an example of what award types are available.
    :param reward_id: int -> id of the reward instance
    :param cost: int -> amount of satisfaction points this reward will cost
    :param award_type: WhimAwardTypes -> award type enum
    """

    reward_instance = services.get_instance_manager(resources.Types.REWARD).get(reward_id)

    if reward_instance is not None:

        immutable_slots_class = collections.make_immutable_slots_class(['cost', 'award_type'])
        reward_immutable_slots = immutable_slots_class(dict(cost=cost, award_type=award_type))

        satisfaction_store_items = dict(WhimsTracker.SATISFACTION_STORE_ITEMS)
        satisfaction_store_items[reward_instance] = reward_immutable_slots

        WhimsTracker.SATISFACTION_STORE_ITEMS = FrozenAttributeDict(satisfaction_store_items)

        logger.info("Reward Item: {} has been injected.".format(reward_id), owner="TwelfthDoctor1")

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Reward Item: {} has been injected.".format(reward_id), owner="TwelfthDoctor1")

        if master_logger is not None and master_logger is not False:
            master_logger.info("Reward Item: {} has been injected.".format(reward_id), owner="TwelfthDoctor1")


# Example of injecting a new reward trait
@injector.inject_to(InstanceManager, 'load_data_into_class_instances')
def _load_satisfaction_store_rewards(original, self):
    original(self)

    register_satisfaction_store_reward(17413066339074432809, 10000, WhimsTracker.WhimAwardTypes.TRAIT)
