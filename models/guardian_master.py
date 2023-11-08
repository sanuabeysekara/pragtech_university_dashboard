from odoo import fields, models, _, api


class GuardianMaster(models.Model):
    _name = 'guardian.master'
    _inherits = {"res.partner": "partner_id"}
    _inherit = 'mail.thread'

    teacher_first_name = fields.Char('First Name', required=True)
    teacher_last_name = fields.Char('Last Name')

    student_relationship = fields.Char(string='Student Relationship', required=1)

    user_id = fields.Many2one('res.users', ondelete="cascade", string='Guardian User Name')

    enroll_student_guardians_id = fields.Many2one('enroll.mechanism', invisible=True)
    student_master_guardians_id = fields.Many2one('student.master', invisible=True)

    def my_students(self):
        my_students = self.env['student.master'].search(
            [('id', 'in', self.student_master_guardians_id.students_guardian_ids.ids)])
        return {'domain': {'student_master_guardians_id': [('id', 'in', my_students.ids)]}}

