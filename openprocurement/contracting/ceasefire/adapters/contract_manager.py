# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils import validate_with
from openprocurement.api.utils.data_engine import DataValidationEngine, DataPersistenceEngine
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


@implementer(IContractManager)
class CeasefireContractManager(object):

    _engine_cls = DataEngine

    def __init__(self, context):
        self.context = context
        self.document_manager = CeasefireContractDocumentManager

    def create_contract(self, event):
        pass

    change_validators = (
        # validate_allowed_contract_statuses,
    )

    @validate_with(change_validators)
    def change_contract(self, event):
        updated_contract = self._engine_cls(event).apply_data_on_model()
        new_status = updated_contract.get('status')
        if new_status == 'active.payment':
            milestone_manager = CeasefireMilestoneManager(event.context)
            milestone_manager.create_milestones(updated_contract)
