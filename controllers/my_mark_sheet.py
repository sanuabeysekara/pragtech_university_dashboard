from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalInherit(CustomerPortal):

    @route(['/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        res = super(CustomerPortalInherit, self).home()
        return res

    @route(['/my/exams/'], type='http', auth="user", website=True)
    def exams(self, **kw):
        mark_sheet = request.env['mark.sheet'].sudo().search([])
        values = []
        for rec in mark_sheet:
            if rec.student_id.user_id.id == request.env.user.id:
                values.append({
                    'exams': rec.exam_name_id.name,
                    'academic_yr': rec.exam_name_id.academic_year_id.name,
                    'exam_id': rec.exam_name_id.id,
                    'class': rec.student_class_id.name,
                })
        return request.render("pragtech_university_dashboard.portal_my_exams", {'values': values})

    @route(['/my/mark_sheet/<int:exam_id>'], type='http', auth="user", website=True)
    def my_mark_sheet(self, exam_id,  **kw):
        mark_sheet = request.env['mark.sheet'].sudo().search([('exam_name_id.id', '=', exam_id)])
        values = []
        total_values = {}
        for rec in mark_sheet:
            if rec.student_id.user_id.id == request.env.user.id:
                total_values.update({
                    'exams': rec.exam_name_id.name,
                    'student_name': rec.student_id.first_name,
                    'class': rec.student_class_id.name,
                    'total_exam_pass_marks': rec.total_exam_pass_marks,
                    'total_exam_marks': rec.total_exam_marks,
                    'total_obtained_mark': rec.total_obtained_mark,
                    'total_obtained_percentage': rec.total_obtained_percentage,
                    'result': rec.result,
                })
                for record in rec.mark_sheet_line_ids:
                    values.append({
                        'exam_sub': record.exam_details_id.exam_subject_id.name,
                        'marks': record.marks,
                        'pass_marks': record.pass_marks,
                        'obtained_mark': record.obtained_mark,
                        'grade': record.grade,
                        'percentage': record.percentage,
                        'result_status': record.result_status,
                    })

        return request.render("pragtech_university_dashboard.portal_my_mark_sheet",
                              {'values': values, 'marks': total_values})




