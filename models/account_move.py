from odoo import api,models,fields,_ 


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    student_id = fields.Many2one('student.master',string="Student")
    is_fees = fields.Boolean("Is Fees")

