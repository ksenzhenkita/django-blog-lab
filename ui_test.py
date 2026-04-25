import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==========================================
# 1. PAGE OBJECTS (Опис сторінок та елементів)
# ==========================================

class LoginPage:
    """Клас, що описує сторінку Логіну"""

    def __init__(self, driver):
        self.driver = driver
        self.url = "http://127.0.0.1:8000/accounts/login/"
        # Локатори (шляхи до елементів)
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.submit_btn = (By.XPATH, "//button[@type='submit']")

    def open(self):
        self.driver.get(self.url)

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.submit_btn).click()


class PostPage:
    """Клас, що описує сторінку Поста з коментарями"""

    def __init__(self, driver):
        self.driver = driver
        # Локатори
        self.comment_input = (By.ID, "id_text")
        self.submit_btn = (By.XPATH, "//button[contains(@class, 'btn-success')]")

    def open(self, post_id):
        self.driver.get(f"http://127.0.0.1:8000/post/{post_id}/")

    def add_comment(self, text):
        # Чекаємо, поки поле з'явиться, і вводимо текст
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.comment_input)
        ).send_keys(text)

        # Використовуємо JS клік (як у минулій лабі), щоб обійти меню
        btn = self.driver.find_element(*self.submit_btn)
        self.driver.execute_script("arguments[0].click();", btn)


# ==========================================
# 2. САМІ ТЕСТИ (Використовують Page Objects)
# ==========================================

class BlogUITests(unittest.TestCase):
    def setUp(self):
        # Запускаємо браузер Chrome
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)

    def test_login_and_comment(self):
        # Ініціалізуємо сторінки
        login_page = LoginPage(self.driver)
        post_page = PostPage(self.driver)

        # Крок 1: Відкриваємо логін
        login_page.open()
        self.driver.save_screenshot("step1_login_page.png")  # Робимо скріншот!

        # Крок 2: Логінимось
        login_page.login("xx", "xx")
        time.sleep(1)  # Трохи чекаємо для красивого скріншота
        self.driver.save_screenshot("step2_after_login.png")

        # Крок 3: Відкриваємо пост (припустимо, що його ID = 1)
        post_page.open(1)
        self.driver.save_screenshot("step3_post_page.png")

        # Крок 4: Залишаємо коментар
        post_page.add_comment("Тестовий коментар через Selenium Web Driver!")
        time.sleep(1)
        self.driver.save_screenshot("step4_comment_added.png")

        # Перевіряємо, що коментар з'явився на сторінці
        self.assertIn("Тестовий коментар через Selenium Web Driver!", self.driver.page_source)

    def tearDown(self):
        # Закриваємо браузер після тесту
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()