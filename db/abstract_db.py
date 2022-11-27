from abc import ABC, abstractmethod
from models.contact import Contact


class AbsContactRepo(ABC):
    @abstractmethod
    def insert(self, contact: Contact):
        raise NotImplementedError

    @abstractmethod
    def update(self, id: int, first_name: str, last_name: str, tel: int):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Contact]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> Contact:
        raise NotImplementedError

    @abstractmethod
    def get_by_first_name(self, fist_name: str) -> Contact:
        raise NotImplementedError

    @abstractmethod
    def get_by_last_name(self, last_name: str) -> Contact:
        raise NotImplementedError
