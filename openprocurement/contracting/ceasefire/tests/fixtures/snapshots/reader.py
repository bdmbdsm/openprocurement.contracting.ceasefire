# -*- coding: utf-8 -*-
import os
import json

from openprocurement.contracting.ceasefire.constants import SNAPSHOTS_DIR

def get_snapshot(snapshot_filename):
    """Read adjacent file & deserialize it"""
    full_filename = os.path.join(SNAPSHOTS_DIR, snapshot_filename)
    with open(full_filename, 'r') as f:
        data = f.read()
    return json.loads(data)
