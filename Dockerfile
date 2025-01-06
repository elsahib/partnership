FROM odoo:18.0

USER root

# Install JWT library

RUN apt-get update && apt-get install -y  python3-jwt 

RUN pip install pyjwt

# Create volumes for data, config, and addons
VOLUME ["/var/lib/odoo", "/etc/odoo", "/mnt/extra-addons"]

# Copy local config and addons to container volumes
COPY config /etc/odoo
COPY addons /mnt/extra-addons

# Expose port 8069
EXPOSE 8069


USER odoo

# Run Odoo
CMD ["-c", "/etc/odoo/odoo.conf"]



