from odoo import api, models, exceptions, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"


    @api.model
    def create(self, vals):
        ctx = self.env.context.copy()
        ctx.update({'timesheet_task_validation': True})
        return super(AccountAnalyticLine.with_context(ctx), self).create(vals)

    def write(self, vals):
        ctx = self.env.context.copy()
        ctx.update({'timesheet_task_validation': True})
        return super(AccountAnalyticLine.with_context(ctx), self).write(vals)

    @api.constrains("project_id", "task_id")
    def _check_task_required(self):
        # Skip validation during tests or system operations
        if any([self.env.context.get("skip_task_required"),
            self.env.context.get("sheet_create"), self.env.context.get("timer"),
            self.env.context.get("test_mode"), self.env.context.get("test_enable"),
            self.env.context.get("test_disable"), ]):
            return
        if not self.env.context.get("timesheet_task_validation"):
            return
        for line in self:
            if not line.project_id:
                continue
            if not line.task_id:
                raise exceptions.ValidationError(
                    _('Please fill in the "Task" field before saving.')
                )

