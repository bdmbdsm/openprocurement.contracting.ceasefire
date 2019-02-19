# -*- coding: utf-8 -*-
from openprocurement.api.migrations import (
    BaseMigrationsRunner,
    BaseMigrationStep,
)


class CeasefireMigrationsRunner(BaseMigrationsRunner):

    SCHEMA_VERSION = 1
    SCHEMA_DOC = 'openprocurement_contracting_ceasefire_schema'


class FixDocserviceUrlsMigration(BaseMigrationStep):

    def setUp(self):
        self.view = 'contracts/all'

    def migrate_document(self, document):
        pass
