# AI Blog Generator

This project is an AI-powered blog generator that converts YouTube video content into blog posts. It consists of a backend built with Django and a frontend using HTML and Tailwind CSS.

## Project Structure

```
.gitignore
.vscode/
    settings.json
backend/
    ai_blog_app/
        ai_blog_app/
        blog_generator/
        db.sqlite3
        manage.py
        media/
        static/
        templates/
notes.txt
frontend/
    all-blogs.html
    blog-details.html
    index.html
    login.html
    signup.html
    style.css
venv/
    bin/
    etc/
    include/
    lib/
    lib64
    pyvenv.cfg
    share/
```

## Prerequisites

- Python 3.8+
- Virtualenv (optional but recommended)

## Setup Instructions

### Backend Setup

1. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install the required Python packages:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Apply database migrations:**

   ```sh
   python manage.py migrate
   ```

4. **Create a superuser:**

   ```sh
   python manage.py createsuperuser
   ```

5. **Run the development server:**

   ```sh
   python manage.py runserver
   ```

## Project Details

### Backend

- **URL Configuration:** The URL configuration is defined in [`urls.py`](backend/ai_blog_app/ai_blog_app/urls.py).
- **Views:** The views for handling user signup, login, and blog generation are defined in [`views.py`](backend/ai_blog_app/blog_generator/views.py).
- **Models:** The `BlogPost` model is defined in the initial migration file [`0001_initial.py`](backend/ai_blog_app/blog_generator/migrations/0001_initial.py).

### Frontend

- **HTML Templates:** The HTML templates are located in the `templates` directory.
- **CSS:** The styling is done using Tailwind CSS, and the main stylesheet is [`style.css`](frontend/style.css).

### Running the Application

1. **Start the backend server:**

   ```sh
   cd backend/ai_blog_app
   source venv/bin/activate  # Activate the virtual environment
   python manage.py runserver
   ```

2. **Open the frontend in a browser:**

   Navigate to [`http://127.0.0.1:8000`](http://127.0.0.1:8000) to access the application.

## Notes

- The `.gitignore` file is configured to ignore the `venv` and `.vscode` directories.
- The `notes.txt` file contains additional information about the project.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---

This README provides a comprehensive guide to setting up and running the AI Blog Generator project. If you have any questions or need further assistance, please refer to the documentation or open an issue on GitHub.
