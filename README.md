# Quiz App

The Quiz Platform API is designed to provide a comprehensive solution for creating and managing
quizzes. It allows users to create quizzes, manage questions and answers, and enable others to
participate in the quizzes. The API offers features such as scoring, timed quizzes etc.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Generating Fake Data](#generating-fake-data)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation

Follow the steps below to install and configure the Quiz App API:

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/rayhanrock/quiz-api.git
   ```

2. Navigate to the project directory:
   ```shell
   cd quiz-api
   ```


3. Create a virtual environment for the project:

   ```shell
   # Create a new virtual environment
   python -m venv myenv
   
   # Activate the virtual environment
   # For Windows:
   myenv\Scripts\activate
   # For macOS/Linux:
   source myenv/bin/activate
   ```

4. Install the required dependencies by navigating to the project directory and running the following command:

   ```shell
   pip install -r requirements.txt
   ```

5. Configure the email settings in the settings.py file:

   ```shell
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = "###"
   EMAIL_HOST_USER = '###'
   EMAIL_HOST_PASSWORD = '###'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_USE_SSL = False
   DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

   #Make sure to replace '###' with your own email credentials.
   ```

6. Apply the database migrations by running the following command:

   ```shell
   python manage.py migrate
   ```

7. Start the development server:

   ```shell
   python manage.py runserver
   ```

Please note that this installation assumes you have Python already set up on your system.

## Usage

To use the Quiz App API, follow the steps below:

1. Register a new user account or log in with an existing account using the provided API endpoints for user
   authentication.

2. Quiz Management:
    - Create quizzes with the required details such as title, description, and time limit.
    - Retrieve quizzes.
    - Update or delete a specific quiz.

3. Question and Answer Management:
    - Create questions for a specific quiz with the question details.
    - Retrieve questions for a specific quiz.
    - Update or delete a specific question.
    - Create answers for a specific question with the answer details.
    - Retrieve answers for a specific question.
    - Update or delete a specific answer.

4. Quiz Participation:
    - Start a quiz by providing the quiz ID.
    - Submit a quiz with answers by providing the quiz ID and answers.
    - Retrieve quiz results for individual users or all participants.

5. Timed Quizzes:
    - Specify the time limit for quizzes when creating them.
    - Ensure participants submit their quizzes before reaching the time limit.

## API Endpoints

The Quiz App provides the following API endpoints:

### Account App

- `GET /api/account/users/`: Retrieve a list of users.
- `POST /api/account/users/`: Create a new user.
- `GET /api/account/users/{user_id}/`: Retrieve a specific user.
- `PUT /api/account/users/{user_id}/`: Update a specific user.
- `DELETE /api/account/users/{user_id}/`: Delete a specific user.
- `POST /api/account/login/`: User login.
- `POST /api/account/logout/`: User logout.
- `POST /api/account/forgot-password/`: Send a password reset email.
- `POST /api/account/forgot-password-confirm/{token}/`: Reset password using the provided token.

### Quiz App

- `GET /api/quizzes/categories/`: Retrieve a list of categories or create a new category.
- `GET /api/quizzes/categories/{category_id}/`: Retrieve, update, or delete a specific category.
- `GET /api/quizzes/tags/`: Retrieve a list of tags or create a new tag.
- `GET /api/quizzes/tags/{tag_id}/`: Retrieve, update, or delete a specific tag.
- `GET /api/quizzes/`: Retrieve a list of quizzes or create a new quiz.
- `GET /api/quizzes/{quiz_id}/`: Retrieve, update, or delete a specific quiz.
- `GET /api/quizzes/{quiz_id}/questions/`: Retrieve a list of questions for a specific quiz or create a new question.
- `GET /api/quizzes/start/`: Start a quiz by providing the quiz ID.
- `POST /api/quizzes/submit/`: Submit a quiz with the answers.
- `GET /api/questions/{question_id}/`: Retrieve, update, or delete a specific question.
- `GET /api/questions/{question_id}/answers/`: Retrieve a list of answers for a specific question or create a new
  answer.
- `GET /api/answers/{answer_id}/`: Retrieve, update, or delete a specific answer.
- `GET /api/quizzes/{quiz_id}/feedback/`: Retrieve a list of feedback for a specific quiz or create new feedback.
- `GET /api/feedback/{feedback_id}/`: Retrieve, update, or delete a specific feedback.

## Testing

The Quiz App API includes a comprehensive set of tests to ensure the functionality and reliability of its features. The
tests are organized into different modules based on the app they belong to.

### Running the Tests

To run the tests for the Quiz app, follow the steps below:

1. Make sure you have activated your virtual environment.

2. Navigate to the project root directory, where the `manage.py` file is located.

3. Run the following command to execute the tests:

   ```shell
   python manage.py test quiz
   ```

## Generating Fake Data

To populate the database with fake users, categories, tags, and quizzes, you can use the following management commands:

### Create Users

1. To create fake users, run the following command:

   ```shell
   python manage.py create_users <num_users> <output_file>
   ```

Replace <num_users> with the desired number of fake users to create and <output_file> with the path where the usernames
and passwords will be saved.

For example, to create 10 users and save their details in a file named users.txt, run the command as follows:

   ```shell
   python manage.py create_users 10 users.txt
   ```

The command will generate fake user profiles and save their usernames and passwords in the specified file.

### Create Quizzes

To create sample quizzes with associated questions and answers, run the following command:

   ```shell
   python manage.py create_quizzes <num_quizzes> <num_questions_per_quiz>
   ```

Replace <num_quizzes> with the desired number of quizzes to create and <num_questions_per_quiz> with the number of
questions to include in each quiz.

For example, to create 5 quizzes, each with 3 questions, run the command as follows:

   ```shell
   python manage.py create_quizzes 5 3
   
   ```

The command will generate sample quizzes, populate them with random questions, and associate random categories, tags,
and users.

### Create Categories and Tags

To create categories and tags for quizzes, run the following command:

```shell
python manage.py create_categories <num_categories>
python manage.py create_tags <num_tags>
```

Replace <num_categories> and <num_tags> with the desired number of categories and tags to create.

## Contributing

Contributions to the Quiz App are welcome! If you'd like to contribute, please follow these guidelines:

- Fork the repository and create a new branch.
- Make your changes and ensure they adhere to the project's coding style and guidelines.
- Test your changes to ensure they don't introduce any regressions.
- Submit a pull request, describing the changes you've made.

## Acknowledgements

The Quiz App utilizes the following libraries and frameworks:

- [Django REST Framework](https://www.django-rest-framework.org/) - Toolkit for building RESTful APIs.

## Contact

If you have any questions, suggestions, or feedback regarding the Quiz App API, please feel free to reach out to us. We
would be happy to assist you!

- **Email**: [rayhanbillah@hotmail.com](mailto:rayhanbillah@hotmail.com)
- **GitHub**: [rayhanrock](https://github.com/rayhanrock)

You can also submit bug reports or feature requests by opening an issue in
the [GitHub repository](https://github.com/rayhanrock/quiz-api). We appreciate your contributions and involvement in
improving the Quiz App API.

Please allow us some time to respond. We'll get back to you as soon as possible.

Thank you for your interest in the Quiz App API!

