from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class MarkSheet(models.Model):
    _name = 'mark.sheet'
    _description = 'Mark Sheet'
    _rec_name = 'exam_name_id'

    exam_name_id = fields.Many2one('exam.master', required=True)
    student_id = fields.Many2one('student.master', 'Student', required=True)
    mark_sheet_line_ids = fields.One2many('mark.sheet.line', 'inv_mark_sheet_id')
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    class_room_id = fields.Many2one('class.rooms', 'Class Rooms')
    active = fields.Boolean(default=True)
    total_exam_marks = fields.Float('Total Mark', compute="_compute_total_exam_marks", )
    total_exam_pass_marks = fields.Float('Total Pass Marks', compute="_compute_total_exam_pass_marks")
    total_obtained_mark = fields.Float('Total Obtained Marks', compute="_compute_total_obtained_mark")
    total_obtained_percentage = fields.Float('Total Percentage', compute="_compute_total_obtained_percentage")
    result = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ], compute="_compute_final_result", store=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)

    _sql_constraints = [
        ('module_exam_name_id_student_id_unique', 'unique(exam_name_id, student_id)',
         'Duplicate not allowed.Already exist this student.'),
    ]

    @api.onchange('exam_name_id')
    def exam_subject(self):
        self.academic_year_id = self.exam_name_id.academic_year_id.id
        self.student_class_id = self.exam_name_id.student_class_id.id
        self.class_room_id = self.exam_name_id.class_room_id.id

    @api.onchange('student_class_id')
    def mark_sheet_class_class_room(self):
        for rec in self:
            return {'domain': {'class_room_id': [('student_class_id', '=', rec.student_class_id.id)]}}

    def _compute_total_obtained_percentage(self):
        for record in self:
            if record.total_exam_marks > 0:
                record.total_obtained_percentage = 100 * record.total_obtained_mark / record.total_exam_marks
            else:
                record.total_obtained_percentage = 0

    def _compute_total_exam_marks(self):
        for record in self:
            record.total_exam_marks = sum([x.marks for x in record.mark_sheet_line_ids])

    def _compute_total_exam_pass_marks(self):
        for record in self:
            record.total_exam_pass_marks = sum([x.pass_marks for x in record.mark_sheet_line_ids])

    def _compute_total_obtained_mark(self):
        for record in self:
            record.total_obtained_mark = sum([x.obtained_mark for x in record.mark_sheet_line_ids])

    @api.depends('mark_sheet_line_ids.result_status')
    def _compute_final_result(self):
        for rec in self:
            if rec.mark_sheet_line_ids:
                if 'fail' in rec.mark_sheet_line_ids.mapped('result_status'):
                    rec.result = 'fail'
                else:
                    rec.result = 'pass'
        # fail_exist = False
        # if self.mark_sheet_line_ids:
        #     for lines in self.mark_sheet_line_ids:
        #         if lines.result_status == 'fail':
        #             fail_exist = True
        #             break
        #     if fail_exist:
        #         self.result = 'fail'
        #     else:
        #         self.result = 'pass'

    @api.onchange('student_class_id', 'class_room_id', 'academic_year_id')
    def check_domain(self):
        list_mark_sheet_stud = []
        for rec in self:
            if rec.class_room_id:
                list_mark_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.academic_year_id.id),
                    ('student_class_id', '=', rec.student_class_id.id),
                    ('class_room_id', '=', rec.class_room_id.id)
                ])
                for st in list_mark_class:
                    for student in st.inv_student_class_id:
                        list_mark_sheet_stud.append(student.id)
            else:
                list_mark_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.academic_year_id.id),
                    ('student_class_id', '=', rec.student_class_id.id)
                ])
                for st in list_mark_class:
                    for student in st.inv_student_class_id:
                        list_mark_sheet_stud.append(student.id)
            return {'domain': {'student_id': [('id', 'in', list_mark_sheet_stud)]}}


class MarkSheetLine(models.Model):
    _name = 'mark.sheet.line'
    _description = 'Mark Sheet Line'

    inv_mark_sheet_id = fields.Many2one('mark.sheet')
    exam_details_id = fields.Many2one('exam.subjects.line', string='Exam', required=True)
    marks = fields.Float('Total Mark', required=True)
    pass_marks = fields.Float('Pass Mark', required=True)
    obtained_mark = fields.Float('Obtained Mark', required=True)
    grade = fields.Char('Grade', compute="_compute_exam_grade")
    percentage = fields.Float('Percentage', compute="_compute_subject_mark_percentage")
    result_status = fields.Selection([
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ], compute="_compute_result_status")

    @api.onchange('exam_details_id')
    def exam_subject(self):
        for rec in self:
            if rec.inv_mark_sheet_id.exam_name_id:
                list_exam = self.env['exam.subjects.line'].search([('exam_subject_inv_id', '=',
                                                                    rec.inv_mark_sheet_id.exam_name_id.exam_subjects_line_ids.exam_subject_inv_id.id)]).ids
                return {'domain': {'exam_details_id': [('id', 'in', list_exam)]}}

    @api.constrains('marks', 'pass_marks', 'obtained_mark')
    def _check_proper_marks(self):
        for rec in self:
            if (rec.marks <= 0.0) or (rec.pass_marks <= 0.0) or (rec.obtained_mark <= 0.0):
                raise ValidationError(_("Enter +ve marks..!"))
            if (rec.marks < rec.pass_marks) or (rec.marks < rec.obtained_mark):
                raise ValidationError(_("Mark can't be greater than Total Mark..!"))

    def _compute_subject_mark_percentage(self):
        for record in self:
            record.percentage = 100 * record.obtained_mark / record.marks

    def _compute_exam_grade(self):
        for record in self:
            grade_master_ids = self.env['grade.master'].search([])
            if grade_master_ids:
                for grade_rec_id in grade_master_ids:
                    if grade_rec_id.minimum_mark <= record.obtained_mark and grade_rec_id.maximum_mark >= record.obtained_mark:
                        record.grade = grade_rec_id.grade
            else:
                record.grade = None

    def _compute_result_status(self):
        for record in self:
            if record.pass_marks <= record.obtained_mark:
                record.result_status = 'pass'
            else:
                record.result_status = 'fail'
