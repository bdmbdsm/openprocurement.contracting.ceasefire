# -*- coding: utf-8 -*-
from schematics.types import StringType, MD5Type
from uuid import uuid4
from zope.interface import implementer, Interface
from schematics.types.compound import (
    ModelType,
)
from pyramid.security import Allow

from openprocurement.api.constants import (
    SANDBOX_MODE,
)
from openprocurement.api.validation import validate_items_uniq
from openprocurement.api.models.common import (
    Period,
)
from openprocurement.api.models.registry_models import LokiItem
from openprocurement.api.models.schema import (
    SwiftsureProcuringEntity,
    dgfOrganization,
)
from openprocurement.api.models.schematics_extender import (
    IsoDateTimeType,
    ListType,
    Model,
)
from openprocurement.contracting.core.models import (
    Contract as BaseContract,
    RelatedProcess,
)
from openprocurement.contracting.ceasefire import constants

from .roles import (
    MILESTONE_ROLES,
    CONTRACT_ROLES,
)


class ICeasefireMilestone(Interface):
    """Contract marker interface
    """


@implementer(ICeasefireMilestone)
class Milestone(Model):
    """Contract milestone
    """
    class Options:
        roles = MILESTONE_ROLES

    # named so to not override built-in method name
    id = MD5Type(required=True, default=lambda: uuid4().hex)
    dateMet = IsoDateTimeType()
    dateModified = IsoDateTimeType()
    description = StringType()
    description_en = StringType()
    description_ru = StringType()
    dueDate = IsoDateTimeType()
    status = StringType(choices=constants.MILESTONE_STATUSES)
    title = StringType()
    title_en = StringType()
    title_ru = StringType()
    type_ = StringType(choices=constants.MILESTONE_TYPES, serialized_name='type')

    def get_role(self):
        root = self.__parent__.__parent__  # contract->root
        request = root.request
        auth_role = request.authenticated_role
        if auth_role == 'Administrator':
            return 'Administrator'
        return 'edit_{0}'.format(request.context.status)


class ICeasefireContract(Interface):
    """Contract marker interface
    """


@implementer(ICeasefireContract)
class Contract(BaseContract):
    """Common Contract
    """

    class Options:
        roles = CONTRACT_ROLES

    awardID = StringType(required=True)  # overridden to make required
    items = ListType(ModelType(LokiItem), required=False, min_size=1, validators=[validate_items_uniq])
    suppliers = ListType(ModelType(dgfOrganization), required=True)
    contractID = StringType(required=True)  # overridden to make required
    dateSigned = IsoDateTimeType(required=True)  # overridden to make required
    contractType = StringType(required=True)  # must be generated by databridge
    milestones = ListType(ModelType(Milestone))  # generated automatically
    period = ModelType(Period)
    procuringEntity = ModelType(SwiftsureProcuringEntity)  # overridden to make not required
    status = StringType(choices=constants.CONTRACT_STATUSES, default=constants.DEFAULT_CONTRACT_STATUS)
    type_ = StringType(serialized_name='type')
    merchandisingObject = StringType(required=True)  # id of related lot
    relatedProcesses = ListType(ModelType(RelatedProcess), default=list())

    _internal_type = 'ceasefire'
    if SANDBOX_MODE:
        sandbox_parameters = StringType()

    def __local_roles__(self):
        return dict([('{}_{}'.format(self.owner, self.owner_token), 'contract_owner')])

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_contract'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_contract_documents'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'create_related_process'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_related_process'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'delete_related_process'),
            (Allow, 'g:caravan', 'create_related_process'),
            (Allow, 'g:caravan', 'edit_related_process'),
            (Allow, 'g:caravan', 'delete_related_process'),
            (Allow, 'g:convoy', 'create_related_process'),
            (Allow, 'g:convoy', 'edit_related_process'),
            (Allow, 'g:convoy', 'delete_related_process'),
        ]
        return acl

    def get_role(self):
        root = self.__parent__
        request = root.request
        if request.authenticated_role == 'Administrator':
            role = 'Administrator'
        elif request.authenticated_role == 'caravan':
            role = 'caravan'
        else:
            role = 'edit_{}'.format(request.context.status)
        return role
