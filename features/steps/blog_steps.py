from behave import given, when, then
from selenium.webdriver.common.by import By

@given('я відкриваю сторінку логіну')
def step_impl(context):
    context.browser.get("http://127.0.0.1:8000/accounts/login/")

@when('я вводжу логін "{username}" та пароль "{password}"')
def step_impl(context, username, password):
    context.browser.find_element(By.NAME, "username").send_keys(username)
    context.browser.find_element(By.NAME, "password").send_keys(password)

@when('я натискаю кнопку входу')
def step_impl(context):
    context.browser.find_element(By.XPATH, "//button[@type='submit']").click()

@then('я маю побачити напис "{text}"')
def step_impl(context, text):
    assert text in context.browser.page_source

@when('я переходжу на сторінку поста {post_id}')
def step_impl(context, post_id):
    context.browser.get(f"http://127.0.0.1:8000/post/{post_id}/")

@when('я вводжу коментар "{comment}"')
def step_impl(context, comment):
    context.browser.find_element(By.ID, "id_text").send_keys(comment)

@when('я натискаю кнопку відправити коментар')
def step_impl(context):
    # Використовуємо наш трюк з JavaScript для кнопки
    btn = context.browser.find_element(By.XPATH, "//button[contains(@class, 'btn-success')]")
    context.browser.execute_script("arguments[0].click();", btn)

@then('я маю побачити коментар "{comment}" на сторінці')
def step_impl(context, comment):
    assert comment in context.browser.page_source