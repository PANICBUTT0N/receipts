FROM python:3

COPY ./server/ /usr/app/server/
WORKDIR /usr/app/server
RUN pip install --no-cache-dir -r /usr/app/server/requirements.txt
EXPOSE 5000
ENTRYPOINT ["flask", "run"]