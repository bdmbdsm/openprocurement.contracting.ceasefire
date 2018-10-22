# -*- coding: utf-8 -*-
from openprocurement.contracting.core.adapters import Manager
from openprocurement.contracting.core.utils import (
    save_contract,
    apply_patch,
)


class CeasefireRelatedProcessesManager(Manager):

    def create(self, request):
        self.context.relatedProcesses.append(request.validated['relatedProcess'])
        return save_contract(request)

    def update(self, request):
        return apply_patch(request, src=request.context.serialize())

    def delete(self, request):
        self.context.relatedProcesses.remove(request.validated['relatedProcess'])
        self.context.modified = False
        return save_contract(request)
