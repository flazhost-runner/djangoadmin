from behave import given, when, then
import json


@given('I have valid credentials')
def step_valid_creds(context):
    context.credentials = {'email': 'admin@admin.com', 'password': '12345678'}


@given('I have invalid credentials')
def step_invalid_creds(context):
    context.credentials = {'email': 'wrong@test.com', 'password': 'wrongpassword'}


@when('I POST to /api/v1/auth/login/')
def step_post_login(context):
    context.response = context.test.client.post(
        '/api/v1/auth/login/',
        json.dumps(context.credentials),
        content_type='application/json',
    )


@then('I should get a JWT token')
def step_get_token(context):
    data = json.loads(context.response.content)
    assert data.get('success') is True
    assert 'token' in data.get('data', {})


@then('I should get 401 status')
def step_get_401(context):
    assert context.response.status_code == 401
