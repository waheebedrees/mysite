# MySite

Welcome to **MySite**, a personal blog project built with Django! This repository contains the full source code for a modern, responsive blog, leveraging HTML, Python (Django), and JavaScript.

## Features

- 📝 Create, edit, and publish blog posts easily
- 🎨 Responsive design using HTML and tailwindcss templates (works on all devices)
- 🔎 Fast navigation & basic search functionality
- 💬 Optional commenting or feedback system
- 🔒 Simple authentication for admin/author (Django’s built-in user system)
- ⚡ Lightweight and easy to deploy

## Tech Stack

- **Python** (Django): Backend, routing, ORM, admin interface
- **HTML and Tailwindcss**: Page structure and templates components 
- **JavaScript**: Interactivity and UI enhancements

## Getting Started

### Prerequisites

- Python 3.x
- `pip` (Python package manager)
- (Optional) Virtual environment tool: `venv` or `virtualenv`

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/waheebedrees/mysite.git
    cd mysite
    ```

2. **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(If requirements.txt is missing, manually install Django: `pip install django`)*

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the site:**
    - Blog: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Customization

- Edit Django templates in the `templates/` directory for layout and design changes.
- Static files (CSS, JS, images) are in the `static/` directory.
- Modify backend logic in the app’s Python files to add features or change behavior.

## Deployment

- Configure `ALLOWED_HOSTS` and static/media settings in `settings.py` for production.
- Use services like Heroku, Vercel, or traditional VPS hosting for deployment.
- Consider using Gunicorn + Nginx for robust production deployments.

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests for any improvements or new features.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

- [waheebedrees](https://github.com/waheebedrees)

---

*Happy blogging with Django! 🚀*
