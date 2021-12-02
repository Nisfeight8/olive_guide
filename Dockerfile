FROM python:3.9.2-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1


WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get -y install netcat gcc postgresql  binutils libproj-dev gdal-bin python-gdal python3-gdal \
    && apt-get clean


# set user:group
RUN groupadd appuser && useradd -g users -G appuser appuser  --home /usr/src/app

# change permission on workdir
RUN chown -R appuser:appuser /usr/src/app


USER appuser:appuser
ENV PATH=$PATH:/usr/src/app/.local/bin

# install dependencies
RUN pip install --upgrade pip
COPY --chown=appuser:appuser requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=appuser:appuser olive_guide .

RUN  python manage.py collectstatic --noinput


# TODO: superuser, migrations
WORKDIR /usr/src/app

#EXPOSE 8000/tcp
#ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000","olive_guide.wsgi"]
CMD gunicorn olive_guide.wsgi:application --bind 0.0.0.0:8000
