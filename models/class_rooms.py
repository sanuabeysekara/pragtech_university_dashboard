from odoo import models, fields


class ClassRooms(models.Model):
    _name = 'class.rooms'
    _description = 'Class Rooms'

    name = fields.Char('Name', required=True)
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    class_strength = fields.Char('Class Room Strength')
    active = fields.Boolean(default=True)


    class_students_ids = fields.Many2many('student.master', 'student_class_rel', 'class_room_id', 'student_id')







