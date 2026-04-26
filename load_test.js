import http from 'k6/http';
import { check, sleep } from 'k6';
import { parseHTML } from 'k6/html';

// Налаштування навантаження: 5 користувачів працюють одночасно протягом 30 секунд
export const options = {
  vus: 5,
  duration: '30s',
};

const BASE_URL = 'http://127.0.0.1:8000';

export default function () {
  // 1. Відкриваємо сторінку логіну
  let res = http.get(`${BASE_URL}/accounts/login/`);

  // ВАЖЛИВО: Витягуємо CSRF-токен з HTML сторінки
  const doc = parseHTML(res.body);
  const csrfToken = doc.find('input[name="csrfmiddlewaretoken"]').val();

  // 2. Логінимось (передаємо логін, пароль і токен)
  res = http.post(`${BASE_URL}/accounts/login/`, {
    username: 'xx',
    password: 'xx',
    csrfmiddlewaretoken: csrfToken,
  });

  // Перевіряємо, чи успішно залогінились (Django робить редирект на головну, тому статус 200)
  check(res, { 'Логін успішний': (r) => r.status === 200 });

  sleep(1); // Імітуємо час "думки" користувача (think time)

  // 3. Читаємо пост (припустимо, що пост з ID=1 існує)
  res = http.get(`${BASE_URL}/post/1/`);
  check(res, { 'Пост завантажено': (r) => r.status === 200 });

  sleep(2); // Користувач читає пост 2 секунди

  // 4. Логаут (у Django він часто працює просто через GET або POST запит)
  // Робимо запит на головну, щоб отримати новий токен для виходу
  let homeRes = http.get(BASE_URL);
  const homeDoc = parseHTML(homeRes.body);
  const logoutCsrf = homeDoc.find('input[name="csrfmiddlewaretoken"]').val() || csrfToken;

  res = http.post(`${BASE_URL}/accounts/logout/`, {
    csrfmiddlewaretoken: logoutCsrf,
  });
  check(res, { 'Вихід успішний': (r) => r.status === 200 });
}