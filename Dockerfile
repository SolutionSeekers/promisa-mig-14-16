FROM odoo:16.0
MAINTAINER Mirsha Rey <mrc@juarez.technology>

COPY --chown=odoo ./extra-addons /var/lib/extra-addons
COPY ./odoo.conf /etc/odoo/

USER root
WORKDIR /
RUN apt-get upgrade
RUN apt-get update

USER odoo