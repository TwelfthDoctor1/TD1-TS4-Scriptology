import event_testing
import services
from event_testing.tests import _TunableTestSetBase, TunableTestVariant, TestSetInstance
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from TD1_FrameworkStructure_TestSet_Pack import TD1FrameworkStructurePackTest


class TD1FrameworkStructureTunableTestSet(_TunableTestSetBase, is_fragment=True):

    def __init__(self, **kwargs):
        TunableTestVariant.TEST_VARIANTS['pack_test'] = TD1FrameworkStructurePackTest.TunableFactory
        super().__init__(test_locked_args={}, **kwargs)


class TD1FrameworkStructureTestSetInstance(TestSetInstance):

    INSTANCE_TUNABLES = {'test': TD1FrameworkStructureTunableTestSet()}
