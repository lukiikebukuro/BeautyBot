BEAUTYBOT – TWÓJ BOT DO SPRZEDAŻY KOSMETYKÓW
(Wersja bez montażu – dla tych, co mają informatyka)  
Cześć! Ten bot pomoże Ci sprzedawać kosmetyki, mówiąc klientom, czy w ich mieście woda jest twarda i jaki kosmetyk wybrać (np. krem na suchą cerę). Nie musisz znać się na komputerach – pokażemy, jak to uruchomić w 15 minut. Jeśli coś jest niejasne, wpisz pytanie na stronie grok.com (to taki mądry czat) albo zapytaj informatyka.  
JAK URUCHOMIĆ BOTA?
(Instrukcja krok po kroku, jakbyś robił kanapkę)  
KROK 1: POBIERZ PROGRAM (PYTHON)

Bot potrzebuje programu zwanego Python, żeby działać.  
Wejdź na stronę: www.python.org (otwórz w przeglądarce, np. Chrome).  
Kliknij przycisk „Downloads” (na górze strony).  
Pobierz najnowszą wersję (np. Python 3.11) – kliknij „Download Python”.  
Otwórz pobrany plik i zainstaluj:  
Ważne! Zaznacz pole „Add Python to PATH” (to malutkie okienko na dole).  
Klikaj „Next” i „Install”, aż się skończy.



KROK 2: OTWÓRZ FOLDER Z BOTEM

Znajdź na komputerze folder kosmetyki (np. w C:\Users\lpisk\Projects\szablonbota\kosmetyki).  
Kliknij folder prawym przyciskiem myszy i wybierz „Otwórz w terminalu”.  
Jeśli masz Windows, może być „Otwórz w PowerShell” albo „Otwórz w Wierszu polecenia”.  
Terminal to czarne okienko, gdzie wpisujesz komendy – nie bój się, to proste!  
Jeśli nie widzisz „Otwórz w terminalu”, otwórz folder, kliknij pasek adresu u góry, wpisz „cmd” i naciśnij Enter – otworzy się terminal.



KROK 3: ZAINSTALUJ DODATKI DO BOTA

W terminalu (czarne okienko) wpisz dokładnie:pip install -r requirements.txt  
Naciśnij Enter i poczekaj, aż się zainstaluje (to jak pobieranie aplikacji na telefon).  
Jeśli coś nie działa, wpisz pytanie na grok.com, np. „Dlaczego pip nie działa?”

KROK 4: WŁĄCZ BOTA

W tym samym terminalu wpisz:python app.py  
Naciśnij Enter. Powinno pokazać coś jak „Running on http://localhost:3000”.  
„localhost:3000” to adres bota na Twoim komputerze – nie Twoja strona, tylko miejsce, gdzie testujesz bota.

KROK 5: SPRAWDŹ BOTA W PRZEGLĄDARCE

Otwórz przeglądarkę (np. Chrome, Firefox).  
W pasku adresu wpisz: http://localhost:3000  
Zobaczysz czat z botem. Wpisz miasto, np. „Warszawa”, a bot powie:„Twardość w Warszawa to niska (zielona kropka). Sucha cera? Sprawdź L’Oreal Krem!”  
Jeśli coś nie działa, napisz do nas (twoj@email.pl) lub zapytaj na grok.com.

JAK ZMIENIĆ KOSMETYKI?

Bot poleca kosmetyki z pliku products.json (znajdziesz go w folderze kosmetyki).  
Otwórz products.json w Notatniku (kliknij prawym przyciskiem, wybierz „Otwórz za pomocą” → „Notatnik”).  
Zmień nazwę kosmetyku, cenę lub link na Twój sklep, np.:[{"name": "Vichy Krem", "price": 60, "link": "twojsklep.pl/vichy"}]
Zapisz plik (Plik → Zapisz).  
Wróć do terminalu, zatrzymaj bota (naciśnij Ctrl+C), i uruchom ponownie:python app.py  
Sprawdź w przeglądarce – bot poleci Twój kosmetyk!

CO ROBI BOT?

Klient wpisuje miasto (np. „Płock”).  
Bot mówi, czy woda jest twarda (niska, umiarkowana, wysoka, bardzo wysoka) i pokazuje kolorową kropkę:  
Zielona: Woda OK, cera w porządku.  
Pomarańczowa: Trochę twarda, może wysuszać cerę.  
Żółta: Twarda, problemy z cerą i włosami.  
Czerwona: Bardzo twarda, koniecznie kosmetyk!


Bot poleca kosmetyk z Twojego sklepu (np. „Sprawdź Vichy Krem!”).

CO DOSTAJESZ?

Dane dla 32 dużych miast (np. Warszawa 1.8M, Kraków 780K, Wrocław 650K, Łódź 670K, Poznań 530K).  
Bot pokazuje poziom twardości (kółeczka), nie dokładne dane – to nasza tajemnica!  
Wkrótce uruchomimy Skankran.pl (za 2-3 miesiące). Kup bota, a dostaniesz wersję premium za darmo – dokładne dane o wodzie z różnych stacji, 14 parametrów, żeby wiedzieć, gdzie sprzedawać kosmetyki!  
Chcesz, żebyśmy ustawili bota za Ciebie? Kup wersję z montażem (1499 zł, napisz: twoj@email.pl).

PROBLEM?

Zapytaj na grok.com (np. „Jak otworzyć terminal?”).  
Napisz do nas: twoj@email.pl.  
Jeśli masz informatyka, pokaż mu ten plik – ogarnie w 5 minut!

Powodzenia! Twój bot podbije sprzedaż kosmetyków i wyprzedzi konkurencję! 😊
