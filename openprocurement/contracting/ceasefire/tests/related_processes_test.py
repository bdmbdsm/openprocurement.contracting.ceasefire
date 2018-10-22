import time
import unittest

from copy import copy, deepcopy

from schematics.exceptions import ModelConversionError
from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.api.utils import (
    calculate_business_date,
)
from openprocurement.contracting.core.tests.base import (
    RelatedProcessesTestMixinBase,
)
from openprocurement.contracting.ceasefire.tests.base import (
    BaseWebTest,
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
    DEFAULT_CONTRACT_STATUS,
    MILESTONE_FINANCING_DUEDATE_OFFSET
)
from openprocurement.contracting.ceasefire.tests.fixtures.data import (
    contract_create_data,
)
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,
)
from openprocurement.contracting.core.tests.fixtures.related_process import (
    test_related_process_data,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
)
from openprocurement.contracting.ceasefire.tests.constants import (
    CONTRACT_FIELDS_TO_HIDE,
)
from openprocurement.contracting.ceasefire.tests.fixtures.helpers import (
    create_contract,
    get_contract,
    patch_contract,
    post_document,
    prepare_milestones_all_met,
)


class CeasefireRelatedProcessesTestMixin(RelatedProcessesTestMixinBase):
    """These methods adapt test blank to the test case

    This adaptation is required because the mixin would test different types
    of resources, e.g. auctions, lots, assets.
    """

    def mixinSetUp(self):
        contract_id = create_contract(self).data.id
        self.base_resource_url = 'contracts/{0}'.format(contract_id)
        self.base_resource_collection_url = 'contracts'

        token = self.db[contract_id]['owner_token']
        self.access_header = {'X-Access-Token': str(token)}

        self.base_resource_initial_data = contract_create_data
        self.initial_related_process_data = test_related_process_data


class CeasefireRelatedProcessesTestCase(BaseWebTest, CeasefireRelatedProcessesTestMixin):

    docservice = True

    def setUp(self):
        super(CeasefireRelatedProcessesTestCase, self).setUp()
        self.app.authorization = ('Basic', ('broker5', ''))

#    def test_contract_post_by_contracting(self):
#        self.app.authorization = ('Basic', ('contracting', ''))
#        response = self.app.post_json(
#            ENDPOINTS['contracts_collection'],
#            {
#                'data': contract_create_data,
#            }
#        )
#        response_data = response.json['data']
#        self.assertEqual(response.status, '201 Created', 'Contract not created')
#        self.assertEqual(response_data['awardID'], contract_create_data['awardID'])
#        self.assertEqual(response_data['status'], DEFAULT_CONTRACT_STATUS)
#
#    def test_get_contract(self):
#        contract = create_contract(self)
#        contract_id = contract.data.id
#        self.app.authorization = ('Basic', ('broker1', ''))
#        response = self.app.get(
#            ENDPOINTS['contracts'].format(
#                contract_id=contract_id))
#        assert response.status == '200 OK'
#        response_data_keys = response.json['data'].keys()
#        assert '_internal_type' not in response_data_keys
#        assert 'period' not in response_data_keys
#        assert 'terminationDetails' not in response_data_keys
#        assert 'dateModified' in response_data_keys
