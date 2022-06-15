from typing import List, overload


class Notification:

    __messages: dict[str, List[str]] = {}
    __temp: List[str] = []

    def add_message(self, context: str, message: str) -> None:
        if context not in self.__messages:
            self.__messages[context] = []
        self.__messages[context].append(message)
        self.__temp = self.__messages[context]

    def remove_message(self, context: str, message: str) -> None:
        if context in self.__messages and message in self.__messages[context]:
            self.__messages[context].remove(message)
            self.__temp = self.__messages[context]
        return self

    @overload
    def clear(self) -> None:
        ...

    @overload
    def clear(self, context: str) -> None:
        ...

    def clear(self, context: str = None) -> None:
        if context is None:
            self.__messages = {}
        elif context in self.__messages:
            del self.__messages[context]
        self.__temp = []

    @property
    def messages(self) -> dict[str, List[str]]:
        return self.__messages

    def messages_filter(self, context: str) -> 'Notification':
        self.__temp = self.__messages[context] if context in self.__messages else []
        return self

    def to_list(self) -> List[str]:
        return self.__temp

    def to_str(self, separator: str = '\n', end: str = '') -> str:
        return separator.join(self.__temp) + end
