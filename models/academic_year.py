from odoo import fields, models


class AcademicYear(models.Model):
    _name = 'academic.year'
    _description = 'Academic Year'

    name = fields.Char('Academic Year', required=True)
    academic_start_date = fields.Date('Start Date', required=True)
    academic_end_date = fields.Date('End Date', required=True)
    active = fields.Boolean(default=True)

    academic_semester = fields.Selection([('two_semester', 'Two Semester'),
                                          ('three_semester', 'Three Semester'),
                                          ('four_semester', 'Four semester'),
                                          ('other', 'Other')],
                                         string="Academic Semesters")
