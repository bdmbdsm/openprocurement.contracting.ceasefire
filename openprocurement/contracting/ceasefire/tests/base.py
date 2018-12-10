from os import path
from functools import partial

from openprocurement.api.utils import read_json
from openprocurement.contracting.core.tests.base import (
    BaseWebTest as CoreBaseWebTest,
    BaseContractWebTest as CoreBaseContractWebTest,
)

from openprocurement.contracting.core.tests.base import (
    MOCK_CONFIG as BASE_MOCK_CONFIG,
    connection_mock_config
)
from openprocurement.contracting.ceasefire.constants import SNAPSHOTS_DIR
from openprocurement.contracting.ceasefire.tests.fixtures.config import PARTIAL_MOCK_CONFIG
from openprocurement.contracting.ceasefire.tests.fixtures.data import contract_create_data

MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'contracting.core', 'plugins'))


get_snapshot = partial(read_json, file_dir=SNAPSHOTS_DIR)


class BaseWebTest(CoreBaseWebTest):

    relative_to = path.dirname(__file__)
    mock_config = MOCK_CONFIG


class BaseContractWebTest(CoreBaseContractWebTest):

    relative_to = path.dirname(__file__)
    mock_config = MOCK_CONFIG
    initial_data = contract_create_data
