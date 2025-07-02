# Quiz Management System (QMS)

A web-based Quiz Management System built with Django (backend) and React (frontend). This platform allows faculty to create quizzes and students to participate in them, with secure authentication and a modern UI.

## Features
- User authentication (students & faculty)
- Faculty: Create, manage, and review quizzes
- Students: Take quizzes and view results
- RESTful API (Django REST Framework)
- JWT-based authentication
- Modern React frontend

## Project Structure
```
qms-anvi/
├── anvi/                # Python virtual environment
├── config/              # Django project settings
├── manage.py            # Django management script
├── quiz/                # Django app for quiz logic
├── quiz-frontend/       # React frontend app
```

## Backend Setup (Django)
1. **Install dependencies** (inside virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
3. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```
4. **Run the backend server:**
   ```bash
   python manage.py runserver
   ```

## Frontend Setup (React)
1. Navigate to the frontend directory:
   ```bash
   cd quiz-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```

## How to Run (Development)
- Start the Django backend server (see above)
- Start the React frontend server (see above)
- Access the app at [http://localhost:3000](http://localhost:3000)

## API
- The backend exposes a RESTful API at [http://localhost:8000](http://localhost:8000)
- Authentication uses JWT (SimpleJWT + Djoser)

## License
This project is for educational purposes. 