from .abstract_db import AbsContactRepo
from models.contact import Contact
from pathlib import Path
import os


class ContactRepo(AbsContactRepo):
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        db_path.touch(exist_ok=True)

    def _contact_to_bytes(self, contact: Contact) -> bytes:
        f_name_bytes = (
            contact.first_name + (15 - len(contact.first_name)) * " "
        ).encode("utf-8")
        l_name_bytes = (
            contact.last_name
            + (
                25
                - len(
                    contact.last_name,
                )
            )
            * " "
        ).encode(
            "utf-8",
        )
        tel_bytes = contact.tel.to_bytes(8, "big")
        return f_name_bytes + l_name_bytes + tel_bytes

    def _bytes_to_contact(self, id: int, contact_bytes: bytes) -> Contact:
        f_name = contact_bytes[0:15].decode("utf-8").strip()
        l_name = contact_bytes[15:40].decode("utf-8").strip()
        tel = int.from_bytes(contact_bytes[40:48], "big")
        return Contact(
            f_name,
            l_name,
            tel,
            id,
        )

    def _validate_first_name(self, f_name: str):
        if len(f_name) > 15:
            raise ValueError(
                "First name length must be less than 15 characters",
            )

    def _validate_last_name(self, l_name: str):
        if len(l_name) > 25:
            raise ValueError(
                "Last name length must be less than 25 characters",
            )

    def _validate_tell(self, tel: int):
        if tel > 9223372036854775807:
            raise ValueError(
                "Phone number must be less than 9223372036854775807",
            )

    def _validate_contact(self, contact: Contact):
        self._validate_first_name(contact.first_name)
        self._validate_last_name(contact.last_name)
        self._validate_tell(contact.tel)

    def insert(self, contact: Contact):
        with self.db_path.open("ab") as f:
            f.write(self._contact_to_bytes(contact))

    def update(
        self,
        id: int,
        first_name: str = None,
        last_name: str = None,
        tel: int = None,
    ):
        pass

    def delete(self, id: int):
        id = id - 1
        contacts_byte_length = os.stat(self.db_path.absolute()).st_size
        deleted_contact_offset = id * 48
        if deleted_contact_offset >= contacts_byte_length:
            raise IndexError
        last_contact_offset = deleted_contact_offset
        with self.db_path.open("rb+") as f:
            for current_contact_offset in range(
                deleted_contact_offset + 48,
                contacts_byte_length,
                48,
            ):
                f.seek(current_contact_offset)
                current_contact_bytes = f.read(48)
                f.seek(last_contact_offset)
                f.write(current_contact_bytes)
                last_contact_offset = current_contact_offset
            f.seek(contacts_byte_length - 48)
            f.truncate()

    def list(self) -> list[Contact]:
        contacts = []
        with self.db_path.open("rb") as f:
            contacts_bytes = f.read()
            for offset in range(0, len(contacts_bytes), 48):
                contacts.append(
                    self._bytes_to_contact(
                        offset // 48 + 1,
                        contacts_bytes[offset : offset + 48],
                    )
                )
        return contacts

    def get_by_first_name(self, fist_name: str) -> Contact:
        pass

    def get_by_last_name(self, last_name: str) -> Contact:
        pass

    def get_by_id(self, id: int) -> Contact:
        offset = (id - 1) * 48
        if os.stat(self.db_path.absolute()).st_size <= offset:
            raise IndexError
        with self.db_path.open("rb") as f:
            f.seek(offset)
            return self._bytes_to_contact(id, f.read(48))
