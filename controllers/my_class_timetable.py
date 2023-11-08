from odoo.http import Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalInherit(CustomerPortal):

    @route(['/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        res = super(CustomerPortalInherit, self).home()
        return res

    @route(['/my/class_timetable'], type='http', auth="user", website=True)
    def class_timetable(self, **kw):
        timetable = request.env['create.timetables'].sudo().search([])
        students_class_data = request.env['student.master'].sudo().search([])
        for students_data in students_class_data:

            if students_data.user_id.id == request.env.user.id:
                # new_values = []
                values = []
                for rec in timetable:
                    for ids_rec in students_data.students_class_ids:
                        if rec.classroom_id.id == ids_rec.class_room_id.id and rec.student_class_id.id == ids_rec.student_class_id.id and rec.academic_year_id.id == ids_rec.academic_year_id.id:
                            values.append({
                                'name': rec.name,
                                'academic_yr': rec.academic_year_id.name,
                                'class': rec.student_class_id.name,
                                'class_room': rec.classroom_id.name,
                                'class_room_id': rec.classroom_id.id,
                                'start_date': rec.timetable_start_date,
                                'end_date': rec.timetable_end_date,
                                'rec_id': rec.id,
                            })
                # for item in values:
                #     if item not in new_values:
                #         new_values.append(item)

                return request.render("pragtech_university_dashboard.portal_my_class_timetable", {'values': values})

    @route(['/my/timetable_chart/<int:timetable_id>'], type='http', auth="user", website=True)
    def my_timetable_chart(self, timetable_id,  **kw):
        table_rec = request.env['create.timetables'].sudo().browse(timetable_id)
        period = request.env['timetable.period.time'].sudo().search([])
        periods = []
        table_monday_values = []
        table_tuesday_values = []
        table_wednesday_values = []
        table_thursday_values = []
        table_friday_values = []
        table_saturday_values = []
        table_sunday_values = []
        title_values = {}
        title_values.update({
                            'academic_yr': table_rec.academic_year_id.name,
                            'class': table_rec.student_class_id.name,
                            'class_room': table_rec.classroom_id.name,
                            'start_date': table_rec.timetable_start_date,
                            'end_date': table_rec.timetable_end_date,
                            })
        for rec in period:
            periods.append({
                'name': rec.name,
                # 'start': rec.start_time,
                # 'end': rec.end_time,
            })
        for rec_line in table_rec.monday_line_ids:
            table_monday_values.append({
                'monday_subjects': rec_line.class_subject_id.name,
            })
        for rec_line in table_rec.tuesday_line_ids:
            table_tuesday_values.append({
                'tuesday_subjects': rec_line.class_subject_id.name,
            })
        for rec_t in table_rec.wednesday_line_ids:
            table_wednesday_values.append({
                'wednesday_subjects': rec_t.class_subject_id.name,
            })
        for rec_t in table_rec.thursday_line_ids:
            table_thursday_values.append({
                'thursday_subjects': rec_t.class_subject_id.name,
            })
        for rec_t in table_rec.friday_line_ids:
            table_friday_values.append({
                'friday_subjects': rec_t.class_subject_id.name,
            })
        for rec_t in table_rec.saturday_line_ids:
            table_saturday_values.append({
                'saturday_subjects': rec_t.class_subject_id.name,
            })
        for rec_t in table_rec.sunday_line_ids:
            table_sunday_values.append({
                'sunday_subjects': rec_t.class_subject_id.name,
            })

        return request.render("pragtech_university_dashboard.portal_my_classroom_timetables",
                              { 'periods':periods, 'title_values': title_values, 'table_monday_values': table_monday_values,
                                'table_tuesday_values': table_tuesday_values, 'table_wednesday_values': table_wednesday_values,
                                'table_thursday_values': table_thursday_values, 'table_friday_values':table_friday_values,
                                'table_saturday_values':table_saturday_values, 'table_sunday_values':table_sunday_values
                                })
