#!/usr/bin/env bash
#creates a postgres database
username="$db_username"

createdb -U "$username" customers_orders_db

if [ $? -eq 0 ]; then
	    echo "Database creation successful."
    else
	        echo "Database creation failed."
fi
