# Olive Guide
An app for farmers to help them manage their olive groves.They can create/edit/delete their olive groves.View the weather for each olive grove,add/edit/delete notes for each olive grove.

## Tech

Olive Guide uses a number of open source projects to work properly:

- [Django] - Python Framework
- [Matrializecss] - great UI boilerplate for modern web apps
- [PostgreSQL-Postgis] - Database
- [OpenWeatherApi] - API for taking weather information

Usefull Libraries :
- [django-leaflet] - Tool for awesome maps
- [django-allauth] - Authentication library for django


## Installation and run
To run the app locally you have to own a postgres database.ALso you need to copy the .env.example variables to .env file and add your own credentials for OpenWeather API key and email configuration.

```sh
pip install -r requirements
cd olive_guide
python manage.py migrate
python manage.py runserver
```
Or with docker-compose 
```sh
docker-compose up --build
```
