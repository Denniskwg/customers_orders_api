# Customers_orders_api
A simple customer order management api for maintaining customers and related orders. Users have to register in order to use the service. After registering, users can access the endpoint for creating customers and creating orders which are protected using oidc. After adding an order relating to a customer a confirmation message is sent to the customer.
**To set up the application locally, open a terminal and run the following commands:**
- start docker daemon
- run docker compose up --build
- in another terminal, run docker exec -it customers-orders-app python3 manage.py creatersakey
- take note of kid printed from above command and add it to the docker_compose file in the web service environment as the value for OIDC_KEY_IDENTIFIER
- create admin user for the app using docker exec -it customers-orders-app python3 manage.py createsuperuser
- create oidc client for the app using docker exec -it customers-orders-app python3 manage.py shell < create_oidc_client.py
- close the session started by docker compose and start it again.
- Access the app at http://127.0.0.1:8000
