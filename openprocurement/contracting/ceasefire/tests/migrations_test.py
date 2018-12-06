# -*- coding: utf-8 -*-
from unittest import TestCase
from uuid import uuid4

from openprocurement.contracting.core.traversal import Root 
from openprocurement.contracting.ceasefire.tests.fixtures.snapshots import get_snapshot
from openprocurement.contracting.ceasefire.tests.base import (
    BaseWebTest
)
from openprocurement.contracting.ceasefire.migrations import (
    CeasefireMigrationsRunner,
    RelatedProcessesMigrationStep,
)
from openprocurement.api.utils import (
    search_list_with_dicts,
)


class RelatedProcessesMigrationTestCase(BaseWebTest):

    def setUp(self):
        auction_fixture = get_snapshot('contract_with_merchandising_object.json')
        self.merchandisingObject = auction_fixture['merchandisingObject']
        self.contract_id = self.db.save(auction_fixture)[0]

        runner = CeasefireMigrationsRunner(self.app.app.registry, Root)
        steps = (RelatedProcessesMigrationStep,)

        def run_migration():
            runner.migrate(steps, schema_version_max=1, check_plugins=False)

        self.run_migration = run_migration

    def test_ok(self):
        """Turn merchandisingObject into relatedProcess"""

        self.run_migration()
        
        migrated_contract = self.db[self.contract_id]

        self.assertNotIn('merchandisingObject', migrated_contract.keys(), 'merchandisingObject should be removed')
        self.assertIn('relatedProcesses', migrated_contract.keys(), 'relatedProcesses should be present')
        rps = migrated_contract['relatedProcesses']
        self.assertTrue(len(rps) > 0, 'relatedProcesses should be non empty')
        rp = search_list_with_dicts(rps, 'relatedProcessID', self.merchandisingObject)
        self.assertIsNotNone(rp, 'relatedProcessID must be initialized')
        self.assertEqual(rp['type'], 'lot')

    def test_skip_migrated(self):
        contract_doc = self.db[self.contract_id]
        # add relatedProcesses
        contract_doc['relatedProcesses'] = [{
            'id': uuid4().hex,
            'relatedProcessID': uuid4().hex
        }]
        # remove merchandisingObject
        del contract_doc['merchandisingObject']

        self.db.save(contract_doc)

        self.run_migration()

        after_migration_doc = self.db[self.contract_id]
        self.assertNotIn('merchandisingObject', after_migration_doc.keys())
        self.assertIn('relatedProcesses', after_migration_doc.keys())

    def tearDown(self):
        del self.db[self.contract_id]
