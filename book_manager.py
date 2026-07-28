import os

class Entity:
    """საბაზო კლასი მემკვიდრეობისა და პოლიმორფიზმის სადემონსტრაციოდ"""
    def get_info(self) -> str:
        return "Generic entity info"


class Book(Entity):
    """Book კლასი - წარმოადგენს თითოეულ წიგნს"""
    def __init__(self, title: str, author: str, year: int):
        self.__title = title      # ინკაფსულაცია (პირადი ატრიბუტები)
        self.__author = author
        self.__year = year

    # Getters
    def get_title(self) -> str:
        return self.__title

    def get_author(self) -> str:
        return self.__author

    def get_year(self) -> int:
        return self.__year

    # პოლიმორფიზმი - მშობლიური კლასის მეთოდის გადაფარვა (Override)
    def get_info(self) -> str:
        return f"სათაური: {self.__title} | ავტორი: {self.__author} | გამოცემის წელი: {self.__year}"


class BookManager:
    """BookManager კლასი წიგნების სიისა და ფაილური ოპერაციების სამართავად"""
    def __init__(self, filename: str = "books.txt"):
        self.__filename = filename
        self.__books = []
        self.load_from_file()

    def add_book(self, book: Book) -> None:
        """ახალი წიგნის დამატება სიაში და ფაილში შენახვა"""
        self.__books.append(book)
        self.save_to_file()
        print("წიგნი წარმატებით დაემატა.")

    def display_all_books(self) -> None:
        """ყველა წიგნის სიის ჩვენება"""
        print("\n--- წიგნების სრული სია ---")
        if not self.__books:
            print("სია ცარიელია. წიგნები ჯერ არ არის დამატებული.")
            return

        for index, book in enumerate(self.__books, start=1):
            print(f"{index}. {book.get_info()}")

    def search_by_title(self, search_title: str) -> None:
        """წიგნის ძებნა სათაურის მიხედვით"""
        search_title_clean = search_title.strip().lower()
        found_books = [
            b for b in self.__books 
            if search_title_clean in b.get_title().lower()
        ]

        print(f"\n--- ძებნის შედეგები სიტყვისთვის: '{search_title}' ---")
        if not found_books:
            print("მითითებული სათაურით წიგნი ვერ მოიძებნა.")
            return

        for book in found_books:
            print(book.get_info())

    def save_to_file(self) -> None:
        """მონაცემების ჩაწერა ფაილში"""
        with open(self.__filename, "w", encoding="utf-8") as f:
            for book in self.__books:
                f.write(f"{book.get_title()};{book.get_author()};{book.get_year()}\n")

    def load_from_file(self) -> None:
        """მონაცემების წაკითხვა ფაილიდან"""
        if not os.path.exists(self.__filename):
            return

        self.__books = []
        with open(self.__filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 3:
                    title, author, year_str = parts
                    try:
                        year = int(year_str)
                        self.__books.append(Book(title, author, year))
                    except ValueError:
                        continue


# ვალიდაციის დამხმარე ფუნქციები
def get_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("შეცდომა: ტექსტი არ უნდა იყოს ცარიელი! სცადეთ თავიდან.")

def get_valid_year(prompt: str) -> int:
    while True:
        try:
            year = int(input(prompt).strip())
            if 0 < year <= 2026:
                return year
            print("შეცდომა: შეიყვანეთ რეალური წელი (1-დან 2026-მდე)!")
        except ValueError:
            print("შეცდომა: გთხოვთ შეიყვანოთ მხოლოდ მთელი რიცხვი!")


def main():
    manager = BookManager()

    while True:
        print("\n=== წიგნების მართვის სისტემა ===")
        print("1. ახალი წიგნის დამატება")
        print("2. ყველა წიგნის სიის ნახვა")
        print("3. წიგნის ძებნა სათაურით")
        print("4. გასვლა")

        choice = input("აირჩიეთ ოპერაცია (1-4): ").strip()

        if choice == "1":
            print("\n--- ახალი წიგნის დამატება ---")
            title = get_non_empty_string("შეიყვანეთ წიგნის სათაური: ")
            author = get_non_empty_string("შეიყვანეთ ავტორი: ")
            year = get_valid_year("შეიყვანეთ გამოცემის წელი: ")

            new_book = Book(title, author, year)
            manager.add_book(new_book)

        elif choice == "2":
            manager.display_all_books()

        elif choice == "3":
            print("\n--- წიგნის ძებნა ---")
            search_title = get_non_empty_string("შეიყვანეთ წიგნის სათაური (ან ნაწილი): ")
            manager.search_by_title(search_title)

        elif choice == "4":
            print("პროგრამა დასრულებულია. ნახვამდის!")
            break

        else:
            print("შეცდომა: არასწორი არჩევანი, გთხოვთ აირჩიოთ 1-დან 4-მდე!")

if __name__ == "__main__":
    main()