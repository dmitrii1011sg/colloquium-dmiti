from core.base.Integer import Integer
from core.base.Natural import Natural

# Жуков Александр 5381


class Rational:
    """
    Модель рационального числа.

    Хранится в виде дроби numer / denom, где знак числа несёт числитель.

    Attributes:
        numer (Integer): Числитель (целое число со знаком).
        denom (Natural): Знаменатель (натуральное число, не равное нулю).
    """

    __slots__ = ("numer", "denom")

    def __init__(self, numer: Integer, denom: Natural) -> None:
        """
        Инициализация рационального числа.

        Args:
            numer (Integer): Числитель.
            denom (Natural): Знаменатель (не равен нулю).

        Raises:
            ValueError: Параметры не соответствуют типам или знаменатель равен нулю.
        """
        if not isinstance(numer, Integer) or not isinstance(denom, Natural):
            raise ValueError("Invalid value")

        if denom.length == 1 and denom.digits[0] == 0:
            raise ValueError("Denominator must not be zero")

        self.numer: Integer = numer
        self.denom: Natural = denom

    def is_zero(self) -> bool:
        return self.numer.is_zero()

    @classmethod
    def from_str(cls, value: str) -> "Rational":
        """
        Создание рационального числа из строки.

        Поддерживаемые форматы:
            "3/4", "-3/4", "+3/4" — дробь;
            "5", "-5", "+5"       — целое (знаменатель = 1).

        Args:
            value (str): Строковое представление дроби.

        Raises:
            ValueError: Параметры не соответствуют типам или значениям.

        Returns:
            Rational: Рациональное число.
        """
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Invalid value")

        if "/" in value:
            parts = value.split("/")
            if len(parts) != 2:
                raise ValueError("Invalid value")
            numer_str, denom_str = parts[0], parts[1]
        else:
            numer_str, denom_str = value, "1"

        numer = Integer.from_str(numer_str)
        denom = Natural.from_str(denom_str)

        return cls(numer, denom)

    def __str__(self) -> str:
        """
        Строковое представление рационального числа.

        Returns:
            str: Число в виде "numer/denom" или "numer", если знаменатель равен 1.
        """
        if self.denom.length == 1 and self.denom.digits[0] == 1:
            return f"{self.numer}"
        return f"{self.numer}/{self.denom}"

    def __repr__(self) -> str:
        """
        Отладочное представление.

        Returns:
            str: Строка вида "Rational(3/4)".
        """
        return f"Rational({self})"
