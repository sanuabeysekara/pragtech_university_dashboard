from odoo import fields, models, api, _


class CreateTimetables(models.Model):
    _name = 'create.timetables'
    _description = 'Create Timetables'
    _rec_name = 'classroom_id'

    name = fields.Char(required=True, string="Name")
    timetable_start_date = fields.Date('Start Date')
    timetable_end_date = fields.Date('End Date')
    student_class_id = fields.Many2one('students.class', 'Class', required=True)
    classroom_id = fields.Many2one('class.rooms', 'Class Room', required=True)
    academic_year_id = fields.Many2one('academic.year', 'Academic Year', required=True)
    active = fields.Boolean(default=True)

    monday_line_ids = fields.One2many('day.timetable.line', 'timetable_monday_id', invisible=True)
    tuesday_line_ids = fields.One2many('day.timetable.line', 'timetable_tuesday_id', invisible=True)
    wednesday_line_ids = fields.One2many('day.timetable.line', 'timetable_wednesday_id', invisible=True)
    thursday_line_ids = fields.One2many('day.timetable.line', 'timetable_thursday_id', invisible=True)
    friday_line_ids = fields.One2many('day.timetable.line', 'timetable_friday_id', invisible=True)
    saturday_line_ids = fields.One2many('day.timetable.line', 'timetable_saturday_id', invisible=True)
    sunday_line_ids = fields.One2many('day.timetable.line', 'timetable_sunday_id', invisible=True)


    @api.onchange('student_class_id')
    def timetable_class_class_room(self):
        for rec in self:
            return {'domain': {'classroom_id': [('student_class_id', '=', rec.student_class_id.id)]}}

    # @api.model
    # def default_get(self, fields):
    #     res = super(CreateTimetables, self).default_get(fields)
    #     period_lines = []
    #     all_periods = self.env['timetable.period.time'].search([])
    #     for rec in all_periods:
    #         line = (0, 0, {
    #             'period_timing_id': rec.id
    #         })
    #         period_lines.append(line)
    #     res.update({
    #         'monday_line_ids': period_lines,
    #         'tuesday_line_ids': period_lines,
    #         'wednesday_line_ids': period_lines,
    #         'thursday_line_ids': period_lines,
    #         'friday_line_ids': period_lines,
    #         'saturday_line_ids': period_lines,
    #         'sunday_line_ids': period_lines
    #
    #     })
    #     return res



class DayTimetableLine(models.Model):
    _name = 'day.timetable.line'
    _description = 'Day Timetable Line'

    timetable_monday_id = fields.Many2one('create.timetables')
    timetable_tuesday_id = fields.Many2one('create.timetables')
    timetable_wednesday_id = fields.Many2one('create.timetables')
    timetable_thursday_id = fields.Many2one('create.timetables')
    timetable_friday_id = fields.Many2one('create.timetables')
    timetable_saturday_id = fields.Many2one('create.timetables')
    timetable_sunday_id = fields.Many2one('create.timetables')

    period_timing_id = fields.Many2one('timetable.period.time', 'Period')
    # teacher_id = fields.Many2one('teacher.master', 'Teacher')
    class_subject_id = fields.Many2one('class.subjects', 'Subjects')


    # subjects show only particular class subjects
    @api.onchange('class_subject_id')
    def timetable_class_subject(self):
        for rec in self:
            list_classes = []
            if rec.timetable_monday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_monday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}

            if rec.timetable_tuesday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_tuesday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}

            if rec.timetable_wednesday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_wednesday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}

            if rec.timetable_thursday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_thursday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}

            if rec.timetable_friday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_friday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}

            if rec.timetable_saturday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_saturday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}

            if rec.timetable_sunday_id.student_class_id:
                list_classes = self.env['class.subjects'].search([('student_class_sub_id', '=',
                                                                  rec.timetable_sunday_id.student_class_id.id)]).ids
                return {'domain': {'class_subject_id': [('id', 'in', list_classes)]}}


