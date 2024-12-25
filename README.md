
# CS5356 Project

## Requirements
To install the required dependencies, use the following command:

```bash
pip install django
```

## How to Run the Program
1. Open a terminal in the project folder.
2. Start the Django development server with:

   ```bash
   python manage.py runserver
   ```

## Checking the Inbuilt Django Database
To interact with the database, you can use Django's shell. Follow these steps:

1. Run migrations (if not already done):

   ```bash
   python manage.py migrate
   ```

2. Open the Django shell:

   ```bash
   python manage.py shell
   ```

3. Sample command to retrieve all student entries:

   ```python
   from home.models import Student
   Student.objects.all().values()
   ```

4. Exit the shell:

   ```bash
   exit()
   ```

## Available Pages
- **Login Page**: `/login`
- **Home Page**: `/index`
- **Student Registration**: `/student_register`
- **Company Registration**: `/company_register`
- **Password Reset**: `/password_reset`
- Other pages vary depending on the user type.

---

## Additional Information
If you wish to explore the different functionalities of the webpage, refer to the `populateDB.txt` file. This file contains all the queries used to populate the current project. Each of these users and postings is available for testing.
