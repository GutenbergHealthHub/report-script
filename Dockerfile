FROM python:3.8

COPY report_script.py /script/
COPY requirements.txt /script/
COPY app.py .

COPY report-script-cron /etc/cron.d/report-script-cron

RUN apt-get update && apt-get install -y \
    cron \
    postgresql \
    nano \
    && pip install -r /script/requirements.txt

RUN chmod 0644 /etc/cron.d/report-script-cron && \
    crontab /etc/cron.d/report-script-cron && \
    chgrp -R 0 /script && \
    chmod -R g=u /script && \
    chmod -R 777 /run 


CMD ["/bin/bash", "-c", "--", "while true; do sleep 30; done;" ]