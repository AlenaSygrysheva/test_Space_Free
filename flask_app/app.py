from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

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