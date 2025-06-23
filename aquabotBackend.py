import json
import random
from fuzzywuzzy import fuzz

def normalize_text(text):
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    for pl, lat in replacements.items():
        text = text.replace(pl, lat)
    return text.lower().strip()

class BeautyBot:
    CITY_ALIASES = {
        "koszlin": "koszalin",
        "gorzow": "gorzow wielkopolski",
        "zielona": "zielona gora",
        "grudziadz": "grudziadz",
        "grudziądz": "grudziadz",
        "grudziadza": "grudziadz",
    }
    CATEGORY_ALIASES = {
        "skora": "skóra",
        "wlosy": "włosy",
        "oczy": "oczy",
    }
    CATEGORIES = {
        "skóra": ["sucha cera", "przetłuszczająca się cera", "łuszcząca się skóra", "podrażnienia", "trądzik", "szorstkość", "przebarwienia"],
        "włosy": ["matowe włosy", "łamliwe włosy", "przetłuszczające się włosy", "suche włosy", "wypadające włosy", "puszące się włosy", "rozdwojone końcówki"],
        "oczy": ["suche oczy", "swędzące oczy", "zaczerwienione oczy", "opuchnięte oczy", "wrażliwe oczy", "zmęczone oczy", "pieczące oczy"]
    }

    def __init__(self, addressStyle, city, waiting_for_category=False, waiting_for_problem=False, selected_category=""):
        with open('static/js/station_data.json', 'r', encoding='utf-8') as f:
            self.water_data = json.load(f)
        with open('static/js/products.json', 'r', encoding='utf-8') as f:
            self.products = json.load(f)
        self.addressStyle = addressStyle or ""
        self.city = city or ""
        self.waiting_for_category = waiting_for_category
        self.waiting_for_problem = waiting_for_problem
        self.selected_category = selected_category

    def get_hardness_reply(self, city):
        city = city.lower()
        data = self.water_data.get(city, {})
        dot = data.get('kropka', 'green-dot')
        hardness = data.get('twardosc', 'nieznana')
        who_ref = ""
        if hardness == "niska":
            who_ref = "Według WHO: niska twardość to dobra woda, ale może lekko wysuszać cerę czy włosy."
        elif hardness == "umiarkowana":
            who_ref = "Według WHO: umiarkowana twardość może powodować lekkie wysuszenie skóry."
        elif hardness == "wysoka":
            who_ref = "Według WHO: wysoka twardość wody może prowadzić do podrażnień i matowych włosów."
        elif hardness == "bardzo wysoka":
            who_ref = "Według WHO: bardzo wysoka twardość wody wysusza cerę, powoduje łuszczenie i matowi włosy."
        range_text = self.get_hardness_range(dot)
        return f"Woda w {city.capitalize()} ma {hardness} twardość ({range_text}) (<span class='dot {dot}'></span>)! {who_ref}<br>Wybierz kategorię problemu, {self.addressStyle}:<ul><li>skóra</li><li>włosy</li><li>oczy</li></ul>"

    def get_hardness_range(self, dot):
        if dot == "green-dot":
            return "<150 mg CaCO3/l"
        elif dot == "orange-dot":
            return "150-200 mg CaCO3/l"
        elif dot == "yellow-dot":
            return "200-250 mg CaCO3/l"
        else:
            return ">250 mg CaCO3/l"

    def match_city(self, user_input):
        user_input = user_input.lower().strip()
        if user_input in self.CITY_ALIASES:
            return self.CITY_ALIASES[user_input]
        for city in self.water_data.keys():
            if user_input in city.lower():
                return city
        return None

    def match_category(self, user_input):
        user_input = user_input.lower().strip()
        if user_input in self.CATEGORY_ALIASES:
            return self.CATEGORY_ALIASES[user_input]
        norm_input = normalize_text(user_input)
        for category in self.CATEGORIES.keys():
            norm_category = normalize_text(category)
            if norm_input == norm_category:
                return category
        return None

    def match_concern(self, user_input):
        user_input = normalize_text(user_input)
        best_match = None
        best_score = 0
        for problem in self.CATEGORIES.get(self.selected_category, []):
            norm_problem = normalize_text(problem)
            score = fuzz.partial_ratio(user_input, norm_problem)
            if score > best_score:
                best_score = score
                best_match = problem
        if best_score > 70:
            return best_match
        return None

    def getHealthAdvice(self, message=""):
        message_lower = message.lower().strip()
        norm_message = normalize_text(message_lower)
        matched_city = self.match_city(message_lower)
        if matched_city:
            self.city = matched_city
            self.waiting_for_category = True
            self.waiting_for_problem = False
            self.selected_category = ""
            reply = self.get_hardness_reply(matched_city)
            return {
                'reply': reply,
                'city': self.city,
                'waitingForCategory': True,
                'waitingForProblem': False,
                'selectedCategory': ""
            }
        elif norm_message in ["zmien miasto", "zmienmiasto", "zmień miasto", "zmieńmiasto"] and self.city:
            self.city = ""
            self.waiting_for_category = False
            self.waiting_for_problem = False
            self.selected_category = ""
            reply = f"OK, {self.addressStyle}, podaj nowe miasto, aby zacząć!"
            return {
                'reply': reply,
                'city': self.city,
                'waitingForCategory': False,
                'waitingForProblem': False,
                'selectedCategory': ""
            }
        elif not self.city or (self.city and not self.waiting_for_category and not self.waiting_for_problem):
            matched_city = self.match_city(message_lower)
            if matched_city:
                self.city = matched_city
                self.waiting_for_category = True
                self.waiting_for_problem = False
                self.selected_category = ""
                reply = self.get_hardness_reply(matched_city)
                return {
                    'reply': reply,
                    'city': self.city,
                    'waitingForCategory': True,
                    'waitingForProblem': False,
                    'selectedCategory': ""
                }
            else:
                self.city = "unknown"
                self.waiting_for_category = True
                reply = f"Twojego miasta jeszcze nie ma w naszej bazie, {self.addressStyle}, bo zbieramy dane ręcznie aby były jak najbardziej dokładne. Możesz kontynuować, a ja doradzę na podstawie typowych problemów z wodą!<br>Wybierz kategorię problemu, {self.addressStyle}:<ul><li>skóra</li><li>włosy</li><li>oczy</li></ul>"
                return {
                    'reply': reply,
                    'city': self.city,
                    'waitingForCategory': True,
                    'waitingForProblem': False,
                    'selectedCategory': ""
                }

        if self.waiting_for_category:
            matched_category = self.match_category(message_lower)
            if matched_category:
                self.selected_category = matched_category
                self.waiting_for_category = False
                self.waiting_for_problem = True
                problems = self.CATEGORIES[matched_category]
                reply = f"Wybierz problem z kategorii {matched_category}, {self.addressStyle}:<ul>" + "".join([f"<li>{p}</li>" for p in problems]) + "</ul>"
                return {
                    'reply': reply,
                    'city': self.city,
                    'waitingForCategory': False,
                    'waitingForProblem': True,
                    'selectedCategory': self.selected_category
                }
            return {
                'reply': f"Nie rozumiem, {self.addressStyle}! Wpisz kategorię: skóra, włosy, oczy.",
                'city': self.city,
                'waitingForCategory': True,
                'waitingForProblem': False,
                'selectedCategory': ""
            }

        if self.waiting_for_problem:
            matched_concern = self.match_concern(message_lower)
            if matched_concern and matched_concern in self.CATEGORIES[self.selected_category]:
                products_for_concern = [p for p in self.products if p["problem"] == matched_concern]
                if products_for_concern:
                    product = random.choice(products_for_concern)
                    reply = f"{self.addressStyle}, dla {matched_concern} polecam {product['name']} za {product['price']}. {product['description']} <a href='{product['link']}'>Kup tutaj</a>"
                else:
                    reply = f"Niestety, nie mam produktu na {matched_concern}, {self.addressStyle}."
                return {
                    'reply': reply,
                    'city': self.city,
                    'waitingForCategory': False,
                    'waitingForProblem': False,
                    'selectedCategory': ""
                }
            return {
                'reply': f"Nie rozumiem, {self.addressStyle}! Wpisz problem z kategorii {self.selected_category}:<ul>" + "".join([f"<li>{p}</li>" for p in self.CATEGORIES[self.selected_category]]) + "</ul>",
                'city': self.city,
                'waitingForCategory': False,
                'waitingForProblem': True,
                'selectedCategory': self.selected_category
            }

        return {
            'reply': f"Hmm, {self.addressStyle}, nie rozumiem. Podaj miasto, aby zacząć!",
            'city': self.city,
            'waitingForCategory': False,
            'waitingForProblem': False,
            'selectedCategory': ""
        }