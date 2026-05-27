import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Централизованная конфигурация приложения"""

    # ========== НАСТРОЙКИ ПРИЛОЖЕНИЯ ==========
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

    # ========== ЦЕНЫ ==========
    PRICES = {
        'landing': int(os.getenv('PRICE_LANDING', 50000)),
        'corporate': int(os.getenv('PRICE_CORPORATE', 150000)),
        'shop': int(os.getenv('PRICE_SHOP', 300000))
    }

    PAGE_PRICE = int(os.getenv('PAGE_PRICE', 3000))

    # ========== БАЗОВЫЕ СТРАНИЦЫ ==========
    BASE_PAGES = {
        'landing': int(os.getenv('BASE_PAGES_LANDING', 1)),
        'corporate': int(os.getenv('BASE_PAGES_CORPORATE', 5)),
        'shop': int(os.getenv('BASE_PAGES_SHOP', 10))
    }

    # ========== ЦЕНЫ НА ФУНКЦИИ ==========
    FEATURE_PRICES = {
        'form': int(os.getenv('FEATURE_FORM_PRICE', 10000)),
        'catalog': int(os.getenv('FEATURE_CATALOG_PRICE', 30000)),
        'payment': int(os.getenv('FEATURE_PAYMENT_PRICE', 50000)),
        'crm': int(os.getenv('FEATURE_CRM_PRICE', 40000)),
        'multilang': int(os.getenv('FEATURE_MULTILANG_PRICE', 35000))
    }

    # ========== КОЭФФИЦИЕНТЫ СРОЧНОСТИ ==========
    URGENCY_MULTIPLIERS = {
        'normal': float(os.getenv('URGENCY_NORMAL', 1.0)),
        'urgent': float(os.getenv('URGENCY_URGENT', 1.3)),
        'very': float(os.getenv('URGENCY_VERY', 1.6))
    }

    # ========== БАЗОВЫЕ СРОКИ ==========
    BASE_DEADLINES = {
        'landing': int(os.getenv('DEADLINE_LANDING', 10)),
        'corporate': int(os.getenv('DEADLINE_CORPORATE', 25)),
        'shop': int(os.getenv('DEADLINE_SHOP', 45))
    }

    # ========== ВЛИЯНИЕ ФУНКЦИЙ НА СРОК ==========
    FEATURE_DEADLINE_IMPACT = {
        'catalog': int(os.getenv('FEATURE_CATALOG_DEADLINE', 5)),
        'payment': int(os.getenv('FEATURE_PAYMENT_DEADLINE', 7)),
        'crm': int(os.getenv('FEATURE_CRM_DEADLINE', 6)),
        'multilang': int(os.getenv('FEATURE_MULTILANG_DEADLINE', 4)),
        'form': int(os.getenv('FEATURE_FORM_DEADLINE', 2))
    }

    # ========== ВСПОМОГАТЕЛЬНЫЕ СЛОВАРИ ==========
    @classmethod
    def get_site_names(cls):
        """Названия типов сайтов"""
        return {
            'landing': 'Лендинг',
            'corporate': 'Корпоративный сайт',
            'shop': 'Интернет-магазин'
        }

    @classmethod
    def get_feature_names(cls):
        """Названия функций"""
        return {
            'form': 'Форма заявки',
            'catalog': 'Каталог',
            'payment': 'Онлайн-оплата',
            'crm': 'Интеграция с CRM',
            'multilang': 'Мультиязычность'
        }

    @classmethod
    def get_urgency_names(cls):
        """Названия срочности"""
        return {
            'normal': 'Обычная',
            'urgent': 'Срочно',
            'very': 'Очень срочно'
        }

    @classmethod
    def validate_site_type(cls, site_type):
        """Проверка существования типа сайта"""
        return site_type in cls.PRICES

    @classmethod
    def validate_urgency(cls, urgency):
        """Проверка существования типа срочности"""
        return urgency in cls.URGENCY_MULTIPLIERS

    @classmethod
    def validate_features(cls, features):
        """Фильтрация существующих функций"""
        return [f for f in features if f in cls.FEATURE_PRICES]