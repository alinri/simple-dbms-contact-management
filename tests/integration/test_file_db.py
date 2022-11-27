import pytest
from db.file_db import ContactRepo
from tempfile import TemporaryDirectory
from models.contact import Contact
from pathlib import Path


@pytest.fixture
def db_file_path():
    with TemporaryDirectory() as db_folder:
        yield Path(db_folder) / "my_db.db"


@pytest.fixture
def contact_repo(db_file_path: Path) -> ContactRepo:
    return ContactRepo(db_file_path)


def test_create_db_file(contact_repo: ContactRepo, db_file_path: Path):
    assert db_file_path.exists()
    print(db_file_path)


def test_create_db_not_overright_db(
    contact_repo: ContactRepo,
    db_file_path: Path,
):
    contact = Contact("ali", "noori", 98253792538)
    contact_repo.insert(
        contact,
    )
    new_repo = ContactRepo(db_file_path)
    assert new_repo.get_by_id(1) == contact


def test_insert_person(contact_repo: ContactRepo, db_file_path: Path):
    contact = Contact(
        "ali",
        "noori",
        9012498019,
    )
    contact_repo.insert(contact)
    with open(db_file_path, "rb") as f:
        assert f.read(15) == "ali            ".encode("utf-8")
        assert f.read(25) == "noori                    ".encode("utf-8")
        assert f.read(8) == contact.tel.to_bytes(8, "big")


def test_insert_at_end(contact_repo: ContactRepo, db_file_path: Path):
    contact1 = Contact(
        "ali",
        "noori",
        9012498019,
    )
    contact2 = Contact(
        "ali2",
        "noori2",
        9012423452,
    )
    contact_repo.insert(contact1)
    contact_repo.insert(contact2)
    with open(db_file_path, "rb") as f:
        f.seek(48)
        assert f.read(15) == "ali2           ".encode("utf-8")
        assert f.read(25) == "noori2                   ".encode("utf-8")
        assert f.read(8) == contact2.tel.to_bytes(8, "big")


def test_select_by_id(contact_repo: ContactRepo):
    contact1 = Contact(
        "ali",
        "noori",
        9012498019,
    )
    contact2 = Contact(
        "ali2",
        "noori2",
        9012423452,
    )
    contact3 = Contact(
        "ali3",
        "noori3",
        9012423344,
    )
    contact_repo.insert(contact1)
    contact_repo.insert(contact2)
    contact_repo.insert(contact3)

    db_contact = contact_repo.get_by_id(2)
    assert db_contact == contact2
    assert db_contact.id == 2


def test_select_by_id_first(contact_repo: ContactRepo):
    contact1 = Contact(
        "ali",
        "noori",
        9012498019,
    )
    contact2 = Contact(
        "ali2",
        "noori2",
        9012423452,
    )
    contact3 = Contact(
        "ali3",
        "noori3",
        9012423344,
    )
    contact_repo.insert(contact1)
    contact_repo.insert(contact2)
    contact_repo.insert(contact3)

    db_contact = contact_repo.get_by_id(1)
    assert db_contact == contact1
    assert db_contact.id == 1


def test_select_by_id_last(contact_repo: ContactRepo):
    contact1 = Contact(
        "ali",
        "noori",
        9012498019,
    )
    contact2 = Contact(
        "ali2",
        "noori2",
        9012423452,
    )
    contact3 = Contact(
        "ali3",
        "noori3",
        9012423344,
    )
    contact_repo.insert(contact1)
    contact_repo.insert(contact2)
    contact_repo.insert(contact3)

    db_contact = contact_repo.get_by_id(3)
    assert db_contact == contact3
    assert db_contact.id == 3


def test_contact_list(contact_repo: ContactRepo):
    contact1 = Contact(
        "ali",
        "noori",
        9012498019,
    )
    contact2 = Contact(
        "ali2",
        "noori2",
        9012423452,
    )
    contact3 = Contact(
        "ali3",
        "noori3",
        9012423344,
    )
    contact_repo.insert(contact1)
    contact_repo.insert(contact2)
    contact_repo.insert(contact3)

    assert contact_repo.list() == [
        contact1,
        contact2,
        contact3,
    ]
