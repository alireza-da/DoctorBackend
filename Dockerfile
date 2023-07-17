FROM python:3.9


RUN mkdir /DcBackend
WORKDIR /DcBackend
RUN pip install --upgrade pip
COPY requirements.txt /DcBackend/

RUN pip install -r requirements.txt
COPY . /DcBackend/

EXPOSE 8000

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]