from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class StudentMaster(models.Model):
    _name = 'student.master'
    _description = 'Academic Students'
    _inherit = "mail.thread"
    _rec_name = 'first_name'

    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name')
    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    date_of_birth = fields.Date('Date Of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')], )
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
    active = fields.Boolean(default=True)
    admission_master_id = fields.Many2one('admission.master', 'Enrollment Register', readonly=True)
    enrollment_no = fields.Char('Enrollment No', readonly=True)
    enrollment_date = fields.Datetime('Enrollment Date', readonly=True)
    student_class_id = fields.Many2one('students.class', 'Class', readonly=True)
    previous_academy = fields.Char('Previous Academy', readonly=True)
    previous_class = fields.Char('Previous Class', readonly=True)
    previous_result = fields.Char('Previous Result', readonly=True)

    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    email = fields.Char()
    mobile = fields.Char()

    guardian_name = fields.Char(string='Name')
    guardian_email = fields.Char(string='Email')
    guardian_mobile = fields.Char(string='Mobile')
    student_relationship = fields.Char(string='Student Relationship')

    fees_history_ids = fields.Many2many('fees.management.line', 'fees_student_rel', 'student_id', 'fees_id')
    students_class_id = fields.Many2one('class.rooms', invisible=True)
    students_class_ids = fields.One2many('classes.data', 'inv_student_class_id', invisible=True,)
    guardian_user_id = fields.Many2one('res.users', ondelete="cascade")
    guardian_partner_id = fields.Many2one('res.partner', ondelete="cascade")
    student_partner_id = fields.Many2one('res.partner', ondelete="cascade")
    partner_id = fields.Many2one('res.partner', ondelete="cascade") 
    name = fields.Char(string='Student Id')
    

    @api.model
    def create(self, vals_list):
        if vals_list.get('name', 'New') == 'New':
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'student.id.generate') or 'New'
        return super(StudentMaster, self).create(vals_list)



    @api.constrains('date_of_birth')
    def _date_of_birth_val(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError(_(
                    "Can't be born on the upcoming date!! Please enter birth date less than current date."))

    def create_portal_user(self):
        if not self.user_id:
            if self.email:
                new_user_id = self.env['res.users'].sudo().create({
                    'name': self.first_name,
                    'login': self.email,
                    'groups_id': [(6, 0, [self.env.ref('pragtech_university_dashboard.group_student_user').id,
                                          self.env.ref('base.group_portal').id])],
                })
                self.user_id = new_user_id.id
            else:
                raise ValidationError(_("Please enter email..! Its login user name"))
        else:
            raise ValidationError(_("This User Already Exist"))

    class ClassesData(models.Model):
        _name = 'classes.data'
        _description = 'Students Classes'

        inv_student_class_id = fields.Many2one('student.master')
        academic_year_id = fields.Many2one('academic.year', required=True)
        student_class_id = fields.Many2one('students.class', string='Classes', required=True)
        class_room_id = fields.Many2one('class.rooms', string='Class Rooms')

        @api.onchange('student_class_id')
        def exam__attend_class_class_room(self):
            for rec in self:
                return {'domain': {'class_room_id': [('student_class_id', '=', rec.student_class_id.id)]}}
