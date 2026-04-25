from selenium import webdriver

def before_all(context):
    # Відкриваємо браузер перед початком усіх тестів
    context.browser = webdriver.Chrome()
    context.browser.implicitly_wait(5)
    context.browser.maximize_window()

def after_all(context):
    # Закриваємо браузер в кінці
    context.browser.quit()