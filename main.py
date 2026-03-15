import math

class RatNum:
    def __init__(self, num, denom=1):
        '''
        @requires: num и denom — целые числа (int) или строки "NaN"
        @modifies: self
        @effects: Создает рациональное число
        @raises: None
        @returns: None
        '''
        self.num = num
        self.denom = denom
        # если знаменатель = 0, значит NaN
        if denom == 0:
            self.num = 0
            self.denom = 0
            return
        # если числитель или знаменатель NaN
        if num == "NaN" or denom == "NaN":
            self.num = 0
            self.denom = 0
            return

        # минус всегда в числителе
        if self.denom < 0:
            self.num = -self.num
            self.denom = -self.denom
        # сокращение дробей
            common = math.gcd(num, denom)
            self.num = num // common
            self.denom = denom // common

    '''Вспомогательные методы'''
    def is_nan(self):
        return self.denom == 0

    def is_positive(self):
        return not self.is_nan() and self.num > 0

    def is_negative(self):
        return not self.is_nan() and self.num < 0

    def compare_to(self, other):
        '''
        @requires: объект RatNum
        @modifies: None
        @effects: Сравнивает два числа
        @raises: None
        @returns: 1, если self > other; -1, если self < other; 0, если они равны.
        '''
        if self.is_nan() and other.is_nan(): return 0
        if self.is_nan(): return 1
        if other.is_nan(): return -1

        v1 = self.num * other.denom
        v2 = other.num * self.denom
        if v1 > v2: return 1
        if v1 < v2: return -1
        return 0

    def float_value(self):
        if self.is_nan():
            raise ValueError("Cannot convert NaN to int")
        return self.num / self.denom

    def int_value(self):
        if self.is_nan():
            raise ValueError("Value is NaN")
        return self.num // self.denom

    '''Клиентские методы'''

    def __neg__(self):
        if self.is_nan():
            return self
        return RatNum(-self.num, self.denom)

    def __add__(self, other):
        '''
        @requires: объект RatNum.
        @modifies: None.
        @effects: Выполняет сложение чисел RatNum
        @raises: None
        @returns: Новый объект RatNum
        '''
        if self.is_nan() or other.is_nan():
            return RatNum(1, 0)
        new_num = self.num * other.denom + other.num * self.denom
        new_denom = self.denom * other.denom
        return RatNum(new_num, new_denom)

    def __sub__(self, other):
        '''
        @requires: объект RatNum
        @modifies: None
        @effects: Выполняет вычитание чисел RatNum
        @raises: None
        @returns: Новый объект RatNum
        '''
        return self + (-other)

    def __mul__(self, other):
        '''@requires: other — объект RatNum
        @modifies: None
        @effects: Выполняет умножение чисел RatNum
        @raises: None
        @returns: Новый объект RatNum
        '''
        if self.is_nan() or other.is_nan():
            return RatNum(1, 0)
        return RatNum(self.num * other.num, self.denom * other.denom)

    def __truediv__(self, other):
        '''@requires:  RatNum
        @modifies: None
        @effects: Выполняет деление чисел RatNum
        @raises: None
        @returns: Новый объект RatNum
        '''
        if self.is_nan() or other.is_nan() or other.num == 0:
            return RatNum(1, 0)
        return RatNum(self.num * other.denom, self.denom * other.num)


    def __str__(self):
        if self.is_nan(): return 'NaN'
        if self.denom == 1: return str(self.num)
        return f"{self.num}/{self.denom}"

    def __hash__(self):
        return hash((self.num, self.denom))

    def __eq__(self, other):
        return self.compare_to(other) == 0

