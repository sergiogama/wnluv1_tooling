# --- Base Image
# FROM us.icr.io/ibmdegla-cr-namespace/alpine-python374-bokeh:latest
FROM vmpereiraf/flaskbase:latest

# Install requirements
RUN pip install Flask-Mobility numpy

# Clean
RUN rm -rf ~/.cache/pip

# Set working directory
WORKDIR /usr/src/app

# Add flask server files
COPY . /usr/src/app/

# Set entrypoint.sh permissions
RUN chmod +x /usr/src/app/entrypoint.sh

# Run server
CMD ["/usr/src/app/entrypoint.sh"]
