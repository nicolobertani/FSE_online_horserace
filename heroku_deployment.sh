#!/bin/bash

# bash otree_setup.sh

# heroku create
# heroku addons:create heroku-postgresql:essential-0
# heroku config:set OTREE_PRODUCTION=1
# heroku config:set OTREE_AUTH_LEVEL='STUDY' 
# heroku config:set OTREE_ADMIN_PASSWORD='I_am_the_admin'

git push heroku master
sleep 20
heroku pg
