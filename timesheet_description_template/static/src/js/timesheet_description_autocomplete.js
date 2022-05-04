/*
    © 2022 - today Numigi <https://www.numigi.com>
    License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL.html).
*/
odoo.define("timesheet_description_autocomplete", function (require) {
"use strict";

var AbstractField = require("web.AbstractField");
var FieldChar = require("web.basic_fields").FieldChar;
var registry = require("web.field_registry");
var rpc = require("web.rpc");

var AutocompleteWidget = FieldChar.extend({
    _prepareInput: function () {
        const $input = this._super.apply(this, arguments);
        $input.autocomplete({
            source: async (request, response) => {
                const descriptions = await searchDescriptions(request.term)
                response(descriptions)
            },
        });
        return $input
    },
});

async function searchDescriptions(term) {
    return await rpc.query({
        model: "timesheet.description.template",
        method: "get_suggestions",
        args:[term],
    })
}

registry.add("timesheet_description_autocomplete", AutocompleteWidget);

});
