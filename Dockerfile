FROM llacox/odoo:14.0
MAINTAINER Aztlan Munoz <amr@indboo.com>

COPY --chown=odoo ./extra-addons /var/lib/extra-addons
COPY ./odoo.conf /etc/odoo/

USER root
WORKDIR /
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    python3-dev
RUN pip3 install xmltodict
USER odoo