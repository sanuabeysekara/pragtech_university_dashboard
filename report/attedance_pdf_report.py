from odoo.http import request
from odoo import models, api


class ProjectReportParser(models.AbstractModel):
    _name = 'report.pragtech_university_dashboard.report_student_attendance'

    def _get_report_values(self, docids, data=None):
        domain = []
        from_date = data['from_date']
        if from_date:
            domain += [('day_date', '>=', from_date)]
        to_date = data['to_date']
        if to_date:
            domain += [('day_date', '<=', to_date)]
        academic_year = data['academic_year']
        if academic_year:
            domain += [('academic_year_id', '<=', academic_year)]
        student_class = data['student_class']
        if student_class:
            domain += [('student_class_id', '<=', student_class)]
        
        student_lines = self.env['students.attendance'].search(domain)

        attendance_line_list = []
        if student_lines:
            for line_id in student_lines:
                student_attendance_lines = self.env['students.attendance.line'].search([('attendance_id', '=', line_id.id)])
                for each in student_attendance_lines:
                    if line_id.half_day == "before_noon":
                        session = 'Before Noon'
                    elif line_id.half_day == "after_noon":
                        session = 'After Noon'
                    else:
                        session = ''
                    if len(student_lines)>0:
                        vals= {
                        'name': each.student_id.first_name,
                        'date':line_id.day_date,
                        'academic_year': line_id.academic_year_id.name,
                        'student_class': line_id.student_class_id.name,
                        'student_class_room':line_id.classroom_id.name,
                        'session':session,
                        'status':each.status,
                        }
                        attendance_line_list.append(vals)
                    else:
                        vals1 =  vals= {
                        'name': False,
                        'date':False,
                        'academic_year': False,
                        'student_class': False,
                        'student_class_room':False,
                        'session':False,
                        'status':False,
                        }
                        attendance_line_list.append(vals1)
        return{
            'attendance':attendance_line_list
        } 


