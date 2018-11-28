# -*- coding: utf-8 -*-
from openprocurement.contracting.core import (
    BaseMigrationsRunner,
    BaseMigrationStep,
)


class CeasefireMigrationsRunner(BaseMigrationsRunner):
    pass


class RelatedProcessesMigrationStep(BaseMigrationStep):
    """Use relatedProcesses instead of merchandisingObject"""
    pass
