# Shop app

This is a learning app for shop.

## Technologies

-   Backend
    -   Django
    -   Django REST framework
-   Frontend
    -   React TypeScript
    -   TailwindCSS
    -   [Vite](https://vitejs.dev/)

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/simonfabcic/32_-_NestJS_-_ReactJS-app
    ```

### Backend

1. Go into backend directory:
    ```
    cd .\32_-_NestJS_-_ReactJS-app\backend\
    ```
1. Prepare virtual environment (Python 3.12 required):
    - Install `pipenv`:
        ```
        pip install pipenv
        ```
    - Create virtual environment and install dependencies from `Pipfile.lock`:
        ```
        pipenv install -d
        ```
    - To activate this project's virtualenv, run:
        ```
        pipenv shell
        ```
1. Applies migrations to your database:
    ```
    python manage.py migrate
    ```
1. [Optional]
    - To create super user run command and follow the prompts:
        ```
        python manage.py createsuperuser
        ```
    - seed data to DB:
        ```
        python seed.py
        ```
1. Run server in development mode on port 8456
    ```
    python manage.py runserver 8456
    ```

### Frontend

1. Go into frontend directory:
    ```
    cd .\32_-_NestJS_-_ReactJS-app\frontend\
    ```
1. Install packages with npm:
    ```
    npm install
    ```
1. Run dev environment:
    ```
    npm run dev
    ```

## Tests

### Backend

1. Go into backend directory:
    ```
    cd .\32_-_NestJS_-_ReactJS-app\backend\
    ```
1. And run:
    ```
    python manage.py test
    ```

### Frontend

1. Go into frontend directory:
    ```
    cd .\32_-_NestJS_-_ReactJS-app\frontend\
    ```
1. And run:
    ```
    npm run test
    ```
