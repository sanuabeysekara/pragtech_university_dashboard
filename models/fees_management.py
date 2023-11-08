from odoo import fields, models, api


class FeesManagement(models.Model):
    _name = 'fees.management'
    _description = 'Fees Management'
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.master', required=True)
    student_fee_ids = fields.One2many('fees.management.line', 'fee_relation_id')
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    class_room_id = fields.Many2one('class.rooms', 'Class Room', required=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)
    active = fields.Boolean(default=True)


    @api.onchange('student_class_id')
    def fees_class_class_room(self):
        for rec in self:
            return {'domain': {'class_room_id': [('student_class_id', '=', rec.student_class_id.id)]}}


    @api.model_create_multi
    def create(self, vals_list):
        res = super(FeesManagement, self).create(vals_list)
        res.student_id.update({
            'fees_history_ids': [(6, 0, res.student_fee_ids.ids)],
        })
        return res

    @api.onchange('student_class_id', 'class_room_id', 'academic_year_id')
    def check_domain_student(self):
        list_fees_stud = []
        for rec in self:
            if rec.class_room_id:
                list_fees_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.academic_year_id.id),
                    ('student_class_id', '=', rec.student_class_id.id),
                    ('class_room_id', '=', rec.class_room_id.id)
                ])
                for st in list_fees_class:
                    for student in st.inv_student_class_id:
                        list_fees_stud.append(student.id)
            else:
                list_fees_class = self.env['classes.data'].search([
                    ('academic_year_id', '=', rec.academic_year_id.id),
                    ('student_class_id', '=', rec.student_class_id.id)
                ])
                for st in list_fees_class:
                    for student in st.inv_student_class_id:
                        list_fees_stud.append(student.id)
            return {'domain': {'student_id': [('id', 'in', list_fees_stud)]}}


class FeesManagementLine(models.Model):
    _name = 'fees.management.line'
    _description = 'Students Fees Management Line'

    fee_id = fields.Many2one('product.product', 'Fees Type', required=True)
    fee_amount = fields.Float('Fees Amount')
    fee_relation_id = fields.Many2one('fees.management', invisible=True)
    fees_invoice_id = fields.Many2one('account.move', 'Invoice ID')
    state = fields.Selection(related='fees_invoice_id.state', string='Invoice Status', readonly=True)
    payment_state = fields.Selection(related='fees_invoice_id.payment_state', string='Payment Status', readonly=True)

    @api.onchange('fee_id')
    def fee_amount_onchange(self):
        self.fee_amount = self.fee_id.list_price

    def action_inv_create(self):
        invoice_id = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.fee_relation_id.student_id.guardian_partner_id.id,
            'student_id': self.fee_relation_id.student_id.id,
            'is_fees': True,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.fee_id.id,
                'quantity': 1.0,
                'price_unit': self.fee_amount,
            })]
        })
        self.fees_invoice_id = invoice_id.id

    def action_inv_view(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.move',
            'target': 'current',
            'res_id': self.fees_invoice_id.id,
        }
