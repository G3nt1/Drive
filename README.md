Based on the provided code, it appears to be a Django application for managing folders and files with user authentication. The application allows users to create folders, upload files to those folders, mark items as important, delete items, and share folders and files with other users.

Here's a README template that you can use for GitHub:

# Django File Management App

This is a Django-based web application for managing folders and files with user authentication. Users can organize their files in folders, upload files to those folders, mark files and folders as important, and share them with other users.

## Features

- User authentication and registration system.
- Users can create folders and upload files to those folders.
- Users can mark folders and files as important.
- Folders can be shared with other users, and access permissions can be managed.
- Trashed items can be restored or permanently deleted.
- Users can search for specific files or folders.
- Customizable view mode and theme mode based on user preferences.

## Installation

To install and run the application, follow these steps:

1. Clone the repository to your local machine:

```
git clone https://github.com/your_username/django-file-management-app.git
```

2. Navigate to the project directory:

```
cd django-file-management-app
```

3. Set up a virtual environment (optional but recommended):

```
python -m venv venv
```

4. Activate the virtual environment:

- For Windows:

```
venv\Scripts\activate
```

- For macOS and Linux:

```
source venv/bin/activate
```

5. Install the required dependencies:

```
pip install -r requirements.txt
```

6. Run database migrations:

```
python manage.py migrate
```

7. Create a superuser account to access the Django admin interface:

```
python manage.py createsuperuser
```

8. Start the development server:

```
python manage.py runserver
```

9. Access the application in your web browser at `http://localhost:8000/`.

## Usage

- After running the application, you can access the home page at `http://localhost:8000/`.
- Log in with your superuser account or create a new account.
- Create folders and upload files to organize your data.
- Mark folders or files as important by clicking on the corresponding button.
- Share folders with other users by navigating to the "Share" section.
- Use the search functionality to find specific files or folders.
- Customize your view mode and theme mode in the user preferences section.

## Contributing

Contributions are welcome! If you find any issues or have ideas to improve the application, please open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Special thanks to the Django community and the developers of various libraries used in this project.

## Contact

If you have any questions or need further assistance, feel free to contact the project maintainers:

- Maintainer: [Gentjan Mateli](mateli.gentjan@gmail.com)
- Project Link: https://github.com/G3nt1

---

Please note that you should replace "your_username" with your actual GitHub username, and make sure to update the "Contact" section with appropriate information.

Remember to provide clear and concise instructions so that other developers can easily set up and use your application. Additionally,
including relevant sections like "Features" and "Usage" helps users understand what the application does and how they can interact with it.
