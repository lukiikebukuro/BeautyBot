function getColor(parameter, value) {
    if (parameter !== 'twardosc') return 'green-dot';
    let numValue = parseFloat(value);
    if (isNaN(numValue)) return 'green-dot';
    if (numValue < 150) return 'green-dot';
    if (numValue <= 200) return 'orange-dot';
    if (numValue <= 250) return 'yellow-dot';
    return 'red-dot';
}
// Ekspozycja na globalny obiekt window
window.utilis = { getColor };