from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class TeacherMaster(models.Model):
    _name = 'teacher.master'
    _description = 'Teacher Master'
    _inherits = {"res.partner": "partner_id"}
    _inherit = 'mail.thread'

    teacher_first_name = fields.Char('First Name', required=True)
    teacher_last_name = fields.Char('Last Name')
    teacher_id = fields.Char(string='Teacher Id')
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)

    date_of_birth = fields.Date('Date Of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')])
    blood_gp = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ])
    visa_details = fields.Char('Visa Details')

    alternate_contact = fields.Char('Alternate Contact')
    user_id = fields.Many2one('res.users', ondelete="cascade", readonly=True)
    partner_id = fields.Many2one('res.partner', ondelete="cascade",)
    active = fields.Boolean(default=True)

    @api.onchange('teacher_first_name', 'teacher_last_name')
    def _partner_name(self):
        full_name = str(self.teacher_first_name)
        if self.teacher_last_name:
            full_name += " " + str(self.teacher_last_name)
        self.name = full_name

    def create_teacher_user(self):
        if not self.user_id:
            if self.email:
                new_user_id = self.env['res.users'].create({
                    'name': self.name,
                    'login': self.email,
                    'partner_id': self.partner_id.id,
                    'groups_id': [(6, 0, [self.env.ref('pragtech_university_dashboard.group_teacher_user').id,
                                          self.env.ref('base.group_user').id])],
                })
                self.user_id = new_user_id.id
            else:
                raise ValidationError(_("Please enter email..! Its login user name"))
        else:
            raise ValidationError(_("This User Already Exist"))
        

    @api.model
    def create(self, vals_list):
        if vals_list.get('teacher_id', 'New') == 'New':
            vals_list['teacher_id'] = self.env['ir.sequence'].next_by_code(
                'teacher.id.generate') or 'New'
        return super(TeacherMaster, self).create(vals_list)
        

    
