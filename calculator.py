import os

class BaseOperation:
    """აბსტრაქტული ბაზისური კლასი ოპერაციებისთვის (პოლიმორფიზმისა და მემკვიდრეობისთვის)"""
    def calculate(self, num1: float, num2: float) -> float:
        raise NotImplementedError("შვილეულმა კლასმა უნდა განახორციელოს ეს მეთოდი.")

class Addition(BaseOperation):
    """მიმატების ოპერაცია"""
    def calculate(self, num1: float, num2: float) -> float:
        return num1 + num2

class Subtraction(BaseOperation):
    """გამოკლების ოპერაცია"""
    def calculate(self, num1: float, num2: float) -> float:
        return num1 - num2

class Multiplication(BaseOperation):
    """გამრავლების ოპერაცია"""
    def calculate(self, num1: float, num2: float) -> float:
        return num1 * num2

class Division(BaseOperation):
    """გაყოფის ოპერაცია შეცდომის დამუშავებით"""
    def calculate(self, num1: float, num2: float) -> float:
        if num2 == 0:
            raise ZeroDivisionError("ნულზე გაყოფა შეუძლებელია!")
        return num1 / num2


class Calculator:
    """კალკულატორის მთავარი კლასი, რომელიც მართავს ლოგიკასა და ფაილებთან მუშაობას"""
    def __init__(self, history_file: str = "history.txt"):
        self.__history_file = history_file  # ინკაფსულაცია (ინკაფსულირებული ატრიბუტი)
        # ლოგიკური რუკა ოპერაციების დასაკავშირებლად
        self.operations = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division()
        }

    def save_to_history(self, record: str) -> None:
        """ჩანაწერის შენახვა ფაილში"""
        with open(self.__history_file, "a", encoding="utf-8") as f:
            f.write(record + "\n")

    def read_history(self) -> list:
        """ისტორიის წაკითხვა ფაილიდან"""
        if not os.path.exists(self.__history_file):
            return []
        with open(self.__history_file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def clear_history(self) -> None:
        """ისტორიის ფაილის წაშლა/გასუფთავება"""
        if os.path.exists(self.__history_file):
            os.remove(self.__history_file)


def get_float_input(prompt: str) -> float:
    """მომხმარებლისგან ვალიდური რიცხვის მიღების ფუნქცია"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(" შეცდომა: გთხოვთ შეიყვანოთ ვალიდური რიცხვი!")


def main():
    calc = Calculator()

    while True:
        print("\n===  კალკულატორი ===")
        print("1. გამოთვლის შესრულება")
        print("2. ისტორიის ნახვა")
        print("3. ისტორიის წაშლა")
        print("4. გასვლა")

        choice = input("აირჩიეთ ოპერაცია (1-4): ").strip()

        if choice == "1":
            num1 = get_float_input("შეიყვანეთ პირველი რიცხვი: ")
            op_symbol = input("შეიყვანეთ ოპერატორი (+, -, *, /): ").strip()

            if op_symbol not in calc.operations:
                print(" არასწორი ოპერატორი!")
                continue

            num2 = get_float_input("შეიყვანეთ მეორე რიცხვი: ")

            try:
                operation = calc.operations[op_symbol]
                result = operation.calculate(num1, num2)
                record = f"{num1} {op_symbol} {num2} = {result}"
                print(f" შედეგი: {result}")
                calc.save_to_history(record)
            except ZeroDivisionError as e:
                print(f" {e}")

        elif choice == "2":
            history = calc.read_history()
            print("\n---  გამოთვლების ისტორია ---")
            if not history:
                print("ისტორია ცარიელია.")
            else:
                for line in history:
                    print(line)

        elif choice == "3":
            calc.clear_history()
            print(" ისტორია წარმატებით წაიშალა!")

        elif choice == "4":
            print("გმადლობთ კალკულატორით სარგებლობისთვის! ")
            break
        else:
            print(" არასწორი არჩევანი, სცადეთ თავიდან.")

if __name__ == "__main__":
    main()