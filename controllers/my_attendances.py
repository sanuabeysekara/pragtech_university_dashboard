from odoo.http import request, Controller, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalInherit(CustomerPortal):

    @route(['/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        res = super(CustomerPortalInherit, self).home()
        return res

    @route(['/my/attendances'], type='http', auth="user", website=True)
    def attendances(self, **kw):
        students_attendances = request.env['students.attendance'].sudo().search([])
        student_rec = []
        for student in students_attendances:
            for student_line in student.student_attendance_ids:
                if student_line.student_id.user_id.id == request.env.user.id:
                    line = {
                        'date': student.day_date,
                        'class': student.student_class_id.name,
                        'half_day': student.half_day,
                        'presented': student_line.presented,
                        'absented': student_line.absented,
                        'notes': student_line.notes
                    }
                    student_rec.append(line)
                # else:
                #     guardian_students = request.env['student.master'].sudo().search([('guardian_user_id', '=', request.env.user.id)])
                #     for rec in guardian_students:
                #         if rec.guardian_user_id.id == request.env.user.id:
                #             own_students = request.env['students.attendance.line'].sudo().search([("student_id", "=", rec.id)])
                #             for attendance_line in own_students:
                #                 line = {
                #                     'date': attendance_line.attendance_id.day_date,
                #                     'class': attendance_line.attendance_id.student_class_id.name,
                #                     'half_day': attendance_line.attendance_id.half_day,
                #                     'presented': attendance_line.presented,
                #                     'absented': attendance_line.absented,
                #                     'notes': attendance_line.notes,
                #                     'students': rec.first_name
                #                 }
                #                 student_rec.append(line)
        return request.render("pragtech_university_dashboard.portal_my_attendances", {'values': student_rec})
