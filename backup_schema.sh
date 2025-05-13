#!/bin/bash

sqlite3 api_sncf.db .dump > db_data.sql
sqlite3 api_sncf.db .schema > db_schema.sql