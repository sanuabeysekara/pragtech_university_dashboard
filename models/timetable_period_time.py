from odoo import fields, models, api


class TimetablePeriodTime(models.Model):
    _name = "timetable.period.time"
    _description = "Timetable Period Time"

    name = fields.Char('Name', required=True)
    start_time = fields.Float('Start Time', required=True)
    end_time = fields.Float('End Time', required=True)
    active = fields.Boolean(default=True)
