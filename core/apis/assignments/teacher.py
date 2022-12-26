from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.libs import assertions 
from core.models.assignments import Assignment,AssignmentStateEnum,GradeEnum

from .schema import AssignmentSchema, AssignmentSubmitSchema
teachers_assignments_resources = Blueprint('student_assignments_resources',__name__)

@teachers_assignments_resources.route('/assignments',methods=['GET'],strict_slashes=False)
@decorators.auth_principal
def list_assigned_assignment(p):

    submitted_assignment = Assignment.get_assignments_by_teacher(p.teacher_id)
    submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment,many=True)
    return APIResponse.respond(data=submitted_assignment_dump)

@teachers_assignments_resources.route('/assignments/grade',methods=['POST'],strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(principal,incoming_payload):
    assertions.assert_valid(incoming_payload.get('id',False),'id was not found')
    assertions.assert_valid(incoming_payload.get('grade',False),'grade was not found')
    assertions.assert_validation(incoming_payload['grade'] in ['A','B','C','D'], 'invalid grade')
    assignment = Assignment.get_by_id(incoming_payload['id'])

    assertions.assert_found(assignment, 'No assignment with this id was found')
    assertions.assert_valid(assignment.teacher_id == principal.teacher_id, 'This assignment belongs to some other teacher')
    assertions.assert_valid(assignment.state is AssignmentStateEnum.SUBMITTED, 'assignment should be submitted')

    assignment.state = AssignmentStateEnum.GRADED
    assignment.grade = incoming_payload['grade']
    db.session.commit()
    upserted_assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data= upserted_assignment_dump)
