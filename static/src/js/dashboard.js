odoo.define('pragtech_university_dashboard.Dashboard', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;

    var CustomDashboard = AbstractAction.extend({
        template: 'pragtech_university_dashboard.edu_dashboard_template',
        events:{
            'click .students': '_onClickStudents',
            'click .teachers': '_onClickTeachers',
            'click .admissions': '_onClickAdmissions',
            'click .timetable': '_onClickTimetable',
            'click .assignment': '_onClickAssignments',
            'click .exam': '_onClickExam',
            'click .attendance': '_onClickAttendance',
            'click .fees': '_onClickFees',
        },

        _onClickStudents:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                name:'Students',
                res_model: 'student.master',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
            debugger
        },

        _onClickTeachers:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'teacher.master',
                name:'Teachers',
                views: [[false, 'kanban'], [false, 'list'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
        },

         _onClickAdmissions:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'admission.master',
                name:'Admission Registers',
                views: [[false, 'list'], [false, 'kanban'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
         },

         _onClickTimetable:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'create.timetables',
                name:'Timetable',
                views: [[false, 'list'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
         },

        //  _onClickAssignments:function(ev) {
        //     var $target = $(ev.currentTarget);
        //     this.do_action({
        //         type: 'ir.actions.act_window',
        //         res_model: 'assignment.master',
        //         name:'Assignments',
        //         views: [[false, 'list'], [false, 'kanban'], [false, 'form']],
        //         view_mode: 'list',
        //         target: 'current',
        //     });
        //  },

         _onClickExam:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'exam.master',
                name:'Exams ',
                views: [[false, 'list'], [false, 'kanban'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
         },

         _onClickAttendance:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'students.attendance',
                name:'Attendance ',
                views: [[false, 'list'], [false, 'kanban'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
         },


         _onClickFees:function(ev) {
            var $target = $(ev.currentTarget);
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'fees.management',
                name:'Fees Payment ',
                views: [[false, 'list'], [false, 'form']],
                view_mode: 'list',
                target: 'current',
            });
         },

        init: function (parent, action) {
            this._super(parent, action);
            this.url = action.params.url;
        },

        willStart: function () {
            var self = this;
            var defs = [];
            var def = this._super.apply(this, arguments);
            defs.push(def);
            return $.when.apply($, defs);
        },

        start: function () {
            var self = this;
            var defs = [];
            var def = this._super.apply(this,arguments);
            return $.when.apply($,defs);
        },

        destroy: function () {
            this._super.apply(this, arguments);
        }
    });

    core.action_registry.add('pragtech_university_dashboard', CustomDashboard);
});
