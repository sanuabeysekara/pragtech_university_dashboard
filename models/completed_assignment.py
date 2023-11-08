from odoo import fields, models, api, _


class CompletedAssignment(models.Model):
    _name = 'completed.assignment'
    _description = 'Completed Assignment'
    _rec_name = 'assignment_master_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    assignment_master_id = fields.Many2one('assignment.master', required=True, readonly=True)
    students_id = fields.Many2one('student.master', required=True, readonly=True)
    completed_date = fields.Date('Completed Date', readonly=True, default=lambda self: fields.Date.today())
    obtained_mark = fields.Char('Obtained Mark')
    active = fields.Boolean(default=True)
    completed_task_description = fields.Text('Answered Description', required=True, readonly=True)
    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
    ], default='submitted')

    def submit(self):
        self.state = 'submitted'

    def validate(self):
        self.state = 'validated'

    @api.onchange('assignment_master_id')
    def assignment_students(self):
        if self.assignment_master_id:
            students = self.env['student.master'].search(
                [('id', 'in', self.assignment_master_id.assigned_students_ids.ids)])
            return {'domain': {'students_id': [('id', 'in', students.ids)]}}
