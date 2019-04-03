# -*- coding: utf-8 -*-
from datetime import datetime

from openprocurement.api.utils import (
    APIResource,
    context_unpack,
    json_view,
)
from openprocurement.api.utils.error_management import handle_errors_on_view
from openprocurement.contracting.core.utils import (
    apply_patch,
    contractingresource,
)
from openprocurement.contracting.core.interfaces import (
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from openprocurement.contracting.ceasefire.validators import (
    validate_patch_milestone_data,
)
from openprocurement.api.utils.validation import validate_data_to_event
from openprocurement.contracting.core.manager_discovery import ContractManagerDiscovery


@contractingresource(
    name='Ceasefire Milestone',
    path=ENDPOINTS['milestones'],
    collection_path=ENDPOINTS['milestones_collection'])
class CeasefireMilestoneResource(APIResource):

    @json_view(
        permission='view_contract',
        content_type='application/json')
    def get(self):
        return {'data': self.request.context.serialize()}

    @json_view(
        permission='edit_contract',
        content_type='application/json',
        validators=(validate_data_to_event,))
    @handle_errors_on_view
    def patch(self):
        event = self.request.event
        md = ContractManagerDiscovery(self.request.registry.manager_registry)
        contract_manager = md.discover(event.ctx.high)
        manager = contract_manager.milestone_manager()
        return manager.change_milestone(event)
