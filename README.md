# Daystar University Events and Activities Backend

This repository contains the backend for the Daystar University's Orientation application. The application allows users to view events, activities, and FAQs, and also allows administrators to manage these resources.

## Installation

0. Clone the repository:
    ```bash
    git clone https://github.com/your-username/Orientation-App-backend.git
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

- **Django Admin:** Access the admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/).
- **View Orientation:** Access the orientation list at [http://localhost:8000/api/orientation/](http://localhost:8000/api/orientation/).
- **Edit a Orientation period:** Edit Orientation use PUT method [http://localhost:8000/api/orientation/<int:id>/](http://localhost:8000/api/orientation/<int:id>/).
- **Delete a Oreintation period:** Delete a Orientation use DELETE method [http://localhost:8000/api/orientation/<int:id>/](http://localhost:8000/api/orientation/<int:id>/).
- **View Events:** Access the events list at [http://localhost:8000/api/events/](http://localhost:8000/api/events/).
- **Edit an event:** Edit an event use PUT method [http://localhost:8000/api/events/<int:id>/](http://localhost:8000/api/events/<int:id>/).
- **Delete an event:** Delete an event use DELETE method [http://localhost:8000/api/events/<int:id>/](http://localhost:8000/api/events/<int:id>/).
- **View Activities:** Access the activities list at [http://localhost:8000/api/activities/](http://localhost:8000/api/activities/).
- **Edit an activity:** Edit an activity use PUT method [http://localhost:8000/api/activities/<int:id>/](http://localhost:8000/api/activities/<int:id>/).
- **Delete an activity:** Delete an activity use DELETE method [http://localhost:8000/api/activities/<int:id>/](http://localhost:8000/api/activities/<int:id>/).
- **View FAQs:** Access the FAQs list at [http://localhost:8000/api/faqs/](http://localhost:8000/api/faqs/).
- **Edit a FAQ:** Edit a FAQ use PUT method [http://localhost:8000/api/faqs/<int:id>/](http://localhost:8000/api/faqs/<int:id>/).
- **Delete a FAQ:** Delete a FAQ use DELETE method [http://localhost:8000/api/faqs/<int:id>/](http://localhost:8000/api/faqs/<int:id>/).
- **Add Orientation:** Use the POST method at [http://localhost:8000/api/orientation/](http://localhost:8000/api/orientation/) to add new oreintation period.
- **Add Events:** Use the POST method at [http://localhost:8000/api/events/](http://localhost:8000/api/events/) to add new event.
- **Add Activities:** Use the POST method at [http://localhost:8000/api/activities/](http://localhost:8000/api/activities/) to add new activities.
- **Add FAQs:** Use the POST method at [http://localhost:8000/api/faqs/](http://localhost:8000/api/faqs/) to add new FAQs.
- **Register Users:** Use the POST method at [http://localhost:8000/api/accounts/](http://localhost:8000/api/accounts/) to register new users.
- **Edit a user:** Edit a User use the PUT method [http://localhost:8000/api/accounts/<int:id>/](http://localhost:8000/api/accounts/<int:id>/).
- **Delete a user:** Delete a user use DELETE method [http://localhost:8000/api/accounts/<int:id>/](http://localhost:8000/api/accounts/<int:id>/).
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
