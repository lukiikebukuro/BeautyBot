import json
import re
import random

def normalize_text(text):
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for pl, lat in replacements.items():
        text = text.replace(pl, lat)
    return text

class BeautyBot:
    CITY_ALIASES = {
        "koszlin": "koszalin",
        "gorzow": "gorzow wielkopolski",
        "zielona": "zielona gora",
    }
    CONCERN_ALIASES = {
        "sucha": "sucha cera",
        "cera": "sucha cera",
        "sucha cera": "sucha cera",
        "matowe": "matowe włosy",
        "wlosy": "matowe włosy",
        "matowe wlosy": "matowe włosy",
        "matowe włosy": "matowe włosy",
        "łuszczaca": "łuszcząca się skóra",
        "luszczaca": "łuszcząca się skóra",
        "skora": "łuszcząca się skóra",
        "łuszcząca się skóra": "łuszcząca się skóra",
        "podraznienia": "podrażnienia",
        "dobra": "dobra",
        "podrazniona skora": "podrażnienia",
    }
    TIPS = {
        "sucha cera": [
            "Myj twarz letnią wodą, by skóra była gładka!",
            "Używaj delikatnego żelu do mycia rano!",
            "Nakładaj krem wieczorem po chłodnej wodzie!",
            "Pij dużo wody – to podstawa nawilżenia!"
        ],
        "matowe włosy": [
            "Używaj odżywek bez silikonów!",
            "Spłukuj włosy letnią wodą!",
            "Wypróbuj maskę raz w tygodniu!"
        ],
        "łuszcząca się skóra": [
            "Peelinguj skórę raz w tygodniu!",
            "Używaj balsamów z mocznikiem!",
            "Unikaj gorących pryszniców!"
        ],
        "podrażnienia": [
            "Używaj kosmetyków hipoalergicznych!",
            "Unikaj perfumowanych produktów!",
            "Stosuj okłady z rumianku!"
        ],
        "dobra": [
            "Używaj lekkich kremów!",
            "Pamiętaj o SPF!",
            "Dbaj o dietę bogatą w witaminy!"
        ]
    }

    def __init__(self, addressStyle, city, waiting_for_concern=False, waiting_for_sub_question=False, current_sub_question=None):
        with open('static/js/station_data.json', 'r', encoding='utf-8') as f:
            self.water_data = json.load(f)
        with open('static/js/products.json', 'r', encoding='utf-8') as f:
            self.products = json.load(f)
        self.addressStyle = addressStyle or ""
        self.city = city or ""
        self.waiting_for_concern = waiting_for_concern
        self.waiting_for_sub_question = waiting_for_sub_question
        self.current_sub_question = current_sub_question
        self.sub_questions = ["sucha cera", "matowe włosy", "łuszcząca się skóra", "podrażnienia"]

    def match_city(self, user_input):
        user_input = user_input.lower().strip()
        if user_input in self.CITY_ALIASES:
            return self.CITY_ALIASES[user_input]
        for city in self.water_data.keys():
            if user_input in city.lower():
                return city
        return None

    def match_concern(self, user_input):
        user_input = normalize_text(user_input.lower().strip())
        if user_input in self.CONCERN_ALIASES:
            return self.CONCERN_ALIASES[user_input]
        user_words = set(user_input.split())
        for problem in self.sub_questions + ["dobra"]:
            norm_problem = normalize_text(problem)
            problem_words = set(norm_problem.split())
            if user_words.intersection(problem_words):
                return problem
        return None

    def get_hardness_reply(self, city):
        data = self.water_data[city]
        dot = data['kropka']
        hardness = data['twardosc']
        who_ref = ""
        if hardness == "niska":
            who_ref = "Według WHO: niska twardość to dobra woda, ale może lekko wysuszać cerę czy włosy."
        elif hardness == "umiarkowana":
            who_ref = "Według WHO: umiarkowana twardość może powodować lekkie wysuszenie skóry."
        elif hardness == "wysoka":
            who_ref = "Według WHO: wysoka twardość wody może prowadzić do podrażnień i matowych włosów."
        elif hardness == "bardzo wysoka":
            who_ref = "Według WHO: bardzo wysoka twardość wody wysusza cerę, powoduje łuszczenie i matowi włosy."
        return f"Woda w {city.capitalize()}: {hardness} (<span class='{dot}'></span>)! {who_ref} Jaki jest Twój główny problem kosmetyczny, {self.addressStyle}? (Np. sucha cera, matowe włosy, łuszcząca się skóra, podrażnienia, dobra)"

    def get_next_sub_question(self):
        if not self.current_sub_question:
            return self.sub_questions[0]
        current_index = self.sub_questions.index(self.current_sub_question)
        if current_index < len(self.sub_questions) - 1:
            return self.sub_questions[current_index + 1]
        return None

    def getHealthAdvice(self, message=""):
        message_lower = message.lower().strip()
        matched_city = self.match_city(message_lower)
        if matched_city:
            self.city = matched_city
            self.waiting_for_concern = True
            self.waiting_for_sub_question = False
            self.current_sub_question = None
            return {
                'reply': self.get_hardness_reply(matched_city),
                'city': self.city,
                'waitingForConcern': True,
                'waitingForSubQuestion': False,
                'currentSubQuestion': None
            }

        if self.waiting_for_concern:
            matched_concern = self.match_concern(message_lower)
            if matched_concern:
                self.waiting_for_concern = False
                products_for_concern = [p for p in self.products if p["problem"] == matched_concern]
                if products_for_concern:
                    product = random.choice(products_for_concern)
                    reply = f"{self.addressStyle}, polecam {product['name']} za {product['price']}. {product['description']} <a href='{product['link']}'>Kup tutaj</a>."
                    if matched_concern in self.TIPS:
                        tip = random.choice(self.TIPS[matched_concern])
                        reply += f" {tip}"
                    if matched_concern != "dobra" and self.water_data[self.city]['twardosc'] in ["wysoka", "bardzo wysoka"]:
                        dot = self.water_data[self.city]['kropka']
                        reply += f" Twarda woda w {self.city.capitalize()} (<span class='{dot}'></span>) męczy Twoją cerę, {self.addressStyle}! Działaj, zanim skóra powie dość!"
                else:
                    reply = "Niestety, nie mam produktu na ten problem."
                return {
                    'reply': f"{reply} Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')",
                    'city': self.city,
                    'waitingForConcern': False,
                    'waitingForSubQuestion': False,
                    'currentSubQuestion': None
                }
            return {
                'reply': f"Oj, {self.addressStyle}, coś Ci się palec omsknął? 😄 Wpisz np. ‘sucha cera’, ‘matowe włosy’, ‘łuszcząca się skóra’, ‘podrażnienia’, ‘dobra’ – pomogę z Twoją cerą!",
                'city': self.city,
                'waitingForConcern': True,
                'waitingForSubQuestion': False,
                'currentSubQuestion': None
            }

        if self.waiting_for_sub_question:
            if self.current_sub_question:
                if re.search(r"tak|mam", message_lower):
                    products_for_concern = [p for p in self.products if p["problem"] == self.current_sub_question]
                    if products_for_concern:
                        product = random.choice(products_for_concern)
                        reply = f"Na {self.current_sub_question} polecam {product['name']} za {product['price']}. {product['description']} <a href='{product['link']}'>Kup tutaj</a>."
                        if self.current_sub_question in self.TIPS:
                            tip = random.choice(self.TIPS[self.current_sub_question])
                            reply += f" {tip}"
                    else:
                        reply = "Niestety, nie mam produktu na ten problem."
                    next_question = self.get_next_sub_question()
                    if next_question:
                        self.current_sub_question = next_question
                        reply += f" A masz {next_question}, {self.addressStyle}? (Tak/Nie)"
                    else:
                        self.waiting_for_sub_question = False
                        self.current_sub_question = None
                        reply += f" Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')"
                    return {
                        'reply': reply,
                        'waitingForConcern': False,
                        'waitingForSubQuestion': self.waiting_for_sub_question,
                        'currentSubQuestion': self.current_sub_question,
                        'city': self.city
                    }
                elif re.search(r"nie", message_lower):
                    next_question = self.get_next_sub_question()
                    if next_question:
                        self.current_sub_question = next_question
                        return {
                            'reply': f"OK, a masz {next_question}, {self.addressStyle}? (Tak/Nie)",
                            'waitingForConcern': False,
                            'waitingForSubQuestion': self.waiting_for_sub_question,
                            'currentSubQuestion': self.current_sub_question,
                            'city': self.city
                        }
                    else:
                        self.waiting_for_sub_question = False
                        self.current_sub_question = None
                        return {
                            'reply': f"Super, {self.addressStyle}! Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')",
                            'waitingForConcern': False,
                            'waitingForSubQuestion': self.waiting_for_sub_question,
                            'currentSubQuestion': self.current_sub_question,
                            'city': self.city
                        }
                else:
                    return {
                        'reply': f"Wpisz 'tak' lub 'nie', {self.addressStyle}!",
                        'waitingForConcern': False,
                        'waitingForSubQuestion': self.waiting_for_sub_question,
                        'currentSubQuestion': self.current_sub_question,
                        'city': self.city
                    }

        if re.search(r"inny kosmetyk", message_lower):
            product = random.choice(self.products)
            reply = f"Może {product['name']} za {product['price']}? {product['description']} <a href='{product['link']}'>Kup tutaj</a>."
            return {
                'reply': f"{reply} Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')",
                'city': self.city,
                'waitingForConcern': False,
                'waitingForSubQuestion': False,
                'currentSubQuestion': None
            }

        if re.search(r"porady", message_lower):
            data = self.water_data[self.city]
            dot = data['kropka']
            if data['twardosc'] in ["wysoka", "bardzo wysoka"]:
                reply = f"Twarda woda w {self.city.capitalize()} męczy cerę i włosy, {self.addressStyle}! 😅 Myj twarz letnią wodą i używaj kremu z ceramidami wieczorem – skóra odżyje! Polecam AquaHydrate za 59 zł. <a href='https://example.com/aquahydrate'>Kup tutaj</a>."
            else:
                reply = f"Woda w {self.city.capitalize()} jest OK (<span class='{dot}'></span>), ale i tak dbaj o nawilżenie, {self.addressStyle}! Używaj lekkich kremów i odżywek bez silikonów."
            return {
                'reply': f"{reply} Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')",
                'city': self.city,
                'waitingForConcern': False,
                'waitingForSubQuestion': False,
                'currentSubQuestion': None
            }

        if re.search(r"o wodzie", message_lower):
            data = self.water_data[self.city]
            dot = data['kropka']
            hardness = data['twardosc']
            if hardness in ["wysoka", "bardzo wysoka"]:
                reply = f"Woda w {self.city.capitalize()} ma {hardness} twardość (<span class='{dot}'></span>), {self.addressStyle}! Według WHO: wysusza cerę, matowi włosy i powoduje łuszczenie. Kosmetyki jak CalmCare za 55 zł to hit dla Twoich klientów! <a href='https://example.com/calmcare'>Kup tutaj</a>. Twoja cera zasługuje na więcej!"
            else:
                reply = f"Woda w {self.city.capitalize()} ma {hardness} twardość (<span class='{dot}'></span>). Jest dość łagodna dla skóry i włosów."
            return {
                'reply': f"{reply} Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')",
                'city': self.city,
                'waitingForConcern': False,
                'waitingForSubQuestion': False,
                'currentSubQuestion': None
            }

        if re.search(r"nowe pytania", message_lower):
            self.waiting_for_sub_question = True
            self.current_sub_question = self.sub_questions[0]
            return {
                'reply': f"Masz {self.current_sub_question}, {self.addressStyle}? (Tak/Nie)",
                'waitingForConcern': False,
                'waitingForSubQuestion': self.waiting_for_sub_question,
                'currentSubQuestion': self.current_sub_question,
                'city': self.city
            }

        matched_concern = self.match_concern(message_lower)
        if matched_concern:
            products_for_concern = [p for p in self.products if p["problem"] == matched_concern]
            if products_for_concern:
                product = random.choice(products_for_concern)
                reply = f"{self.addressStyle}, polecam {product['name']} za {product['price']}. {product['description']} <a href='{product['link']}'>Kup tutaj</a>."
                if matched_concern in self.TIPS:
                    tip = random.choice(self.TIPS[matched_concern])
                    reply += f" {tip}"
                if matched_concern != "dobra" and self.water_data[self.city]['twardosc'] in ["wysoka", "bardzo wysoka"]:
                    dot = self.water_data[self.city]['kropka']
                    reply += f" Twarda woda w {self.city.capitalize()} (<span class='{dot}'></span>) męczy Twoją cerę, {self.addressStyle}! Działaj, zanim skóra powie dość!"
            else:
                reply = "Niestety, nie mam produktu na ten problem."
            return {
                'reply': f"{reply} Co jeszcze, {self.addressStyle}? (Np. 'sucha cera', 'Inny kosmetyk', 'Porady', 'O wodzie', 'Nowe pytania')",
                'city': self.city,
                'waitingForConcern': False,
                'waitingForSubQuestion': False,
                'currentSubQuestion': None
            }

        return {
            'reply': f"Oj, {self.addressStyle}, coś Ci się palec omsknął? 😄 Wpisz np. ‘sucha cera’, ‘Inny kosmetyk’, ‘Porady’, ‘O wodzie’, ‘Nowe pytania’ – pomogę z Twoją cerą!",
            'city': self.city,
            'waitingForConcern': False,
            'waitingForSubQuestion': False,
            'currentSubQuestion': None
        }