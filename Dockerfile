FROM quay.io/numigi/odoo-public:12.0
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

COPY payroll_period /mnt/extra-addons/payroll_period
COPY payroll_preparation /mnt/extra-addons/payroll_preparation
COPY timesheet_list_description_after_task /mnt/extra-addons/timesheet_list_description_after_task
COPY timesheet_list_employee /mnt/extra-addons/timesheet_list_employee
COPY timesheet_multi_line_wizard /mnt/extra-addons/timesheet_multi_line_wizard
COPY timesheet_multi_line_wizard_grid /mnt/extra-addons/timesheet_multi_line_wizard_grid
COPY timesheet_payroll_period /mnt/extra-addons/timesheet_payroll_period
COPY timesheet_validation_status /mnt/extra-addons/timesheet_validation_status
COPY timesheet_validation_status_enterprise /mnt/extra-addons/timesheet_validation_status_enterprise

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
