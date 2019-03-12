# -*- coding: utf-8 -*-
from pyramid.threadlocal import get_current_registry

from openprocurement.api.utils import (
    APIResource,
    context_unpack,
    json_view,
)
from openprocurement.contracting.core.utils import (
    apply_patch,
    contractingresource,
)
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_DEFAULT_TYPE,
    ENDPOINTS,
)
from openprocurement.contracting.core.validation import (
    validate_patch_contract_data,
)
from openprocurement.contracting.core.interfaces import (
    IContractManager,
)
from openprocurement.api.utils.validation import validate_data_to_event


@contractingresource(
    name='ceasefire:Contract',
    path=ENDPOINTS['contracts'],
    collection_path=ENDPOINTS['contracts_collection'],
    internal_type=CONTRACT_DEFAULT_TYPE)
class CeasefireContractResource(APIResource):

    @json_view(permission='view_contract')
    def get(self):
        return {'data': self.request.context.serialize("view")}

    @json_view(
        permission='edit_contract',
        validators=(validate_data_to_event,)
    )
    def patch(self):
        manager = get_current_registry().getAdapter(self.request.context, IContractManager)
        updated = manager.change_contract(self.request.event)
        if updated:
            self.LOGGER.info(
                'Updated ceasefire contract. Status: {0}, id: {1}'.format(
                    self.request.context.status,
                    self.request.context.id
                ),
                extra=context_unpack(
                    self.request,
                    {'MESSAGE_ID': 'ceasefire_contract_patch'}
                )
            )
        return {'data': self.request.context.serialize('view')}
