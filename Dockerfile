FROM odoo:18.0

# Install JWT library
RUN pip install --user pyjwt

# Create volumes for data, config, and addons
VOLUME ["/var/lib/odoo", "/etc/odoo", "/mnt/extra-addons"]

# Copy local config and addons to container volumes
COPY config /etc/odoo
COPY myaddons /mnt/extra-addons

# Expose port 8069
EXPOSE 8069

# Link to a database container (replace "db" with your actual database container name)
# Note: Linking is deprecated in newer Docker versions. Consider using Docker Compose for better network management.
# LINK db:db 

# Run Odoo
CMD ["-c", "/etc/odoo/odoo.conf"]