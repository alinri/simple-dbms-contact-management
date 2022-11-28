from db.file_db import ContactRepo
from models.contact import Contact
from pathlib import Path


def add_contact(db: ContactRepo):
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = int(input("Enter phone number: "))
    contact = Contact(first_name, last_name, phone)
    db.insert(contact)


def print_contact(contact: Contact):
    print(
        f"id: {contact.id}, first name: {contact.first_name}, "
        f"last name: {contact.last_name}, phone: {contact.tel}"
    )


def list_contacts(db: ContactRepo):
    contacts = db.list()
    for contact in contacts:
        print_contact(contact)


def search_contact_by_first_name(db: ContactRepo):
    first_name = input("Enter first name: ")
    contact = db.get_by_first_name(first_name)
    if not contact:
        print("No contact found")
        return
    print_contact(contact)


def search_contact_by_last_name(db: ContactRepo):
    last_name = input("Enter last name: ")
    contact = db.get_by_last_name(last_name)
    if not contact:
        print("No contact found")
        return
    print_contact(contact)


def search_contact_by_tel(db: ContactRepo):
    tel = int(input("Enter tel: "))
    contact = db.get_by_tel(tel)
    if not contact:
        print("No contact found")
        return
    print_contact(contact)


def get_contact_by_id(db: ContactRepo):
    contact_id = int(input("Enter contact id: "))
    contact = db.get_by_id(contact_id)
    if not contact:
        print("No contact found")
        return
    print_contact(contact)


def delete_contact(db: ContactRepo):
    contact_id = int(input("Enter contact id: "))
    db.delete(contact_id)


def main():
    db = ContactRepo(Path("mydb.db"))
    while True:
        print("1. Add Contact")
        print("2. List contacts")
        print("3. Search Contact By First Name")
        print("4. Search Contact By Last Name")
        print("5. Search Contact By Tel")
        print("6. Get Contact By id")
        print("7. Delete Contact")
        print("8. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_contact(db)
        elif choice == 2:
            list_contacts(db)
        elif choice == 3:
            search_contact_by_first_name(db)
        elif choice == 4:
            search_contact_by_last_name(db)
        elif choice == 5:
            search_contact_by_tel(db)
        elif choice == 6:
            get_contact_by_id(db)
        elif choice == 7:
            delete_contact(db)
        elif choice == 8:
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
