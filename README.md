# RANKER 🏓

### Table Tennis (aka Ping Pong) Rankings and Stats for Offices or Local Leagues

Add players, events and match results. Ratings and leaderboard are updated automatically.

Hobby project, made with Django + DRF, VueJS (Vuex, Vue Rouer, Vuetify).

![](https://i.imgur.com/27WAjwE.png)

![](https://i.imgur.com/f0TBJI5.png)

#### Demo

Live demo [here](https://ttranker.herokuapp.com/)

#### Localization

App is available in two languages: English and Russian.

#### Tech Notes

* Ranker uses Postgresql as database engine. All necessary migration files are included.

* (provided for portability) Django i18n compiled file `.mo` is included in the repo. Dont forget to recompile it with `$ ./manage.py compilemessages` if updating translations. `gettext` utility is needed for this (`sudo apt install gettext`).

##### Local installation steps:

1. Install Python 3.9
2. Create virtual environment and install packages with `$ pip install -r requirements.txt`
3. Install node.js and then packages with `$ npm install`
4. Build assets with `$ npm run build`
5. Create Postgresql database, change database name and user/password in [settings](/ranker/settings/dev.py) if needed. Default value for database, user and password is `ranker`
6. Migrate the database:

```
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py createcachetable  # caching is enabled for leaderboard
$ ./manage.py createdemo  # to load demo data
```

7. Use `$ ./manage.py runserver` or deploy with 3rd party web server
8. Use superuser account at `/admin` to manage the database content and to save new match results.

##### Heroku deployment:

1. Sign up for free Heroku account and install Heroku CLI
2. Shell commands:

```
$ heroku apps:create your_app_name
$ heroku git:remote --app your_app_name
$ heroku buildpacks:add --index 1 heroku/nodejs
$ heroku buildpacks:add --index 2 heroku/python
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set DJANGO_SETTINGS_MODULE=ranker.settings.prod
$ heroku config:set RANKER_SECRET_KEY='production SECRET_KEY value'

# superuser section, set values as needed
$ heroku config:set DJANGO_SUPERUSER_USERNAME=admin
$ heroku config:set DJANGO_SUPERUSER_PASSWORD=admin
$ heroku config:set DJANGO_SUPERUSER_EMAIL=admin@admin.admin

$ git push heroku
```

3. Use `$ heroku open` to reach the application.

**Big thanks** to [gtalarico/django-vue-template](https://github.com/gtalarico/django-vue-template) for settings template and perfect instructions.

#### Creating Demo Data

If you need some fake data for demonstration or development purposes you can create it with `$ ./manage.py createdemo`. Some basic parameters for fake data can be altered [here](/ranker/core/management/commands/createdemo.py)

Please create an issue or [email me](mailto:funkindy@gmail.com) if you have any questions.
