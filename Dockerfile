FROM python:3.7


RUN apt-get update && apt-get install -y imagemagick


WORKDIR /usr/src/app

COPY . .

RUN sh setup.sh

ENV FLASK_APP app
ENV FLASK_ENV development

EXPOSE 5000

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "sh", "run.prod.sh"]