class Books:
    def __init__(self, title, author, isbn, available_copies):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._available_copies = available_copies

    # Getter methods
    def get_title(self) -> str:
        return self._title

    def get_author(self) -> str:
        return self._author

    def get_isbn(self) -> str:
        return self._isbn

    def get_available_copies(self) -> int:
        return self._available_copies

    # Setter methods
    def set_title(self, title: str) -> None:
        self._title = title

    def set_author(self, author: str) -> None:
        self._author = author

    def set_isbn(self, isbn: str) -> None:
        self._isbn = isbn

    def set_available_copies(self, available_copies: int) -> None:
        self._available_copies = available_copies

    # Additional method with function return type
    def borrow_book(self, num_copies: int) -> bool:
        if num_copies > 0 and num_copies <= self._available_copies:
            self._available_copies -= num_copies
            return True
        else:
            return False

    # Additional method with function return type
    def return_book(self, num_copies: int) -> None:
        self._available_copies += num_copies

