import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 20 },  // Прогрів: плавно до 20 користувачів
    { duration: '2m', target: 20 },  // Стабільне навантаження
    { duration: '1m', target: 100 }, // Стрес: різкий підйом до 100 користувачів
    { duration: '2m', target: 100 }, // Тримаємо стрес
    { duration: '1m', target: 0 },   // Охолодження: повернення до нуля
  ],
};

export default function () {
  http.get('http://127.0.0.1:8000/');
  sleep(1);
}

