# RANKER 🏓

### Table Tennis (aka Ping Pong) Rankings and Stats for Offices or Local Leagues

Add players, events and match results. Ratings and leaderboard are updated automatically.

Hobby project, made with Django + DRF, VueJS + Vue Rouer + Vuetify.

![](https://i.imgur.com/27WAjwE.png)

![](https://i.imgur.com/f0TBJI5.png)

#### Demo

Live demo [here](https://ttranker.herokuapp.com/)

#### Localization

App is available in two languages: English and Russian.

#### Quickstart:

1. (weird) Ranker repo includes sqlite3 database with demo data for maximum portability. All database migrations are already made. Default superuser is `admin` with password `admin`.
2. To clean up the demo data use `./manage.py flush`. To completely remigrate the database:

```
$ rm db.sqlite3
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py createcachetable  # leaderbord is cached
$ ./manage.py createdemo  # to restore demo data
```

3. Use superuser account at `/admin` to manage the database content and to save new match results.

_TODO:_ Postgresql migration.

##### Local installation steps:

1. Install Python 3.7
2. Create virtual environment and install packages with `$ pip install -r requirements.txt`
3. Install node.js
4. Build assets with `$ npm run build`
5. Use `$ ./manage.py runserver` or deploy with 3rd party web server

##### Heroku deployment:

1. Sign up for free Heroku account and install Heroku CLI
2. Shell commands:

```
$ heroku apps:create your_app_name
$ heroku git:remote --app your_app_name
$ heroku buildpacks:add --index 1 heroku/nodejs
$ heroku buildpacks:add --index 2 heroku/python
$ heroku config:set DJANGO_SETTINGS_MODULE=ranker.settings.prod
$ heroku config:set DJANGO_SECRET_KEY='production SECRET_KEY value'

$ git push heroku
```
3. Use `$ heroku open` to reach the application.

**Big thanks** to [gtalarico/django-vue-template](https://github.com/gtalarico/django-vue-template) for settings template and perfect instructions.

#### Creating Demo Data

If you need some fake data for demonstration or development purposes you can create it with `$ ./manage.py createdemo`. Some basic parameters for fake data can be altered [here](/ranker/core/management/commands/createdemo.py)

Please create an issue or [email me](mailto:funkindy@gmail.com) if you have any questions.
