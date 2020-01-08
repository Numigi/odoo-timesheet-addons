odoo.define("timesheet_multi_line_wizard_grid.GridController", function (require) {
"use strict";

var core = require("web.core");
var dialogs = require('web.view_dialogs');

var _t = core._t;

require("web_grid.GridController").include({
    _onAddLine(event) {
        event.preventDefault();

        if(this._isTimesheetGrid()){
            this._openTimesheetMultiWizard();
        }
        else{
            this._super.apply(this, arguments);
        }
    },

    _isTimesheetGrid(){
        return this.modelName === "account.analytic.line";
    },

    _openTimesheetMultiWizard(){
        var context = this.model.getContext();
        this.trigger_up('execute_action', {
            action_data: {
                name: "get_wizard_open_action",
                type: "object",
            },
            env: {
                model: "timesheet.multi.wizard",
                resIDs: [],
                context,
            },
            on_closed: this._onTimesheetMultiWizardClose.bind(this),
        });
    },

    _onTimesheetMultiWizardClose(){
        this.reload();
    }
});

});
