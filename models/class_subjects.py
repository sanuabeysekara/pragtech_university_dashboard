from odoo import models, fields


class SubjectClass(models.Model):
    _name = 'students.class'
    _description = 'Class'

    name = fields.Char('Class Name', required=True)

    class_subject_ids = fields.One2many('class.subjects', 'student_class_sub_id')
    active = fields.Boolean(default=True)




class ClassSubjects(models.Model):
    _name = 'class.subjects'
    _description = 'Class Subjects'
    _inherit = 'mail.thread'

    student_class_sub_id = fields.Many2one('students.class', string='Class', invisible=True)
    name = fields.Char('Name', required=True)
    sub_category = fields.Selection([
        ('core', 'Core'),
        ('elective', 'Elective')
    ], string='Subject Category')
    sub_exam_type = fields.Selection([
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('both', 'Theory & Practical'),
        ('other', 'Other')
    ], string='Subject Type')


