from config import Config


class Calculator:
    """Калькулятор стоимости и сроков разработки сайта"""

    def __init__(self):
        """Инициализация с загрузкой конфигурации"""
        self.config = Config

    def calculate_price(self, site_type: str, pages: int, features: list, urgency: str) -> tuple:
        """
        Расчёт стоимости сайта

        Returns:
            tuple: (итоговая_цена, количество_доп_страниц, стоимость_функций)
        """
        # Базовая цена
        price = self.config.PRICES[site_type]

        # Дополнительные страницы
        extra_pages = max(0, pages - self.config.BASE_PAGES[site_type])
        price += extra_pages * self.config.PAGE_PRICE

        # Дополнительные функции
        features_price = sum(self.config.FEATURE_PRICES.get(f, 0) for f in features)
        price += features_price

        # Срочность
        price = round(price * self.config.URGENCY_MULTIPLIERS[urgency])

        return price, extra_pages, features_price

    def calculate_deadline(self, site_type: str, pages: int, features: list, urgency: str) -> tuple:
        """
        Расчёт срока выполнения

        Returns:
            tuple: (срок_в_днях, количество_доп_страниц)
        """
        # База + доп. страницы
        extra_pages = max(0, pages - self.config.BASE_PAGES[site_type])
        deadline = self.config.BASE_DEADLINES[site_type]
        deadline += extra_pages * 0.5  # полдня на страницу

        # Влияние функций
        for feature in features:
            deadline += self.config.FEATURE_DEADLINE_IMPACT.get(feature, 0)

        # Ускорение при срочности
        if urgency == 'urgent':
            deadline *= 0.7
        elif urgency == 'very':
            deadline *= 0.5

        return max(3, round(deadline)), extra_pages

    def generate_explanation(self, site_type: str, pages: int, features: list,
                            urgency: str, price: int, deadline: int,
                            extra_pages: int, features_price: int) -> str:
        """
        Генерация текстового пояснения к расчёту
        """
        site_names = self.config.get_site_names()
        feature_names = self.config.get_feature_names()

        explanation_parts = []

        # Базовая стоимость
        explanation_parts.append(
            f"💰 Базовая стоимость ({site_names.get(site_type, site_type)}): "
            f"{self.config.PRICES[site_type]:,} ₽"
        )

        # Дополнительные страницы
        if extra_pages > 0:
            explanation_parts.append(
                f"📄 Доп. страницы ({extra_pages} шт. × {self.config.PAGE_PRICE:,} ₽): "
                f"+{(extra_pages * self.config.PAGE_PRICE):,} ₽"
            )

        # Функции
        if features_price > 0:
            feature_names_list = [feature_names.get(f, f) for f in features]
            explanation_parts.append(
                f"⚙️ Функции: +{features_price:,} ₽ ({', '.join(feature_names_list)})"
            )

        # Срочность
        if urgency != 'normal':
            explanation_parts.append(
                f"⚡ Срочность: ×{self.config.URGENCY_MULTIPLIERS[urgency]}"
            )

        # Итог
        explanation_parts.append(
            f"<strong>📦 Итог: {price:,} ₽, срок {deadline} дней</strong>"
        )

        # Пояснение по срокам
        deadline_detail = f"📝 Из чего срок: база {self.config.BASE_DEADLINES[site_type]} дней"
        if extra_pages > 0:
            deadline_detail += f" +{extra_pages} стр.×0.5 дня"
        if features:
            deadline_detail += f" + функции {len(features)} шт."
        if urgency != 'normal':
            deadline_detail += f", ускорение ×{0.7 if urgency == 'urgent' else 0.5}"

        explanation_parts.append(deadline_detail)

        return '<br>'.join(explanation_parts)

    def calculate_full(self, site_type: str, pages: int, features: list, urgency: str) -> dict:
        """
        Полный расчёт (цена + срок + пояснение)

        Returns:
            dict: {
                'price': int,
                'deadline': int,
                'explanation': str,
                'extra_pages': int,
                'features_price': int
            }
        """
        # Валидация страниц
        pages = max(1, min(100, pages))

        # Фильтрация функций
        features = self.config.validate_features(features)

        # Расчёты
        price, extra_pages, features_price = self.calculate_price(
            site_type, pages, features, urgency
        )
        deadline, _ = self.calculate_deadline(
            site_type, pages, features, urgency
        )
        explanation = self.generate_explanation(
            site_type, pages, features, urgency, price, deadline,
            extra_pages, features_price
        )

        return {
            'price': price,
            'deadline': deadline,
            'explanation': explanation,
            'extra_pages': extra_pages,
            'features_price': features_price
        }