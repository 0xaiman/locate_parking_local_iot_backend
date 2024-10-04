

# Local Backend (Flask)

This project is a prototype Flask application that connects to a database and sets up API routes for use. The application is designed to run locally and integrated with IoT systems and communicate with AWS backend

## Requirements

The application has the following dependencies, which are included in the `requirements.txt`:

- `blinker==1.8.2`
- `click==8.1.7`
- `colorama==0.4.6`
- `Flask==3.0.3`
- `itsdangerous==2.2.0`
- `Jinja2==3.1.4`
- `MarkupSafe==2.1.5`
- `mysql==0.0.3`
- `mysql-connector-python==9.0.0`
- `mysqlclient==2.2.4`
- `pillow==10.4.0`
- `psycopg2==2.9.9`
- `Werkzeug==3.0.4`

To install these dependencies, you can use the following command:

```bash
pip install -r requirements.txt
```

## Application Structure

The main components of the application include:

- `app.py`: The main script to start the Flask application.
- `config/db_connect.py`: Responsible for creating a database connection.
- `routes/routes.py`: Contains the route setup logic for the application.

### Running the Application

To start the server, run the following command:

```bash
python app.py
```

This will start the Flask server on `http://0.0.0.0:5000` with `debug` mode enabled.

### Code Overview

- **Flask Application Initialization**: 
  ```python
  app = Flask(__name__)
  ```
  This initializes the Flask application.

- **Database Connection**:
  ```python
  create_connection()
  ```
  This calls the `create_connection()` function to set up the database connection.

- **Setting Up Routes**:
  ```python
  setup_routes(app)
  ```
  This sets up the routes for the application using the `setup_routes()` function.

- **Running the Application**:
  ```python
  if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000, debug=True)
  ```
  This block ensures that the server runs on the specified host (`0.0.0.0`) and port (`5000`) when the script is executed directly.

## Usage

Once the application is running, you can interact with the defined API routes to perform various operations. Make sure to configure the routes in `routes/routes.py` and set up the appropriate database connections in `config/db_connect.py` for successful operation.
