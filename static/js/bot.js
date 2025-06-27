function startBeautyBot(type) {
    const botSection = document.getElementById(`beauty-bot-${type}`);
    const messages = document.getElementById(`beauty-bot-${type}-messages`);
    const input = document.getElementById(`beauty-bot-${type}-input`);
    const sendButton = document.getElementById(`beauty-bot-${type}-send`);

    if (!botSection || !messages || !input || !sendButton) {
        console.error('Brak elementów czatu!');
        alert('Błąd: Nie znalazłem elementów czatu.');
        return;
    }

    botSection.style.display = 'block';
    let addressStyle = localStorage.getItem('beautyBotAddressStyle');
    let city = localStorage.getItem('beautyBotCity');

    if (!addressStyle) {
        const welcomeMessage = document.createElement('div');
        welcomeMessage.classList.add('bot-message');
        welcomeMessage.textContent = "Cześć! Jestem BeautyBot – sprawdzę twardość wody w Twoim mieście i dobiorę kosmetyki, by Twoja cera i włosy błyszczały jak z reklamy! 😊 Pewnie nie wiesz, ale twarda woda może wysuszać skórę, matowić włosy, a nawet powodować łuszczenie – pomogę Ci to ogarnąć! Jak mam się do Ciebie zwracać?";
        messages.appendChild(welcomeMessage);
    } else if (!city) {
        const askCityMessage = document.createElement('div');
        askCityMessage.classList.add('bot-message');
        askCityMessage.textContent = `Super, ${addressStyle}! Skąd jesteś? (Np. Grudziądz, Koszalin, Gorzów Wielkopolski, Zielona Góra?) 😊`;
        messages.appendChild(askCityMessage);
    } else {
        localStorage.setItem('beautyBotWaitingForCategory', 'true');
        localStorage.removeItem('beautyBotWaitingForProblem');
        localStorage.removeItem('beautyBotSelectedCategory');
        localStorage.removeItem('beautyBotWaitingForMoreAdvice');
        const askCategoryMessage = document.createElement('div');
        askCategoryMessage.classList.add('bot-message');
        askCategoryMessage.innerHTML = `Cześć, ${addressStyle} z ${city}! Wybierz kategorię problemu:<ul><li>skóra</li><li>włosy</li><li>oczy</li></ul>`;
        messages.appendChild(askCategoryMessage);
    }
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    sendButton.onclick = () => sendMessage(type, input, messages, sendButton);
    input.onkeypress = (e) => { if (e.key === 'Enter') sendMessage(type, input, messages, sendButton); };
}