class RatPoly:
    def __init__(self, rn_list=None):
        '''@requires:
        rn_list — список объектов RatNum или None
        @modifies: self.
        @effects: Создает полином. Индекс в списке соответствует степени
        @raises: None
        @returns: None
        '''
        if rn_list is None:
            self.rn_list = [RatNum(0,1)]
        else:
            self.rn_list = list(rn_list)

        while len(rn_list) > 1 and rn_list[-1] == RatNum(0):
            rn_list.pop()

    '''Вспомогательные методы'''

    def degree(self):
        """возвращает степень полинома (длина списка - 1)"""
        if self.is_nan():
            return 0
        return len(self.rn_list) - 1

    def get_coeffs(self, degree):
        if degree < 0 or degree >= len(self.rn_list):
            return RatNum(0,1)
        return self.rn_list[degree]

    def is_nan(self):
        '''если хотя бы один член NaN, весь полином - NaN'''
        for c in self.rn_list:
            if c.is_nan():
                self.rn_list = [RatNum(0, 0)]
                break

    def __add__(self, other):
        '''
        @requires: объект RatPoly
        @modifies: None
        @effects: Вычисляет сумму полиномов
        @raises: None
        @returns: Новый объект RatPoly
        '''
        result = []
        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(1, 0)])
        for i in range(max((len(self.rn_list)),len(other.rn_list))):
            result.append(self.get_coeffs(i) + other.get_coeffs(i))
        return RatPoly(result)

    def __neg__(self):
        neg_list = []
        if self.is_nan():
            return RatPoly([RatNum(1, 0)])
        for rn in self.rn_list:
            neg_list.append(-rn)
        return RatPoly(neg_list)

    def __sub__(self,other):
        '''
        @requires: объект RatPoly
        @modifies: None
        @effects: Вычисляет разность полиномов.
        @raises: None
        @returns: Новый объект RatPoly
        '''
        return self + (-other)

    def __mul__(self,other):
        '''
        @requires: объект RatPoly.
        @modifies: None
        @effects: Вычисляет произведение полиномов
        @raises: None
        @returns: Новый объект RatPoly
        '''
        if self.is_nan() or other.is_nan():
            return RatPoly([RatNum(1, 0)])
        mul_result = [RatNum(0,1) for _ in range (len(self.rn_list) + len(other.rn_list) - 1)]
        for i in range (len(self.rn_list)):
            for j in range (len(other.rn_list)):
                prod = self.rn_list[i] * other.rn_list[j]
                mul_result[i+j] +=  prod
        return RatPoly(mul_result)

    def __truediv__(self, other):
        '''
        @requires: other — объект RatPoly
        @modifies: None
        @effects: Выполняет деление полиномов «уголком».
        @raises: None
        @returns: Новый объект RatPoly
        '''
        if self.is_nan() or other.is_nan() or (len(other.rn_list) == 1 and other.rn_list[0] == RatNum(0)):
            return RatPoly([RatNum(1, 0)])  # Результат деления — NaN

        if self.degree() < other.degree():
            return RatPoly([RatNum(0)])
        remainder = self
        q_coeffs = [RatNum(0)] * (self.degree() - other.degree() + 1)
        while not (len(remainder.rn_list) == 1 and remainder.rn_list[0] == RatNum(0)) \
                and remainder.degree() >= other.degree():
            deg_diff = remainder.degree() - other.degree()
            lead_rem = remainder.rn_list[-1]
            lead_oth = other.rn_list[-1]
            term_coeff = lead_rem / lead_oth
            q_coeffs[deg_diff] = term_coeff
            temp_list = [RatNum(0)] * (deg_diff + 1)
            temp_list[deg_diff] = term_coeff
            term_poly = RatPoly(temp_list)
            remainder = remainder - (term_poly * other)
        return RatPoly(q_coeffs)

    def eval(self,n):
        '''
        @requires: n — объект RatNum
        @modifies: None
        @effects: Вычисляет значение полинома в точке x = n подстановкой степеней.
        @raises: None.
        @returns: Объект RatNum
        '''
        result = RatNum(0)
        exp = RatNum(1)
        for i in range (len(self.rn_list)):
            result += self.rn_list[i] * exp
            exp = exp * n
        return result

    def differentiate(self):
        '''
        @requires: None.
        @modifies: None.
        @effects: Вычисляет производную полинома.
        @raises: None.
        @returns: Новый объект RatPoly.
        '''
        if self.is_nan():
            return RatPoly([RatNum(1, 0)])
        diff_list = []
        for i in range(1,len(self.rn_list)):
            new_coeffs = self.rn_list[i] * RatNum(i)
            diff_list.append(new_coeffs)
        return RatPoly(diff_list)

    def anti_differentiate(self):
        '''
        @requires: None
        @modifies: None
        @effects: Вычисляет первообразную полинома.
        @raises: None.
        @returns: Новый объект RatPoly
        '''
        if self.is_nan():
            return RatPoly([RatNum(1, 0)])
        anti_diff_list =  [RatNum(0)]
        for i in range(1,len(self.rn_list)):
            new_coeffs = self.rn_list[i] / RatNum(i+1)
            anti_diff_list.append(new_coeffs)
        return RatPoly(anti_diff_list)

    def __str__(self):
        '''
        @requires: None
        @modifies: None
        @effects: Формирует строку на вывод.
        @raises: None.
        @returns: Строка (str).'''
        if self.is_nan():
            return "NaN"
        if len(self.rn_list) == 1 and self.rn_list[0] == RatNum(0):
            return "0"

        parts = []
       
        for i in range(len(self.rn_list) - 1, -1, -1):
            coeff = self.rn_list[i]

            if coeff == RatNum(0):
                continue

            s_coeff = str(coeff)

            if i > 0:
                if s_coeff == "1":
                    s_coeff = ""
                elif s_coeff == "-1":
                    s_coeff = "-"

            if i == 0:
                s_x = ""
            elif i == 1:
                s_x = "x"
            else:
                s_x = "x^" + str(i)

            term = s_coeff + s_x

            if parts and not term.startswith("-"):
                parts.append(" + " + term)
            elif parts and term.startswith("-"):
                parts.append(" - " + term[1:]) 
            else:
                parts.append(term)

        return "".join(parts)

    def __hash__(self):
        return hash(tuple(self.rn_list))

    def __eq__(self, other):
        return self.rn_list == other.rn_list



'''unit tests'''

if __name__ == "__main__":
    n1 = RatNum(1, 2)  # 1/2
    n2 = RatNum(1, 3)  # 1/3
    nan_val = RatNum(5, 0)  # NaN

    print(f"{n1} + {n2} = {n1 + n2}")  # 5/6
    print(f"{n1} > {n2} is {n1.compare_to(n2) > 0}")  # True
    print(f"NaN + 1/2 = {nan_val + n1}")  # NaN
    print(f"Is NaN > 1000? {nan_val.compare_to(RatNum(1000)) > 0}")  # True
    
    n1 = RatNum(1, 2)  # 1/2
    n2 = RatNum(1, 3)  # 1/3
    n3 = RatNum(2, 4)  # должно сократиться до 1/2
    nan_val = RatNum(5, 0)  # NaN

    print(f"Сокращение: 2/4 - {n3}")  #  1/2
    print(f"Сложение: {n1} + {n2} = {n1 + n2}")  #  5/6
    print(f"Вычитание: {n1} - {n2} = {n1 - n2}")  #  1/6
    print(f"Умножение: {n1} * {n2} = {n1 * n2}")  #  1/6
    print(f"Деление: {n1} / {n2} = {n1 / n2}")  #  3/2

    print(f"NaN тест: {n1} + NaN = {n1 + nan_val}")  #  NaN
    print(f"Сравнение: {n1} > {n2} это {n1.compare_to(n2) > 0}")  #  True
    print(f"NaN > 1000: {nan_val.compare_to(RatNum(1000)) > 0}")  #  True 
