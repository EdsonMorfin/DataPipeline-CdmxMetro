FROM python:3.8
RUN apt-get update \
  && apt-get install -y postgresql postgresql-contrib
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt
ADD ./app /code/app
ADD ./.env /code/app
EXPOSE 8000
CMD ["python","-u","/code/app/main.py"]

#CMD ["uvicorn", "app.api_metro:app","--reload", "--reload-dir","/code/app/utils"]
