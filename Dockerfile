
FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false
RUN apt-get update \
&& apt-get -y install libpq-dev gcc \
&& pip install psycopg2
WORKDIR /diarias
COPY . .
RUN pip install --upgrade setuptools
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/diarias/core"
EXPOSE 8000
CMD ["python", "main.py"]