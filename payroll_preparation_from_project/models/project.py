# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class Project(models.Model):

    _inherit = 'project.project'

    def open_payroll_preparation_wizard(self):
        pass
