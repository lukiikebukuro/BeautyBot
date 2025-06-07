export function getColor(parameter, value) {
    if (parameter !== 'twardosc') return 'green-dot';
    let numValue = parseFloat(value);
    if (isNaN(numValue)) return 'green-dot';
    if (numValue < 150) return 'green-dot';    // niska
    if (numValue <= 200) return 'orange-dot';  // umiarkowana
    if (numValue <= 250) return 'yellow-dot';  // wysoka
    return 'red-dot';                          // bardzo wysoka
}