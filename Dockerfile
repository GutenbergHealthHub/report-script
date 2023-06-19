FROM python:3.8

COPY report_script.py .
COPY requirements.txt .

RUN yum update && yum install -y \
    @postgresql \
    && pip install -r ./requirements.txt

CMD ["/bin/bash", "-c", "--", "while true; do sleep 30; done;" ]