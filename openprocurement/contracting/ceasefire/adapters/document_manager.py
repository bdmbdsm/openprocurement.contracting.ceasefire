# -*- coding: utf-8 -*-
from zope.interface import implementer

from openprocurement.api.utils import validate_with
from openprocurement.contracting.core.interfaces import (
    IDocumentManager,
)
from openprocurement.contracting.ceasefire.validators import (
    validate_document_upload_contract_not_terminal_status,
    validate_document_upload_milestone_not_terminal_status,
)


@implementer(IDocumentManager)
class CeasefireContractDocumentManager(object):

    create_validators = (
        validate_document_upload_contract_not_terminal_status,
        validate_document_upload_milestone_not_terminal_status,
    )

    @validate_with(create_validators)
    def create_document(self, request):
        document = request.validated['document']
        contract = request.context

        contract.documents.append(document)

    def change_document(self, request):
        pass
