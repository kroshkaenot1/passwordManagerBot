ARG TARGETARCH
FROM ${TARGETARCH}/python:3.8-slim-buster



COPY . /app
RUN pip install -r /app/requirements.txt
WORKDIR /app

ENV MYSQL_HOST=db
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root
ENV MYSQL_DATABASE=password_manager_base

ENV PMBTOKEN=6081656901:AAFhUzEE_gjEeW1Xe2AnGYAIZ_wuSE7N8og
ENV DELAY_FOR_DELETE=60

CMD ["python","main.py"]