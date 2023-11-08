from odoo import fields, models


class GradeMaster(models.Model):
    _name = 'grade.master'
    _description = 'Grade Master'

    minimum_mark = fields.Float('Minimum Mark')
    maximum_mark = fields.Float('Maximum Mark')
    grade = fields.Char('Grade')
    active = fields.Boolean(default=True)

