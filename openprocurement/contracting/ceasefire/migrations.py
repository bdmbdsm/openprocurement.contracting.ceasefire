# -*- coding: utf-8 -*-
from openprocurement.contracting.core.traversal import Root
from openprocurement.contracting.core.migration import (
    BaseMigrationsRunner,
    BaseMigrationStep,
)


class CeasefireMigrationsRunner(BaseMigrationsRunner):

    SCHEMA_VERSION = 1
    SCHEMA_DOC = 'openprocurement_contracting_ceasefire_schema_version'
    ROOT_CLASS = Root


class RelatedProcessesMigrationStep(BaseMigrationStep):
    """Use relatedProcesses instead of merchandisingObject"""

    def setUp(self):
        self.view = 'contracts/all'

    def migrate_document(self, contract):
        if self._skip_predicate(contract):
            return
        merch_obj = contract['merchandisingObject']
        del contract['merchandisingObject']

        return contract

    def _skip_predicate(self, contract):
        if 'merchandisingObject' in contract.keys():
            return False
        return True

MIGRATION_STEPS = (
    RelatedProcessesMigrationStep,
)
