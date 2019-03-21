# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils import validate_with
from openprocurement.api.utils.data_engine import DataEngine
from openprocurement.api.utils.ownership import OwnershipOperator
from openprocurement.contracting.core.interfaces import (
    IContractManager,
)
from openprocurement.contracting.ceasefire.validators import (
    validate_allowed_contract_statuses,
)
from openprocurement.contracting.ceasefire.adapters.milestone_manager import (
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters.document_manager import (
    CeasefireContractDocumentManager,
)
from openprocurement.contracting.ceasefire.models.schema import Contract


@implementer(IContractManager)
class CeasefireContractManager(object):

    _data_engine_cls = DataEngine

    def __init__(self, event):
        self.event = event
        self.document_manager = CeasefireContractDocumentManager
        self.data_engine = self._data_engine_cls(event)

    def create_contract(self):
        contract = self.data_engine.create_model(Contract)
        self._add_documents_to_contract(contract)

        ownersip_operator = OwnershipOperator(contract)
        import ipdb; ipdb.set_trace()
        acc = ownersip_operator.set_ownership(
            self.event.auth.user_id, self.event.data.get('transfer_token')
        )
        pass

    def _add_documents_to_contract(self, contract):
        for i in self.event.data.get('documents', []):
            doc = type(contract).documents.model_class(i)
            doc.__parent__ = contract
            contract.documents.append(doc)

    change_validators = (
        # validate_allowed_contract_statuses, # TODO: move to BL
    )

    @validate_with(change_validators)
    def change_contract(self, event):
        data_engine = self._data_engine_cls(event)

        data_engine.apply_data_on_context()
        contract_upd = event.ctx.cache['l_ctx_updated_model']
        contract = event.ctx.l_ctx.ctx
        new_status = contract_upd.get('status')
        if new_status == 'active.payment':
            milestone_manager = CeasefireMilestoneManager(contract)
            milestone_manager.create_milestones(contract)
        applied = data_engine.update()

        return applied
