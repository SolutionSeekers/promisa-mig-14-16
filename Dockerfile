FROM odoo:16.0
MAINTAINER Mirsha Rey <mrc@juarez.technology>

COPY --chown=odoo ./extra-addons /var/lib/extra-addons
COPY ./odoo.conf /etc/odoo/

USER root
WORKDIR /
RUN apt-get upgrade
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    python3-dev
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip3 install xmltodict
RUN pip3 install py3o.template
RUN pip3 install py3o.formats
USER odoo