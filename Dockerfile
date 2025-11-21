FROM quay.io/numigi/odoo-public:14.latest
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


COPY project_timesheet_time_control_enhanced /mnt/extra-addons/project_timesheet_time_control_enhanced
COPY project_timesheet_time_control_sheet /mnt/extra-addons/project_timesheet_time_control_sheet
COPY timesheet_description_template /mnt/extra-addons/timesheet_description_template
COPY timesheet_holidays_time_control_compatible /mnt/extra-addons/timesheet_holidays_time_control_compatible
COPY timesheet_project_task_validation /mnt/extra-addons/timesheet_project_task_validation
COPY timesheet_sheet_confirm_reset /mnt/extra-addons/timesheet_sheet_confirm_reset


COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
