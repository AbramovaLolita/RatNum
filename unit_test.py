
    print("\n--- Тестируем RatPoly ---")
    # Создадим p1 = 1 + x (записываем как [1, 1])
    p1 = RatPoly([RatNum(1), RatNum(1)])
    # Создадим p2 = 1 - x (записываем как [1, -1])
    p2 = RatPoly([RatNum(1), RatNum(-1)])

    print(f"Полином 1: {p1}")
    print(f"Полином 2: {p2}")

    # Тест сложения: (1+x) + (1-x) = 2
    p_sum = p1 + p2
    print(f"Сложение: ({p1}) + ({p2}) = {p_sum}")  # Должно быть 2

    # Тест вычитания и "очистки нулей": (1+x) - x = 1
    only_x = RatPoly([RatNum(0), RatNum(1)])
    p_sub = p1 - only_x
    print(f"Вычитание (очистка): ({p1}) - x = {p_sub}")  # Должно быть 1, степень 0

    # Тест умножения: (1+x)(1-x) = 1 - x^2
    p_mul = p1 * p2
    print(f"Умножение: ({p1}) * ({p2}) = {p_mul}")  # Ожидаем 1 - x^2

    # Тест производной: (x^2 + 5x + 10)' = 2x + 5
    p_der = RatPoly([RatNum(10), RatNum(5), RatNum(1)])
    print(f"Производная: ({p_der})' = {p_der.differentiate()}")

    # Тест интеграла: (2x + 5) -> x^2 + 5x (константа 0)
    p_to_int = RatPoly([RatNum(5), RatNum(2)])
    print(f"Интеграл: ({p_to_int}) = {p_to_int.anti_differentiate()}")

    # Тест значения: подставим x=3 в (1 + x)
    val = p1.eval(RatNum(3))
    print(f"Значение {p1} при x=3: {val}")  # Ожидаем 4

    # Финальный босс: Деление (x^2 - 1) / (x - 1)
    # p_mul у нас как раз x^2 - 1 (точнее 1 - x^2, так что делим на 1 - x)
    p_div_res = p_mul / p2
    print(f"Деление: ({p_mul}) / ({p2}) = {p_div_res}")  # Ожидаем 1 + x
