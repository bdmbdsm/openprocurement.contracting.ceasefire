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
        pass

MIGRATION_STEPS = (
    RelatedProcessesMigrationStep,
)
