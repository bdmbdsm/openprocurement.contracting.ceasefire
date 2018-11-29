# -*- coding: utf-8 -*-
from unittest import TestCase

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
        self.runner = CeasefireMigrationsRunner(self.app.app.registry)

    def test_ok(self):
        """Turn merchandisingObject into relatedProcess"""
        steps = (RelatedProcessesMigrationStep,)

        self.runner.migrate(steps, schema_version_max=1, check_plugins=False)
        
        migrated_contract = self.db[self.contract_id]

        self.assertNotIn('merchandisingObject', migrated_contract.keys(), 'merchandisingObject should be removed')
        self.assertIn('relatedProcesses', migrated_contract.keys(), 'relatedProcesses should be present')
        rps = migrated_contract['relatedProcesses']
        self.assertTrue(len(rps) > 0, 'relatedProcesses should be non empty')
        rp = search_list_with_dicts(rps, 'relatedProcessID', self.merchandisingObject)
        self.assertIsNotNone(rp, 'relatedProcessID must be initialized')
        self.assertEqual(rp['type'], 'lot')
