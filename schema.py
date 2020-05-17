import graphene

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.graphql_base import OdooObjectType

class Lesson(OdooObjectType):
    name = graphene.String(required=True)

class Course(OdooObjectType):
    name = graphene.String(required=True)
    description = graphene.String()
    lessons = graphene.List(graphene.NonNull(lambda: Lesson), required=True)

    @staticmethod
    def resolve_lessons(root, info):
        return root.slide_ids

class Query(graphene.ObjectType):
    all_courses = graphene.List(
        graphene.NonNull(Course),
        required=True,
        limit=graphene.Int(),
        offset=graphene.Int(),
    )
    @staticmethod
    def resolve_all_courses(root, info, limit=None, offset=None):
        domain = []
        return info.context["env"]["slide.channel"].search(
            domain, limit=limit, offset=offset
        )

schema = graphene.Schema(query=Query)
