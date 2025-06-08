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
    let waitingForSubQuestion = localStorage.getItem('beautyBotWaitingForSubQuestion') === 'true';
    let currentSubQuestion = localStorage.getItem('beautyBotCurrentSubQuestion') || '';

    if (!addressStyle) {
        messages.innerHTML = '<p class="bot-message">Cześć! Jestem BeautyBot – sprawdzę twardość wody w Twoim mieście i dobiorę kosmetyki, by Twoja cera i włosy błyszczały jak z reklamy! 😊 Pewnie nie wiesz, ale twarda woda może wysuszać skórę, matowić włosy, a nawet powodować łuszczenie – pomogę Ci to ogarnąć! Jak mam się do Ciebie zwracać?</p>';
    } else if (!city) {
        messages.innerHTML = `<p class="bot-message">Super, ${addressStyle}! Skąd jesteś? (Np. Grudziądz, Koszalin, Gorzów Wielkopolski, Zielona Góra?) 😊</p>`;
    } else {
        messages.innerHTML = `<p class="bot-message">Cześć, ${addressStyle} z ${city}! Jaki jest Twój główny problem kosmetyczny? (Np. sucha cera, matowe włosy, łuszcząca się skóra, podrażnienia, dobra) 😊</p>`;
    }
    input.value = '';

    sendButton.onclick = () => sendMessage(type, input, messages);
    input.onkeypress = (e) => { if (e.key === 'Enter') sendMessage(type, input, messages); };
}

async function sendMessage(type, input, messages) {
    const message = input.value.trim();
    if (!message) return;

    messages.innerHTML += `<p class="user-message">${message}</p>`;
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    try {
        let addressStyle = localStorage.getItem('beautyBotAddressStyle');
        let city = localStorage.getItem('beautyBotCity');
        let waitingForConcern = localStorage.getItem('beautyBotWaitingForConcern') === 'true';
        let waitingForSubQuestion = localStorage.getItem('beautyBotWaitingForSubQuestion') === 'true';
        let currentSubQuestion = localStorage.getItem('beautyBotCurrentSubQuestion') || '';
        const { getColor } = window.utilis || {};  // Import getColor z utilis.js

        if (!addressStyle) {
            addressStyle = message;
            localStorage.setItem('beautyBotAddressStyle', addressStyle);
            messages.innerHTML += `<p class="bot-message">Super, ${addressStyle}! Skąd jesteś? (Np. Grudziądz, Koszalin, Gorzów Wielkopolski, Zielona Góra?) 😊</p>`;
        } else if (!city) {
            const response = await fetch('https://beautybot-backend-9e66a353b67d.herokuapp.com/verify_city', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ city: message })
            });
            const data = await response.json();
            if (data.valid) {
                city = data.city;
                localStorage.setItem('beautyBotCity', city);
                const hardnessResponse = await fetch('https://beautybot-backend-9e66a353b67d.herokuapp.com/get_hardness', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ city: city })
                });
                const hardnessData = await hardnessResponse.json();
                // Wyciągnij wartość liczbową z odpowiedzi (np. "242.5" z "Woda w Gorzowie: 242.5 mg/L")
                const hardnessValue = hardnessData.reply.match(/\d+\.?\d*/)?.[0] || '200'; // Domyślnie 200, jeśli brak
                // Dodaj kółeczko z odpowiednim kolorem
                messages.innerHTML += `<p class="bot-message">${hardnessData.reply} <span class="dot ${getColor('twardosc', hardnessValue)}"></span></p>`;
                localStorage.setItem('beautyBotWaitingForConcern', 'true');
            } else {
                messages.innerHTML += `<p class="bot-message">Nie znam miasta '${message}', ${addressStyle}! 😕 Wpisz np. 'Koszalin'.</p>`;
            }
        } else {
            const response = await fetch('https://beautybot-backend-9e66a353b67d.herokuapp.com/beautybot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    addressStyle: addressStyle,
                    city: city,
                    waitingForConcern: waitingForConcern,
                    waitingForSubQuestion: waitingForSubQuestion,
                    currentSubQuestion: currentSubQuestion
                })
            });
            const data = await response.json();
            // Wyciągnij wartość twardości, jeśli jest w odpowiedzi
            const hardnessValue = data.reply.match(/\d+\.?\d*/)?.[0] || '200';
            messages.innerHTML += `<p class="bot-message">${data.reply} <span class="dot ${getColor('twardosc', hardnessValue)}"></span></p>`;

            if (data.waitingForConcern !== undefined) {
                localStorage.setItem('beautyBotWaitingForConcern', data.waitingForConcern);
            }
            if (data.waitingForSubQuestion !== undefined) {
                localStorage.setItem('beautyBotWaitingForSubQuestion', data.waitingForSubQuestion);
            }
            if (data.currentSubQuestion) {
                localStorage.setItem('beautyBotCurrentSubQuestion', data.currentSubQuestion);
            } else {
                localStorage.removeItem('beautyBotCurrentSubQuestion');
            }
            if (data.city && data.city !== city) {
                localStorage.setItem('beautyBotCity', data.city);
            }
        }
        messages.scrollTop = messages.scrollHeight;
    } catch (error) {
        console.error('Błąd:', error);
        messages.innerHTML += `<p class="bot-message">Oj, coś poszło nie tak! Spróbuj jeszcze raz.</p>`;
        messages.scrollTop = messages.scrollHeight;
    }
}