from odoo import api, fields, models, _
import xlwt, xlsxwriter
import io
import base64
import pdb
from datetime import datetime,timedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError

class AttendanceReport(models.TransientModel):
    _name="wizard.student.attendance.report"
    _description="Student Attendance Report"


    from_date = fields.Date(string="Start Date", required=True, default=datetime.today())
    to_date = fields.Date(string="End Date", required=True, default=datetime.today())
    academic_year = fields.Many2one('academic.year',string="Academic Year")
    student_class = fields.Many2one('students.class',string="Class")



    def print_item_report(self):
        domain = []
        from_date = self.from_date
        if from_date:
            domain += [('day_date', '>=', from_date)]
        to_date = self.to_date
        if to_date:
            domain += [('day_date', '<=', to_date)]
        if self.academic_year:
            domain += [('academic_year_id', '=', self.academic_year.id)]
        if self.student_class:
            domain += [('student_class_id', '=', self.student_class.id)]
        
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

        if attendance_line_list:
            unlink_obj = self.env['student.attendance.report'].search([])
            unlink_obj.unlink()
            for new_line in attendance_line_list:
                report_attendance = self.env['student.attendance.report'].create(new_line)            
            return {
                'name': _('Attendance Report'),
                'type': 'ir.actions.act_window',
                'res_model': 'student.attendance.report',
                'view_mode':'tree',
                'target': 'current',
            }
        else:
            raise UserError('Sorry no records found')    
            





    def print_pdf_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'from_date':self.from_date,
            'to_date':self.to_date,
            'academic_year':self.academic_year.id,
            'student_class':self.student_class.id
        }
        return self.env.ref('pragtech_university_dashboard.action_attendance_pdf').report_action(self, data=data)

