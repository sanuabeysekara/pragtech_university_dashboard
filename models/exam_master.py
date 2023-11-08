from odoo import fields, models, api, _


class ExamMaster(models.Model):
    _name = 'exam.master'
    _description = 'Exam Master'

    name = fields.Char('Exam Name', required=True)
    exam_section_start_date = fields.Date('Start Date')
    exam_section_end_date = fields.Date('End Date')
    exam_subjects_line_ids = fields.One2many('exam.subjects.line', 'exam_subject_inv_id')
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    class_room_id = fields.Many2one('class.rooms', 'Class Room')
    active = fields.Boolean(default=True)

    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)

    @api.onchange('student_class_id')
    def exam_class_class_room(self):
        for rec in self:
            return {'domain': {'class_room_id': [('student_class_id', '=', rec.student_class_id.id)]}}


class ExamSubjectsLine(models.Model):
    _name = 'exam.subjects.line'
    _description = 'Exam Subjects'
    _rec_name = 'exam_subject_id'

    exam_subject_inv_id = fields.Many2one('exam.master')
    exam_subject_id = fields.Many2one('class.subjects', 'Subjects')
    code_no = fields.Char('Code No')
    exam_start_date = fields.Datetime('Start Time', required=True)
    exam_end_date = fields.Datetime('End Time', required=True)
    exam_hall = fields.Many2many('class.rooms', 'exam_exam_hall_rel', 'exam_id', 'exam_hall_id', 'Exam Hall')

    @api.onchange('exam_subject_id')
    def exam_sub_class(self):
        for rec in self:
            if rec.exam_subject_inv_id.student_class_id:
                if self.exam_subject_inv_id.student_class_id:
                    list_class_subj = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                          self.exam_subject_inv_id.student_class_id.id)]).ids
                return {'domain': {'exam_subject_id': [('id', 'in', list_class_subj)]}}
