# Daystar University Events and Activities Backend

This repository contains the backend for the Daystar University's Orientation application. The application allows users to view events, activities, and FAQs, and also allows administrators to manage these resources.

## Installation

0. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Orientation-APP-Backend.git
    cd daystar-orientation
    ```

1. Create a virtual environment for collaborative development and isolation of dependancies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the following command to create the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- **View Events:** Access the events list at [http://localhost:8000/api/events/](http://localhost:8000/api/events/).
- **View Activities:** Access the activities list at [http://localhost:8000/api/activities/](http://localhost:8000/api/activities/).
- **View FAQs:** Access the FAQs list at [http://localhost:8000/api/faqs/](http://localhost:8000/api/faqs/).
- **Add Events:** Use the POST method at [http://localhost:8000/api/events/](http://localhost:8000/api/events/) to add new events.
- **Add Activities:** Use the POST method at [http://localhost:8000/api/activities/](http://localhost:8000/api/activities/) to add new activities.
- **Add FAQs:** Use the POST method at [http://localhost:8000/api/faqs/](http://localhost:8000/api/faqs/) to add new FAQs.
- **Register Users:** Use the POST method at [http://localhost:8000/api/users/](http://localhost:8000/api/users/) to register new users.
- **Authenticate Users:** Use the POST method at [http://localhost:8000/api/auth/token/login/](http://localhost:8000/api/auth/token/login/) to authenticate users and obtain a token.

## Contributing

1. Fork this repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push the branch to your fork.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For any issues or contributions, please contact [clivesasaka@gmail.com](mailto:clivesasaka@gmail.com).
