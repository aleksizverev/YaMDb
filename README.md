# YaMDb 
![YaMDb workflow](https://github.com/aleksizverev/yamdb_final/workflows/yamdb/badge.svg)
REST API for YaMDb service.
A database with reviews on films, books and music.

## Getting Started
*Adapt .env as you need*
The following commands should be made from
project directory.

#### Launching Docker
 ```
 docker-compose up
 ```
#### First Start
Make migrations:
```
docker-compose exec web python manage.py migrate
```
Create a superuser:
```
docker-compose exec web python manage.py createsuperuser
```
Fill up the database with initial sample data
```
docker-compose exec web python manage.py loaddata fixtures.json
```
#### Built with
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [PostgreSQl](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)

#### Authors
* [Alexei Zverev](https://github.com/aleksizverev) - **Content Part**(Categories, Genres, Titles)
* [Mikhail Gaponov](https://github.com/Contrigra/) - **Content Part**(Reviews, Comments)
* [Dmitriy Frolov](https://github.com/fd239) - **Authentication Part**(Auth, Users)
