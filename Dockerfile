FROM continuumio/miniconda3

WORKDIR /app
COPY . .
RUN apt update && apt install -y cron
RUN pip install pipenv && pipenv install --system
RUN crontab cron_job

ENTRYPOINT ["/bin/bash"]
CMD ["run.sh"]
