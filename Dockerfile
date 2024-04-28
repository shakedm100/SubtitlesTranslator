FROM python:3.9-alpine

# Set up working directory and copy your application
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set up cron jobs
# Echo new cron file
RUN echo -e "*/1 * * * * cd /app && python Main.py >> /var/log/cron.log 2>&1\n" > /etc/crontabs/root
RUN touch /var/log/cron.log

# Exposing port 5000 to run the WebUI
EXPOSE 5000

# Start the cron daemon in the foreground
CMD ["crond", "-f", "-d", "8", "-L", "/dev/stdout"]
