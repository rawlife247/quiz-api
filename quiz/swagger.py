from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def category_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Get list of all categories",
    )


def category_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Create a category",
    )


def category_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a category instance",
    )


def category_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a category instance",
    )


def category_delete_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a category",
        responses={
            204: "No Content",
        }
    )


def tag_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Get list of all tages",
    )


def tag_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Create a tag",
    )


def tag_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a tag instance",
    )


def tag_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a tag instance",
    )


def tag_delete_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a tag",
        responses={
            204: "No Content",
        }
    )


def quiz_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Get list of all quizzes",
    )


def quiz_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Create a quiz",
    )


def quiz_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a quiz",
    )


def quiz_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a quiz",
    )


def quiz_delete_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a quiz",
        responses={
            204: "No Content",
        }
    )


def start_quiz_swagger_schema():
    return swagger_auto_schema(
        operation_description="Start a quiz",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quiz_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='The ID of the quiz to start',
                ),
            },
            required=['quiz_id'],
        ),
        responses={
            200: openapi.Response(
                description='Quiz started successfully',
                examples={
                    'application/json': {
                        'message': 'Quiz started successfully',
                    },
                },
            ),
            400: openapi.Response(
                description='Invalid quiz ID',
                examples={
                    'application/json': {
                        'quiz_id': 'Invalid quiz ID',
                    },
                },
            ),
        }
    )


def submit_quiz_swagger_schema():
    return swagger_auto_schema(
        operation_description="Submit a quiz",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quiz_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='The ID of the quiz to submit',
                ),
                'answers': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question_id': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='The ID of the question',
                            ),
                            'selected_answer': openapi.Schema(
                                type=openapi.TYPE_INTEGER,
                                description='The ID of the selected answer',
                            ),
                        },
                        required=['question_id', 'selected_answer'],
                    ),
                ),
            },
            required=['quiz_id', 'answers'],
        ),
        responses={
            200: openapi.Response(
                description='Quiz submitted successfully',
                examples={
                    'application/json': {
                        'message': 'Quiz submitted successfully',
                        'data': {},
                    },
                },
            ),
        }
    )


def question_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Get a list of questions",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the Quiz to list all questions',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )


def question_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Create a question",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the Quiz , where the question should be added',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )


def question_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a question",
    )


def question_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a question",
    )


def question_delete_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a question",
        responses={
            204: "No Content",
        }
    )


def answer_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Get a list of answers",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the question to list all answers',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )


def answer_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Create a answer",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the question , where the answer should be added',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )


def answer_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a answer",
    )


def answer_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a answer",
    )


def answer_delete_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a answer",
        responses={
            204: "No Content",
        }
    )


def feedback_list_swagger_schema():
    return swagger_auto_schema(
        operation_description="Get the list of feedbacks",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the Quiz , to get all its feedbacks',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )


def feedback_create_swagger_schema():
    return swagger_auto_schema(
        operation_description="Give feedback to a Quiz",
        manual_parameters=[
            openapi.Parameter(
                name='id',
                in_=openapi.IN_PATH,
                description='ID of the Quiz , to give feedback',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )


def feedback_retrieve_swagger_schema():
    return swagger_auto_schema(
        operation_description="Retrieve a feedback",
    )


def feedback_update_swagger_schema():
    return swagger_auto_schema(
        operation_description="Update a feedback",
    )


def feedback_delete_swagger_schema():
    return swagger_auto_schema(
        operation_description="Delete a feedback",
        responses={
            204: "No Content",
        }
    )
