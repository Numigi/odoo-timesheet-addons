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
COPY timesheet_project_change_analytic_account  /mnt/extra-addons/timesheet_project_change_analytic_account

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
