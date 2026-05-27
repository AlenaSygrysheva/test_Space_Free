# import os
# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv
#
# # Загружаем .env
# load_dotenv()
#
# app = Flask(__name__)
#
# # ========== ЗАГРУЗКА КОНСТАНТ ИЗ .ENV ==========
# # Базовые цены
# BASE_PRICES = {
#     'landing': int(os.getenv('PRICE_LANDING', 50000)),
#     'corporate': int(os.getenv('PRICE_CORPORATE', 150000)),
#     'shop': int(os.getenv('PRICE_SHOP', 300000))
# }
#
# PAGE_PRICE = int(os.getenv('PAGE_PRICE', 3000))
#
# BASE_PAGES = {
#     'landing': int(os.getenv('BASE_PAGES_LANDING', 1)),
#     'corporate': int(os.getenv('BASE_PAGES_CORPORATE', 5)),
#     'shop': int(os.getenv('BASE_PAGES_SHOP', 10))
# }
#
# FEATURE_PRICES = {
#     'form': int(os.getenv('FEATURE_FORM_PRICE', 10000)),
#     'catalog': int(os.getenv('FEATURE_CATALOG_PRICE', 30000)),
#     'payment': int(os.getenv('FEATURE_PAYMENT_PRICE', 50000)),
#     'crm': int(os.getenv('FEATURE_CRM_PRICE', 40000)),
#     'multilang': int(os.getenv('FEATURE_MULTILANG_PRICE', 35000))
# }
#
# URGENCY_MULTIPLIER = {
#     'normal': float(os.getenv('URGENCY_NORMAL', 1)),
#     'urgent': float(os.getenv('URGENCY_URGENT', 1.3)),
#     'very': float(os.getenv('URGENCY_VERY', 1.6))
# }
#
# BASE_DEADLINE = {
#     'landing': int(os.getenv('DEADLINE_LANDING', 10)),
#     'corporate': int(os.getenv('DEADLINE_CORPORATE', 25)),
#     'shop': int(os.getenv('DEADLINE_SHOP', 45))
# }
#
# FEATURE_DEADLINE_IMPACT = {
#     'catalog': int(os.getenv('FEATURE_CATALOG_DEADLINE', 5)),
#     'payment': int(os.getenv('FEATURE_PAYMENT_DEADLINE', 7)),
#     'crm': int(os.getenv('FEATURE_CRM_DEADLINE', 6)),
#     'multilang': int(os.getenv('FEATURE_MULTILANG_DEADLINE', 4)),
#     'form': int(os.getenv('FEATURE_FORM_DEADLINE', 2))
# }
#
#
# # ========== ФУНКЦИИ РАСЧЁТА ==========
# def calculate_price(site_type, pages, features, urgency):
#     """Расчёт стоимости"""
#     price = BASE_PRICES[site_type]
#
#     extra_pages = max(0, pages - BASE_PAGES[site_type])
#     price += extra_pages * PAGE_PRICE
#
#     features_price = sum(FEATURE_PRICES.get(f, 0) for f in features)
#     price += features_price
#
#     price = round(price * URGENCY_MULTIPLIER[urgency])
#
#     return price, extra_pages, features_price
#
#
# def calculate_deadline(site_type, pages, features, urgency):
#     """Расчёт срока"""
#     extra_pages = max(0, pages - BASE_PAGES[site_type])
#     deadline = BASE_DEADLINE[site_type]
#     deadline += extra_pages * 0.5
#
#     for feature in features:
#         deadline += FEATURE_DEADLINE_IMPACT.get(feature, 0)
#
#     if urgency == 'urgent':
#         deadline *= 0.7
#     elif urgency == 'very':
#         deadline *= 0.5
#
#     return max(3, round(deadline)), extra_pages
#
#
# def generate_explanation(site_type, pages, features, urgency, price, deadline, extra_pages, features_price):
#     """Генерация пояснения"""
#     site_names = {
#         'landing': 'Лендинг',
#         'corporate': 'Корпоративный сайт',
#         'shop': 'Интернет-магазин'
#     }
#
#     feature_names = {
#         'form': 'Форма заявки',
#         'catalog': 'Каталог',
#         'payment': 'Онлайн-оплата',
#         'crm': 'Интеграция с CRM',
#         'multilang': 'Мультиязычность'
#     }
#
#     explanation = f"💰 Базовая стоимость ({site_names.get(site_type, site_type)}): {BASE_PRICES[site_type]:,} ₽<br>"
#
#     if extra_pages > 0:
#         explanation += f"📄 Доп. страницы ({extra_pages} шт. × {PAGE_PRICE:,} ₽): +{(extra_pages * PAGE_PRICE):,} ₽<br>"
#
#     if features_price > 0:
#         feature_names_list = [feature_names.get(f, f) for f in features]
#         explanation += f"⚙️ Функции: +{features_price:,} ₽ ({', '.join(feature_names_list)})<br>"
#
#     if urgency != 'normal':
#         explanation += f"⚡ Срочность: ×{URGENCY_MULTIPLIER[urgency]}<br>"
#
#     explanation += f"<strong>📦 Итог: {price:,} ₽, срок {deadline} дней</strong><br>"
#     explanation += f"📝 Из чего срок: база {BASE_DEADLINE[site_type]} дней"
#
#     if extra_pages > 0:
#         explanation += f" +{extra_pages} стр.×0.5 дня"
#     if features:
#         explanation += f" + функции {len(features)} шт."
#     if urgency != 'normal':
#         explanation += f", ускорение ×{0.7 if urgency == 'urgent' else 0.5}"
#
#     return explanation
#
#
# # ========== FLASK МАРШРУТЫ ==========
# @app.route('/')
# def index():
#     """Главная страница"""
#     return render_template('index.html')
#
#
# @app.route('/calculate', methods=['POST'])
# def calculate():
#     """API endpoint для расчёта"""
#     print("=== Получен запрос на /calculate ===")  # Отладка
#
#     try:
#         data = request.get_json()
#         print("Полученные данные:", data)  # Отладка
#
#         # Валидация
#         site_type = data.get('type')
#         if site_type not in BASE_PRICES:
#             return jsonify({'error': 'Неверный тип сайта'}), 400
#
#         pages = int(data.get('pages', 1))
#         pages = max(1, min(100, pages))
#
#         features = data.get('features', [])
#         features = [f for f in features if f in FEATURE_PRICES]
#
#         urgency = data.get('urgency', 'normal')
#         if urgency not in URGENCY_MULTIPLIER:
#             urgency = 'normal'
#
#         # Расчёты
#         price, extra_pages, features_price = calculate_price(site_type, pages, features, urgency)
#         deadline, _ = calculate_deadline(site_type, pages, features, urgency)
#         explanation = generate_explanation(site_type, pages, features, urgency, price, deadline, extra_pages,
#                                            features_price)
#
#         result = {
#             'price': price,
#             'deadline': deadline,
#             'explanation': explanation,
#             'extra_pages': extra_pages,
#             'features_price': features_price
#         }
#
#         print("Результат:", result)  # Отладка
#         return jsonify(result)
#
#     except Exception as e:
#         print("ОШИБКА:", str(e))  # Отладка
#         import traceback
#         traceback.print_exc()  # Печатаем полную ошибку
#         return jsonify({'error': str(e)}), 500
#
#
# if __name__ == '__main__':
#     port = int(os.getenv('FLASK_PORT', 5000))
#     debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
#     print(f"Запуск сервера на порту {port}, debug={debug}")
#     app.run(host='0.0.0.0', port=port, debug=debug)

