from odoo import api, models, exceptions, _


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.constrains("project_id", "task_id")
    def _check_task_required(self):
        """
        Enforce: if a project is set → task is required.
        Skip validation for system-created analytic lines:
        - timers
        - hr_timesheet_sheet automatic propagation
        - tests creating minimal AAL
        """
        if self.env.context.get("skip_task_required"):
            return

        for line in self:
            # No project → no task required
            if not line.project_id:
                continue

            # System lines : skip
            if line._context.get("sheet_create") or line._context.get("timer"):
                continue

            # Business rule
            if not line.task_id:
                raise exceptions.ValidationError(
                    _('Please fill in the "Task" field before saving.')
                )
