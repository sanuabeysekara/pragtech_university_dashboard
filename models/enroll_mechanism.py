from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_guardian = fields.Boolean()
    is_student = fields.Boolean()
    student_master_id = fields.Many2one('student.master', string='Student Master')

class EnrollMechanism(models.Model):
    _name = 'enroll.mechanism'
    _description = 'Enroll Mechanism'
    _rec_name = 'enrollment_no'


    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)
    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name')
    active = fields.Boolean(default=True)

    admission_master_id = fields.Many2one('admission.master', 'Enrollment Register', required=True)
    enrollment_no = fields.Char('Enrollment No', readonly=True,
                                default=lambda self: self.env['ir.sequence'].next_by_code('enroll.mechanism'))
    enrollment_date = fields.Datetime('Enrollment Date', default=lambda self: fields.Datetime.now())

    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)

    previous_academy = fields.Char('Previous Academy')
    previous_class = fields.Char('Previous Class')
    previous_result = fields.Char('Previous Result')

    date_of_birth = fields.Date('Date Of Birth', required=True)
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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('enrolled', 'Enrolled')
    ], default="draft")
    email = fields.Char()
    mobile = fields.Char()
    user_id = fields.Many2one('res.users', ondelete="cascade", readonly=True)
    student_user_id = fields.Many2one('res.users', ondelete="cascade", readonly=True)
    partner_id = fields.Many2one('res.partner', ondelete="cascade", readonly=True)
    guardian_name = fields.Char(string='Name')
    guardian_email = fields.Char(string='Email')
    guardian_mobile = fields.Char(string='Mobile')
    student_relationship = fields.Char(string='Student Relationship')

    @api.onchange('admission_master_id')
    def admitted_academic_yr(self):
        self.academic_year_id = self.admission_master_id.academic_year_id.id

    @api.onchange('date_of_birth')
    def date_of_birth_validate(self):
        if self.date_of_birth:
            if self.date_of_birth > date.today():
                raise ValidationError(_(
                    "Can't be born on the upcoming date!! Please enter birth date less than current date."))

    def action_create_student_master(self):
        self.state = 'enrolled'

        student_master = self.env['student.master'].create({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_1920': self.image_1920,
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'blood_gp': self.blood_gp,
            'email': self.email,
            'mobile': self.mobile,
            'guardian_partner_id': self.user_id.partner_id.id,
            'admission_master_id': self.admission_master_id.id,
            'enrollment_date': self.enrollment_date,
            'enrollment_no': self.enrollment_no,
            'previous_academy': self.previous_academy,
            'previous_class': self.previous_class,
            'previous_result': self.previous_result,
            'guardian_name': self.guardian_name,
            'guardian_email': self.guardian_email,
            'guardian_mobile': self.guardian_mobile,
            'student_relationship': self.student_relationship,
            'guardian_user_id': self.user_id.id,
            'user_id': self.student_user_id.id,
            'partner_id': self.student_user_id.partner_id.id,

        })
        partner_id = self.user_id.partner_id.id
        if student_master:
            partner = self.env['res.partner'].search([('id', '=', partner_id)], limit=1)
            if partner_id:
                partner.write({
                    'student_master_id': student_master.id,
                })
        
        student_id = self.student_user_id.partner_id.id
        if student_master:
            student = self.env['res.partner'].search([('id', '=', student_id)], limit=1)
            if student_id:
                student.write({
                    'student_master_id': student_master.id,
                })


        self.env['classes.data'].create({
            'academic_year_id': self.academic_year_id.id,
            'student_class_id': self.student_class_id.id,
            'inv_student_class_id': student_master.id,
        })

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        if res.guardian_email:
            user = self.env['res.users'].sudo().create({
                'name': res.guardian_name,
                'login': res.guardian_email,
                'email': res.guardian_email,
                'mobile': res.guardian_mobile,
                'groups_id': [(6, 0, [self.env.ref('pragtech_university_dashboard.group_parent_user').id,
                                      self.env.ref('base.group_portal').id])],
            })
            res.user_id = user.id
        else:
            raise ValidationError(_("Please enter guardian email..! Its login user name"))
        if res.first_name and res.last_name:
            name = res.first_name + res.last_name
        elif res.first_name:
            name = res.first_name
        elif res.last_name:
            name = res.last_name
        else:
            name = None
        
        if res.email:
            student_user = self.env['res.users'].sudo().create({
                    'name': name,
                    'login': res.email,
                    'email': res.email,
                    'mobile': res.mobile,
                    'groups_id': [(6, 0, [self.env.ref('pragtech_university_dashboard.group_student_user').id,
                                        self.env.ref('base.group_portal').id])],
                })
            res.student_user_id = student_user.id
        else:
            raise ValidationError(_("Please enter Student email..! Its login user name"))

        user.partner_id.update({
            'is_guardian': True,
        })
        student_user.partner_id.update({
            'is_student': True,
        })

        return res





