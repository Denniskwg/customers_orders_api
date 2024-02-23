# Customers_orders_api
A simple customer order management api for maintaining customers and related orders. Users have to register in order to use the service. After registering, users can access the endpoint for creating customers and creating orders which are protected using oidc. After adding an order relating to a customer a confirmation message is sent to the customer.
**To set up the application locally, open a terminal and run the following commands:**
- start postgres server
- **pip install -r requirements.txt**
- Add database credentials to the environment in the format:
        - **db_username**=your username
        - **db_password**=your password
- configure environment variables:
        - export CLIENT_ID=029577
        - export CLIENT_SECRET=326fdc504ed9981aee7ede2a8ba444a11e1b2f82140925f02e120dfd
- Create postgres database. run **create_database.sh** file.
- run python3 manage.py migrate
- run python3 manage.py creatersakey
- take note of kid printed from above command and add it to the environment variables in the format **export OIDC_KEY_IDENTIFIER=<kid>**
- Create admin user. **python3 manage.py createsuperuser**. Enter username as **dennis_admin** and password **dennis2000**
- Create oidc client. **python3 manage.py shell < create_oidc_client.py**
