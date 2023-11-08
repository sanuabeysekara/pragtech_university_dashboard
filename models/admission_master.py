from odoo import fields, models


class AdmissionMaster(models.Model):
    _name = 'admission.master'
    _description = 'Admission Master'
    _inherit = 'mail.thread'

    name = fields.Char('Register Name', required=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)

    active = fields.Boolean(default=True)

    enrolled_students_ids = fields.One2many('enroll.mechanism', 'admission_master_id')

    # def get_academic_student(self):
    #     academic_students = {}
    #     for academic_year in self:
    #         student_count = len(academic_year.enrolled_students_ids)
    #         academic_students[academic_year.id] = {
    #             'name': academic_year.name,
    #             'academic_year_id': academic_year.academic_year_id.name,
    #             'student_count': student_count,
    #         }
    #     return academic_students







