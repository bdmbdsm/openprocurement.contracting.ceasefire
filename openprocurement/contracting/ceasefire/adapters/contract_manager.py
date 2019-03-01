# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils import validate_with
from openprocurement.api.utils.data_engine import DataEngine
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

    def __init__(self, context):
        self.context = context
        self.engine = DataEngine()
        self.document_manager = CeasefireContractDocumentManager

    def create_contract(self, event):
        pass

    change_validators = (
        # validate_allowed_contract_statuses,
    )

    @validate_with(change_validators)
    def change_contract(self, event):
        import ipdb; ipdb.set_trace()
        updated_contract = self.engine.apply_data_on_model(event.data, event.context)
        new_status = updated_contract.get('status')
        if new_status == 'active.payment':
            milestone_manager = CeasefireMilestoneManager(event.context)
            milestone_manager.create_milestones(updated_contract)
