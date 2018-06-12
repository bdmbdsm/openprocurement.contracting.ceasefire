# -*- coding: utf-8 -*-
from schematics.transforms import whitelist, blacklist
from schematics.types import StringType, MD5Type
from uuid import uuid4
from zope.interface import implementer, Interface
from schematics.types.compound import (
    ModelType,
)

from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.api.models.common import (
    Period,
)
from openprocurement.api.models.auction_models import (
    Organization,
)
from openprocurement.api.models.schematics_extender import (
    IsoDateTimeType,
    ListType,
    Model,
)
from openprocurement.contracting.core.models import (
    Contract as BaseContract,
    ProcuringEntity,
    contract_create_role,
    contract_view_role,
    contract_edit_role,
)
from openprocurement.contracting.ceasefire import constants


class ICeasefireMilestone(Interface):
    """Contract marker interface
    """

@implementer(ICeasefireMilestone)
class Milestone(Model):
    """Contract milestone
    """
    class Options:
        roles = {
            'create':
                blacklist(
                    'dateMet',
                    'dateModified',
                    'dueDate',
                    'id',
                    'status',
                    'type_',
                ),
            'edit':
                blacklist(
                    'dateModified',
                    'dueDate',
                    'id',
                    'status',
                    'type_',
                )
        }
    # named so to not override built-in method name
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    dateMet = IsoDateTimeType()
    dateModified = IsoDateTimeType()
    description = StringType()
    dueDate = IsoDateTimeType()
    status = StringType(choices=constants.MILESTONE_STATUSES)
    title = StringType()
    type_ = StringType(choices=constants.MILESTONE_TYPES, serialized_name='type')


class ICeasefireContract(Interface):
    """Contract marker interface
    """


@implementer(ICeasefireContract)
class Contract(BaseContract):
    """Common Contract
    """

    class Options:
        roles = {
            'create':
                contract_create_role +
                whitelist('contractType', 'buyers') +
                blacklist('milestones'),
            'view':
                contract_view_role +
                whitelist('contractType', 'milestones'),
            'edit_active.confirmation':
                contract_edit_role +
                blacklist('buyers', 'milestones'),
            'edit_active.payment':
                contract_edit_role +
                blacklist('buyers', 'milestones'),
            'edit_active.approval':
                contract_edit_role +
                blacklist('buyers', 'milestones'),
            'edit_active':
                contract_edit_role +
                blacklist('buyers', 'milestones'),
            'edit_terminated':
                whitelist(),
            'edit_unsuccessful':
                whitelist(),
        }
    awardID = StringType(required=True)  # overridden to make required
    buyers = ListType(ModelType(Organization), required=True)
    contractID = StringType(required=True)  # overridden to make required
    dateSigned = IsoDateTimeType(required=True)  # overridden to make required
    # must be generated by databridge
    contractType = StringType(choices=[constants.CONTRACT_TYPE], default=constants.CONTRACT_TYPE)
    milestones = ListType(ModelType(Milestone))
    period = ModelType(Period)
    procuringEntity = ModelType(ProcuringEntity)  # overridden to make not required
    status = StringType(choices=constants.CONTRACT_STATUSES, default=constants.DEFAULT_CONTRACT_STATUS)
    create_accreditation = 5
    edit_accreditation = 6
    _internal_type = 'ceasefire'
    if SANDBOX_MODE:
        sandbox_parameters = StringType()