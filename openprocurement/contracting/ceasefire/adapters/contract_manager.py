# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils.data_engine import DataEngine
from openprocurement.api.utils.ownership import OwnershipOperator
from openprocurement.contracting.core.interfaces import (
    IContractManager,
)
from openprocurement.contracting.core.utils import save_contract
from openprocurement.contracting.ceasefire.adapters.milestone_manager import (
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters.document_manager import (
    CeasefireContractDocumentManager,
)
from openprocurement.contracting.ceasefire.models.schema import Contract
from openprocurement.contracting.ceasefire.predicates import allowed_contract_status_changes


@implementer(IContractManager)
class CeasefireContractManager(object):

    _data_engine_cls = DataEngine
    milestone_manager = CeasefireMilestoneManager
    document_manager = CeasefireContractDocumentManager

    def create_contract(self, event):
        de = self._data_engine_cls(event)
        contract = de.create_model(Contract)
        self._add_documents_to_contract(contract, event.data)

        ownersip_operator = OwnershipOperator(contract)
        acc = ownersip_operator.set_ownership(
            event.auth.user_id, event.data.get('transfer_token')
        )
        saved = de.save(contract)
        if saved:
            # TODO log it
            return {
                'access': acc,
                'data': contract.serialize('view')
            }

    def _add_documents_to_contract(self, contract, data):
        for i in data.get('documents', []):
            doc = type(contract).documents.model_class(i)
            doc.__parent__ = contract
            contract.documents.append(doc)

    def change_contract(self, event):
        # validation
        de = self._data_engine_cls(event)
        contract = event.ctx.high
        new_status = event.data.get('status')
        user_id = event.auth.user_id
        if not allowed_contract_status_changes(contract.status, new_status, user_id):
            return None
            # request.errors.add('body', 'status', 'Status change is not allowed.')
            # request.errors.status = 403
            # raise error_handler(request)
        # validation end
        self.data_engine.apply_data_on_context()
        contract_upd = event.ctx.cache.low_data_model
        contract = event.ctx.high
        new_status = contract_upd.get('status')
        if new_status == 'active.payment':
            milestone_manager = self.milestone_manager()
            milestone_manager.create_milestones(contract)
        self.data_engine.update()

        return {'data': event.ctx.high.serialize('view')}
