from odoo.http import request, Controller, route
from odoo.addons.portal.controllers.portal import CustomerPortal
import werkzeug.utils


class CustomerPortalInherit(CustomerPortal):

    @route(['/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        res = super(CustomerPortalInherit, self).home()
        return res

    @route(['/my/assignments'], type='http', auth="user", website=True)
    def assignments(self, **kw):
        assignments = request.env['assignment.master'].sudo().search([])
        values = []
        for rec in assignments:
            for student_line in rec.assigned_students_ids:
                submit_assignment = request.env['completed.assignment'].sudo().search(
                    [('assignment_master_id', '=', rec.id), ('students_id', '=', student_line.student_id.id)], limit=1)
                if student_line.student_id.user_id.id == request.env.user.id:
                    line = {
                        'assignments': rec.name,
                        'subject': rec.class_subject_id.name,
                        'class': rec.student_class_id.name,
                        'assign_date': rec.generate_date,
                        'submission_date': rec.last_date,
                        'total_mark': rec.assignment_mark,
                        'assigned_by': rec.teacher_id.name,
                        'assignment_id': rec,
                        'have_assignments': True if submit_assignment else False,
                        'validate_mark': submit_assignment.obtained_mark,
                        'complete_asgmnt_state': submit_assignment.state,
                    }
                    values.append(line)
        return request.render("pragtech_university_dashboard.portal_my_assignments_management", {'values': values})

    @route(['/my/view_assignment/<int:assignment_id>'], type='http', auth="user", website=True)
    def render_assignments_backend_view(self, assignment_id, **kw):
        assignment = request.env['assignment.master'].sudo().browse(int(assignment_id))
        values = {
            'assignment_question': assignment.assignment_task,
            'assignment_view_id': assignment.id,
        }
        return request.render("pragtech_university_dashboard.portal_my_assignment_submission", values)

    @route(['/create/completed_assignment'], type='http', auth="user", website=True)
    def create_completed_assignment(self, **kw):
        vals_list = [{
            'completed_task_description': kw.get('assignment_answer'),
            'assignment_master_id': kw.get('assignment_view_id'),
            'students_id': request.env['student.master'].sudo().search([('user_id', '=', request.env.user.id)],
                                                                       limit=1).id,
        }]
        request.env['completed.assignment'].sudo().create(vals_list)
        return request.render("pragtech_university_dashboard.portal_my_assignment_submission_completed")
