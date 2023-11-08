from odoo import fields, models, api, _


class SchoolAssignments(models.Model):
    _name = 'assignment.master'
    _description = 'Assignments Master'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    class_room_id = fields.Many2one('class.rooms', 'Class Room', )
    class_subject_id = fields.Many2one('class.subjects', 'Subjects')
    teacher_id = fields.Many2one('teacher.master', 'Assigned By', required=True)
    generate_date = fields.Date('Generate Date', default=lambda self: fields.Date.today())
    last_date = fields.Date('Last Date Of Completion')
    assignment_mark = fields.Char('Total Mark')
    active = fields.Boolean(default=True)
    assignment_task = fields.Text('Questions', required=True)
    assigned_students_ids = fields.One2many('assignment.student', 'assignment_student_id',
                                            'Assigned To')
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)

    @api.onchange('student_class_id')
    def assignment_class_class_room(self):
        for rec in self:
            return {'domain': {
                'class_room_id': [('student_class_id', '=', rec.student_class_id.id)],
                'class_subject_id': [('student_class_sub_id', '=', rec.student_class_id.id)]
                             }
                    }


class MasterStudent(models.Model):
    _name = 'assignment.student'

    student_id = fields.Many2one('student.master', 'Student')
    assignment_student_id = fields.Many2one('assignment.master', invisible=True)

    @api.onchange('student_id')
    def student_assign_class_class_room(self):
        list_assign_students = []
        for rec in self:
            if rec.assignment_student_id.class_room_id:
                list_assign_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.assignment_student_id.academic_year_id.id),
                    ('student_class_id', '=', rec.assignment_student_id.student_class_id.id),
                    ('class_room_id', '=', rec.assignment_student_id.class_room_id.id)
                ])
                for st in list_assign_class:
                    for student in st.inv_student_class_id:
                        list_assign_students.append(student.id)
            else:
                list_assign_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.assignment_student_id.academic_year_id.id),
                    ('student_class_id', '=', rec.assignment_student_id.student_class_id.id)
                ])
                for st in list_assign_class:
                    for student in st.inv_student_class_id:
                        list_assign_students.append(student.id)
            return {'domain': {'student_id': [('id', 'in', list_assign_students)]}}
