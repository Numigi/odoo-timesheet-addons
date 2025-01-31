FROM quay.io/numigi/odoo-public:16.latest
LABEL maintainer="contact@numigi.com"

USER root

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY hr_timesheet_project_parent_enhanced  /mnt/extra-addons/hr_timesheet_project_parent_enhanced
COPY project_timesheet_time_control_sheet  /mnt/extra-addons/project_timesheet_time_control_sheet
COPY timesheet_holidays_time_control_compatible /mnt/extra-addons/timesheet_holidays_time_control_compatible
COPY timesheet_task_project_no_change  /mnt/extra-addons/timesheet_task_project_no_change 

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