from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Константы (те же самые)
BASE_PRICES = {
    'landing': 50000,
    'corporate': 150000,
    'shop': 300000
}
PAGE_PRICE = 3000
BASE_PAGES = {'landing': 1, 'corporate': 5, 'shop': 10}
FEATURE_PRICES = {
    'form': 10000, 'catalog': 30000, 'payment': 50000,
    'crm': 40000, 'multilang': 35000
}
URGENCY_MULTIPLIER = {'normal': 1, 'urgent': 1.3, 'very': 1.6}
BASE_DEADLINE = {'landing': 10, 'corporate': 25, 'shop': 45}
FEATURE_DEADLINE_IMPACT = {
    'catalog': 5, 'payment': 7, 'crm': 6, 'multilang': 4, 'form': 2
}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None, form_data=None)


@app.route('/', methods=['POST'])
def calculate_form():
    """Обработка отправки формы (без JS)"""
    # Получаем данные из формы
    site_type = request.form.get('type')
    pages = int(request.form.get('pages', 1))
    features = request.form.getlist('features')
    urgency = request.form.get('urgency', 'normal')

    # ... твоя логика расчёта ...
    price = BASE_PRICES[site_type]
    extra_pages = max(0, pages - BASE_PAGES[site_type])
    price += extra_pages * PAGE_PRICE
    features_price = sum(FEATURE_PRICES.get(f, 0) for f in features)
    price += features_price
    price = round(price * URGENCY_MULTIPLIER[urgency])

    deadline = BASE_DEADLINE[site_type]
    deadline += extra_pages * 0.5
    for f in features:
        deadline += FEATURE_DEADLINE_IMPACT.get(f, 0)
    if urgency == 'urgent':
        deadline *= 0.7
    elif urgency == 'very':
        deadline *= 0.5
    deadline = max(3, round(deadline))

    explanation = f"💰 Базовая стоимость: {BASE_PRICES[site_type]:,} ₽<br>"
    if extra_pages > 0:
        explanation += f"📄 Доп. страницы: +{(extra_pages * PAGE_PRICE):,} ₽<br>"
    if features_price > 0:
        explanation += f"⚙️ Функции: +{features_price:,} ₽<br>"
    if urgency != 'normal':
        explanation += f"⚡ Срочность: ×{URGENCY_MULTIPLIER[urgency]}<br>"
    explanation += f"<strong>Итог: {price:,} ₽, срок {deadline} дней</strong>"

    return render_template('index.html',
                           result={'price': f"{price:,}", 'deadline': deadline, 'explanation': explanation},
                           form_data={'type': site_type, 'pages': pages, 'features': features, 'urgency': urgency})


if __name__ == '__main__':
    app.run(debug=True)