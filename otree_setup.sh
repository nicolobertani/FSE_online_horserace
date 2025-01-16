#!/bin/bash

# hides debug info
OTREE_PRODUCTION=1
export OTREE_PRODUCTION

OTREE_AUTH_LEVEL='STUDY' # visitors to only be able to play your app if you provided them with a start link
# OTREE_AUTH_LEVEL = 'DEMO' # anybody can play a demo version of your game (but not access the full admin interface)
export OTREE_AUTH_LEVEL

OTREE_ADMIN_PASSWORD='I_am_the_admin' # admin password
export OTREE_ADMIN_PASSWORD