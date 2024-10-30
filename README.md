# AI Blog Generator

This project is an AI-powered blog generator that converts YouTube video content into blog posts. It consists of a backend built with Django and a frontend using HTML and Tailwind CSS.

## Project Structure

```
.gitignore
.vscode/
    ai_blog_app/
        blog_generator/
        manage.py
        static/
        all-blogs.html
    index.html
    signup.html
    bin/
    include/
    lib64
    share/
```

## Prerequisites

- Python 3.8+
- Node.js (for frontend development)
- Virtualenv (optional but recommended)

## Setup Instructions

### Backend Setup

1. **Clone the repository:**

   ```sh
   git clone <repository-url>
   cd <repository-directory>/backend/ai_blog_app
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required Python packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```sh
   python manage.py migrate
   ```

5. **Create a superuser:**

   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```sh
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```sh
   cd <repository-directory>/frontend
   ```

2. **Install Tailwind CSS:**

   ```sh
   npm install -D tailwindcss
   ```

3. **Create a Tailwind configuration file:**

   ```sh
   npx tailwindcss init
   ```

4. **Add Tailwind to your CSS:**

   ```css
   /* In your CSS file */
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

5. **Build your CSS:**

   ```sh
   npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch
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
