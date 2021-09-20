FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

COPY .docker_files/test-requirements.txt .
RUN pip3 install -r test-requirements.txt

ARG GIT_TOKEN

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY payroll_code_on_task_type /mnt/extra-addons/payroll_code_on_task_type
COPY payroll_period /mnt/extra-addons/payroll_period
COPY payroll_preparation /mnt/extra-addons/payroll_preparation
COPY payroll_preparation_export_wizard /mnt/extra-addons/payroll_preparation_export_wizard
COPY payroll_preparation_from_project /mnt/extra-addons/payroll_preparation_from_project
COPY payroll_preparation_from_timesheet /mnt/extra-addons/payroll_preparation_from_timesheet
COPY payroll_preparation_prorata /mnt/extra-addons/payroll_preparation_prorata
COPY project_timesheet_time_control_enhanced /mnt/extra-addons/project_timesheet_time_control_enhanced
COPY timesheet_edit_only_today /mnt/extra-addons/timesheet_edit_only_today
COPY timesheet_edit_only_today_grid /mnt/extra-addons/timesheet_edit_only_today_grid
COPY timesheet_list_description_after_task /mnt/extra-addons/timesheet_list_description_after_task
COPY timesheet_list_employee /mnt/extra-addons/timesheet_list_employee
COPY timesheet_multi_line_wizard /mnt/extra-addons/timesheet_multi_line_wizard
COPY timesheet_multi_line_wizard_grid /mnt/extra-addons/timesheet_multi_line_wizard_grid
COPY timesheet_multi_line_wizard_security /mnt/extra-addons/timesheet_multi_line_wizard_security
COPY timesheet_payroll_period /mnt/extra-addons/timesheet_payroll_period
COPY timesheet_validation_status /mnt/extra-addons/timesheet_validation_status
COPY timesheet_validation_status_enterprise /mnt/extra-addons/timesheet_validation_status_enterprise

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