async function sendMessage(type, input, messages, sendButton) {
    const message = input.value.trim();
    if (!message) return;

    console.log(`Wysyłanie wiadomości użytkownika: ${message}`);
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.textContent = message;
    messages.appendChild(userMessage);
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    try {
        let addressStyle = localStorage.getItem('beautyBotAddressStyle');
        let city = localStorage.getItem('beautyBotCity');
        let waitingForCategory = localStorage.getItem('beautyBotWaitingForCategory') === 'true';
        let waitingForProblem = localStorage.getItem('beautyBotWaitingForProblem') === 'true';
        let selectedCategory = localStorage.getItem('beautyBotSelectedCategory') || '';

        if (message.toLowerCase() === 'zmień miasto') {
            localStorage.removeItem('beautyBotCity');
            localStorage.removeItem('beautyBotWaitingForCategory');
            localStorage.removeItem('beautyBotWaitingForProblem');
            localStorage.removeItem('beautyBotSelectedCategory');
            localStorage.removeItem('beautyBotWaitingForMoreAdvice');
            const changeCityMessage = document.createElement('div');
            changeCityMessage.classList.add('bot-message');
            changeCityMessage.textContent = `OK, ${addressStyle}, podaj nowe miasto, aby zacząć!`;
            messages.appendChild(changeCityMessage);
            messages.scrollTop = messages.scrollHeight;
            return;
        }

        if (localStorage.getItem('beautyBotWaitingForMoreAdvice') === 'true') {
            localStorage.removeItem('beautyBotWaitingForMoreAdvice');
            if (message.toLowerCase() === 'tak') {
                localStorage.setItem('beautyBotWaitingForCategory', 'true');
                localStorage.removeItem('beautyBotSelectedCategory');
                const categoryMessage = document.createElement('div');
                categoryMessage.classList.add('bot-message');
                categoryMessage.innerHTML = `Świetnie, ${addressStyle}! Wybierz kategorię problemu:<ul><li>skóra</li><li>włosy</li><li>oczy</li></ul>`;
                messages.appendChild(categoryMessage);
            } else if (message.toLowerCase() === 'nie') {
                localStorage.removeItem('beautyBotWaitingForCategory');
                localStorage.removeItem('beautyBotWaitingForProblem');
                localStorage.removeItem('beautyBotSelectedCategory');
                localStorage.removeItem('beautyBotWaitingForMoreAdvice');
                input.disabled = true;
                if (sendButton) sendButton.disabled = true;
                const endMessage = document.createElement('div');
                endMessage.classList.add('bot-message');
                endMessage.textContent = `Dziękuję za rozmowę, ${addressStyle}! Odśwież stronę, jeśli chcesz zacząć od nowa.`;
                messages.appendChild(endMessage);
            } else {
                localStorage.setItem('beautyBotWaitingForMoreAdvice', 'true');
                const repeatMessage = document.createElement('div');
                repeatMessage.classList.add('bot-message');
                repeatMessage.textContent = `Wpisz 'tak' lub 'nie', ${addressStyle}!`;
                messages.appendChild(repeatMessage);
            }
            messages.scrollTop = messages.scrollHeight;
            return;
        }

        if (!addressStyle) {
            addressStyle = message;
            localStorage.setItem('beautyBotAddressStyle', addressStyle);
            const askCityMessage = document.createElement('div');
            askCityMessage.classList.add('bot-message');
            askCityMessage.textContent = `Super, ${addressStyle}! Skąd jesteś? (Np. Grudziądz, Koszalin, Gorzów Wielkopolski, Zielona Góra?) 😊`;
            messages.appendChild(askCityMessage);
        } else {
            console.log(`Wysyłanie żądania do /beautybot z wiadomością: ${message}`);
            const response = await fetch('https://beautybot-kmp7.onrender.com/beautybot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    addressStyle: addressStyle,
                    city: city,
                    waitingForCategory: waitingForCategory,
                    waitingForProblem: waitingForProblem,
                    selectedCategory: selectedCategory
                })
            });
            if (!response.ok) throw new Error(`Błąd komunikacji z botem: ${response.status}`);
            const data = await response.json();
            console.log('Surowa odpowiedź serwera:', data.reply); // Debugowanie
            const botResponse = document.createElement('div');
            botResponse.classList.add('bot-message');
            botResponse.innerHTML = data.reply;
            messages.appendChild(botResponse);
            localStorage.setItem('beautyBotWaitingForCategory', data.waitingForCategory.toString());
            localStorage.setItem('beautyBotWaitingForProblem', data.waitingForProblem.toString());
            localStorage.setItem('beautyBotSelectedCategory', data.selectedCategory);
            if (data.city) {
                localStorage.setItem('beautyBotCity', data.city);
            }
            if (!data.waitingForCategory && !data.waitingForProblem && data.city) {
                localStorage.setItem('beautyBotWaitingForMoreAdvice', 'true');
                const moreAdviceMessage = document.createElement('div');
                moreAdviceMessage.classList.add('bot-message');
                moreAdviceMessage.textContent = `Chcesz więcej porad, ${addressStyle}? Wpisz: tak/nie`;
                messages.appendChild(moreAdviceMessage);
            } else {
                localStorage.removeItem('beautyBotWaitingForMoreAdvice');
            }
        }
        messages.scrollTop = messages.scrollHeight;
    } catch (error) {
        console.error('Błąd:', error);
        const errorResponse = document.createElement('div');
        errorResponse.classList.add('bot-message');
        errorResponse.textContent = 'Oj, coś poszło nie tak! Spróbuj jeszcze raz.';
        messages.appendChild(errorResponse);
        messages.scrollTop = messages.scrollHeight;
    }
}