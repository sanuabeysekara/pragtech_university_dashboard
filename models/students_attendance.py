from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StudentsAttendance(models.Model):
    _name = 'students.attendance'
    _description = 'Students Attendance'
    _rec_name = 'day_date'

    day_date = fields.Date('Date', required=True)
    half_day = fields.Selection([('before_noon', 'Before Noon'),
                                 ('after_noon', 'After Noon')]
                                 ,string="Session")
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)
    classroom_id = fields.Many2one('class.rooms', 'Class Room', required=True)
    active = fields.Boolean(default=True)

    student_attendance_ids = fields.One2many('students.attendance.line', 'attendance_id')

    @api.onchange('student_class_id')
    def attendance_class_class_room(self):
        for rec in self:
            return {'domain': {'classroom_id': [('student_class_id', '=', rec.student_class_id.id)]}}
        

    def action_fill_student(self,):
        for rec in self:
            if not rec.academic_year_id or not rec.student_class_id or not rec.classroom_id.name:
                raise ValidationError(_("Please Fill All The Required Details!"))
            
            classroom = self.env['classes.data'].search([
                ('academic_year_id', '=', rec.academic_year_id.id),
                ('student_class_id', '=', rec.student_class_id.id),
                ('class_room_id', '=', rec.classroom_id.name),
            ])
            for each in classroom:
                for student in each.inv_student_class_id:
                    attendance_line = rec.student_attendance_ids.filtered(lambda l: l.student_id == student)
                    if not attendance_line:
                        attendance_line = self.env['students.attendance.line'].create({
                            'attendance_id': self.id,
                            'student_id': student.id,
                        })
                    else:
                        attendance_line.student_id = student.id

class StudentsAttendanceLIne(models.Model):
    _name = 'students.attendance.line'
    _description = 'Students Attendance Line'

    attendance_id = fields.Many2one('students.attendance')
    student_id = fields.Many2one('student.master', 'Student')
    presented = fields.Boolean('Present')
    absented = fields.Boolean('Absent')
    status = fields.Selection([('Present', 'Present'),
                                 ('Absent', 'Absent')])

    notes = fields.Char('Remarks')



    @api.onchange('presented', 'absented')
    def student_attendance(self):
        for record in self:
            if record.presented and record.absented:
                raise ValidationError(_("Can't possible for a student to be absent and present at the same time...!"))
            if record.presented:
                record.status = 'Present'
            elif record.absented:
                record.status = 'Absent'
            else:
                record.status = False
    @api.onchange('student_id')
    def student_attendance_class_class_room(self):
        list_class_students = []
        for rec in self:
            list_class = self.env['classes.data'].search([
                ('academic_year_id', '=', rec.attendance_id.academic_year_id.id),
                ('student_class_id', '=', rec.attendance_id.student_class_id.id),
                ('class_room_id', '=', rec.attendance_id.classroom_id.name),
            ])
            for st in list_class:
                for student in st.inv_student_class_id:
                    list_class_students.append(student.id)
        return {'domain': {'student_id': [('id', 'in', list_class_students)]}}
    

class AttendanceReport(models.Model):
    _name = "student.attendance.report"

    name = fields.Char(string="Student Name")
    academic_year = fields.Char(string="Academic year")
    student_class = fields.Char(string="Class")
    student_class_room = fields.Char(string="Class Room")
    session = fields.Char(string="Session")
    status = fields.Char(string="Status")
    date = fields.Date(string="Date")  

