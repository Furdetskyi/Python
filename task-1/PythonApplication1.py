def roman_to_int(s: str) -> int:
    # Відображення римських чисел у відповідні значення
    roman_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000
    }

    # Змінна для збереження результату
    total = 0

    # Проходимо по кожному символу у рядку
    for i in range(len(s)):
        # Якщо поточне значення менше наступного, віднімаємо його
        if i + 1 < len(s) and roman_map[s[i]] < roman_map[s[i + 1]]:
            total -= roman_map[s[i]]
        else:
            total += roman_map[s[i]]
    
    return total

# Приклади використання
print(roman_to_int("III"))     
print(roman_to_int("LVIII"))   
print(roman_to_int("MCMXCIV")) 
