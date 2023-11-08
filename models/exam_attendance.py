from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ExamAttendance(models.Model):
    _name = 'exam.attendance'
    _description = 'Exam Attendance'
    _rec_name = 'exam_name_id'

    exam_name_id = fields.Many2one('exam.master', required=True)
    exam_details_id = fields.Many2one('exam.subjects.line', string='Exam Subject', required=True,)
    student_class_id = fields.Many2one('students.class', 'Class', required=True,)
    class_room_id = fields.Many2one('class.rooms', 'Class Room')
    exam_attendance_ids = fields.One2many('exam.attendance.line', 'inv_attendance_id')
    exam_hall = fields.Many2many('class.rooms', 'exam_exam_hall_relation', 'exam_data_id', 'exam_hall_data_id',
                                 'Exam Hall',)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)
    active = fields.Boolean(default=True)
    exam_start_date = fields.Datetime('Start Time', required=True)
    exam_end_date = fields.Datetime('End Time', required=True)


    @api.onchange('student_class_id')
    def exam__attend_class_class_room(self):
        for rec in self:
            return {'domain': {'class_room_id': [('student_class_id', '=', rec.student_class_id.id)]}}

    @api.onchange('exam_name_id')
    def exam_subject(self):
        self.academic_year_id = self.exam_name_id.academic_year_id.id
        self.student_class_id = self.exam_name_id.student_class_id.id
        self.class_room_id = self.exam_name_id.class_room_id.id
        for rec in self:
            if rec.exam_name_id.exam_subjects_line_ids:
                list_class_subj = self.env['exam.subjects.line'].search([('exam_subject_inv_id', '=',
                                                     rec.exam_name_id.exam_subjects_line_ids.exam_subject_inv_id.id)]).ids
                return {'domain': {'exam_details_id': [('id', 'in', list_class_subj)]}}

    @api.onchange('exam_details_id')
    def exam_exam_details_id(self):
        for rec in self:
            if rec.exam_details_id:
                selected_subject_id = rec.exam_details_id.exam_subject_id
                matching_subject = rec.exam_details_id.exam_subject_inv_id.exam_subjects_line_ids.filtered(lambda line: line.exam_subject_id == selected_subject_id)
                if matching_subject:
                    exam_start_date = matching_subject[0].exam_start_date
                    exam_end_date = matching_subject[0].exam_end_date
                    rec.exam_start_date = exam_start_date
                    rec.exam_end_date = exam_end_date
            return {'domain': {'exam_hall': [('id', 'in', rec.exam_details_id.exam_subject_inv_id.exam_subjects_line_ids.exam_hall.ids)]}}


class ExamAttendanceLine(models.Model):
    _name = 'exam.attendance.line'
    _description = 'Exam Attendance Line'

    inv_attendance_id = fields.Many2one('exam.attendance')
    student_id = fields.Many2one('student.master', 'Student')
    exam_presented = fields.Boolean('Present')
    exam_absented = fields.Boolean('Absent')
    exam_notes = fields.Char('Remarks')

    @api.onchange('exam_presented', 'exam_absented')
    def exam_exam_attendance(self):
        for rec in self:
            if rec.exam_presented and rec.exam_absented:
                raise ValidationError(_("Can't possible for a student to be absent and present at the same time...!"))

    @api.onchange('student_id')
    def student_exams_attend(self):
        list_class_exm_students = []
        for rec in self:
            if rec.inv_attendance_id.class_room_id.id:
                list_exm_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.inv_attendance_id.academic_year_id.id),
                    ('student_class_id', '=', rec.inv_attendance_id.student_class_id.id),
                    ('class_room_id', '=', rec.inv_attendance_id.class_room_id.id),
                ])
                for st in list_exm_class:
                    for student in st.inv_student_class_id:
                        list_class_exm_students.append(student.id)
                return {'domain': {'student_id': [('id', 'in', list_class_exm_students)]}}
            else:
                list_exm_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.inv_attendance_id.academic_year_id.id),
                    ('student_class_id', '=', rec.inv_attendance_id.student_class_id.id),
                ])
                for st in list_exm_class:
                    for student in st.inv_student_class_id:
                        list_class_exm_students.append(student.id)
                return {'domain': {'student_id': [('id', 'in', list_class_exm_students)]}}




















