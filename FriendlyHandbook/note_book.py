import os
import pickle
from collections import UserDict
from abc import ABC, abstractmethod

SAVE_FILENAME = "notebook.pkl"


class FieldNotebook:
    def __init__(self, value):
        self.value = value


class Tag(FieldNotebook):
    def eq(self, other):
        return isinstance(other, Tag) and self.value == other.value


class Name(FieldNotebook):
    pass


class Record:
    def __init__(self, name: Name, tags: list, text: str):
        self.name = name
        self.tags = [Tag(tag) for tag in tags]
        self.text = text

    def add_tag(self, tag):
        hashtag = Tag(tag)
        if hashtag not in self.tags:
            self.tags.append(hashtag)

    def find_tag(self, value):
        for tag in self.tags:
            if tag.value == value:
                return tag
        return None

    def delete_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def edit_text(self, new_text):
        self.text = new_text


class Notebook(UserDict):
    def __init__(self, user_interface):
        super().__init__()
        self.ui = user_interface

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def save_to_file(self):
        with open(SAVE_FILENAME, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        if os.path.exists(SAVE_FILENAME):
            try:
                with open(SAVE_FILENAME, "rb") as file:
                    self.data = pickle.load(file)
            except FileNotFoundError:
                self.ui.display_message(f"File '{SAVE_FILENAME}' not found.")
        else:
            self.ui.display_message(f"File '{SAVE_FILENAME}' does not exist. Data not loaded.")

    def find_record(self, value):
        return self.data.get(value)

    def edit_record(self, name, new_tags, new_text):
        if name in self.data:
            record = self.data[name]
            record.tags = [Tag(tag) for tag in new_tags]
            record.text = new_text
            self.data[name] = record
            self.ui.display_message(f"Note {name} has been edited.")
        else:
            self.ui.display_message(f"Note '{name}' not found.")

    def search_by_tag(self, tag):
        matching_records = []
        for record in self.data.values():
            if any(tag == t.value for t in record.tags):
                matching_records.append(record)
        return matching_records

    def run_notebook(self):
        while True:
            self.ui.display_message("\nOptions:")
            self.ui.display_message("1. Add a note")
            self.ui.display_message("2. Find a note by name")
            self.ui.display_message("3. Search by tag")
            self.ui.display_message("4. Show all notes")
            self.ui.display_message("5. Edit a note")
            self.ui.display_message("6. Edit note text")
            self.ui.display_message("7. Edit note tags")
            self.ui.display_message("8. Delete a note")
            self.ui.display_message("9. Add tags to a note")
            self.ui.display_message("0. Exit notebook")

            choice = self.ui.get_user_input("Select an option: ").strip()

            if choice == "1" or choice.lower() == "add note":
                name = self.ui.get_user_input("Enter the name of the note: ")
                hashtags = self.ui.get_user_input("Enter tags for the note (if multiple, separate by comma): ").split(", ")
                text = self.ui.get_user_input("Enter the text of the note: ")

                name_field = Name(name.strip())
                record = Record(name_field, hashtags, text)
                self.add_record(record)
                self.ui.display_message(f"Note {name} has been added to the notebook.")

            elif choice == "2" or choice.lower() == "find note":
                search_term = self.ui.get_user_input("Enter the name of the note to find: ")
                record = self.find_record(search_term)
                if record:
                    self.ui.display_message(f"Name: {record.name.value}")
                    self.ui.display_message("Tags:")
                    for tag in record.tags:
                        self.ui.display_message(tag.value)
                    self.ui.display_message("Text:")
                    self.ui.display_message(record.text)
                else:
                    self.ui.display_message(f"Note with name '{search_term}' not found.")

            elif choice == "3" or choice.lower() == "search by tag":
                tag_to_search = self.ui.get_user_input("Enter the tag for searching: ")
                matching_records = self.search_by_tag(tag_to_search)
                if matching_records:
                    self.ui.display_message("Matching Records:")
                    for record in matching_records:
                        self.ui.display_message(f"Name: {record.name.value}")
                        self.ui.display_message("Tags:")
                        for tag in record.tags:
                            self.ui.display_message(tag.value)
                        self.ui.display_message("Text:")
                        self.ui.display_message(record.text)
                else:
                    self.ui.display_message(f"No notes found with tag '{tag_to_search}'.")

            elif choice == "4" or choice.lower() == "show all notes":
                self.ui.display_message("List of all notes:")
                for name, record in self.data.items():
                    self.ui.display_message(f"Name: {record.name.value}")
                    for tag in record.tags:
                        self.ui.display_message(f"Tags: {tag.value}")
                    self.ui.display_message(f"Text: {record.text}")

            elif choice == "5" or choice.lower() == "edit a note":
                edit_name = self.ui.get_user_input("Enter the name of the note to edit: ")
                new_tags = self.ui.get_user_input("Enter new tags (if multiple, separate by comma): ").split(", ")
                new_text = self.ui.get_user_input("Enter new text for the note: ")
                self.edit_record(edit_name.strip(), new_tags, new_text)

            elif choice == "6" or choice.lower() == "edit note text":
                edit_name = self.ui.get_user_input("Enter the name of the note to edit text: ")
                record = self.find_record(edit_name.strip())
                if record:
                    new_text = self.ui.get_user_input("Enter new text: ")
                    record.edit_text(new_text)
                    self.ui.display_message(f"Text of note {edit_name} has been changed.")
                else:
                    self.ui.display_message(f"Note with name '{edit_name}' not found.")

            elif choice == "7" or choice.lower() == "edit note tags":
                edit_tags_name = self.ui.get_user_input("Enter the name of the note to edit tags: ")
                record = self.find_record(edit_tags_name.strip())
                if record:
                    new_tags = self.ui.get_user_input("Enter new tags (if multiple, separate by comma): ").split(", ")
                    record.tags = [Tag(tag.strip()) for tag in new_tags]
                    self.ui.display_message(f"Tags of note {edit_tags_name} have been changed.")
                else:
                    self.ui.display_message(f"Note with name '{edit_tags_name}' not found.")

            elif choice == "8" or choice.lower() == "delete a note":
                delete_term = self.ui.get_user_input("Enter the name of the note to delete: ")
                record = self.find_record(delete_term)
                if record:
                    del self.data[delete_term]
                    self.ui.display_message(f"Note {delete_term} has been deleted from the notebook.")
                else:
                    self.ui.display_message(f"Note with name '{delete_term}' not found.")

            elif choice == "9" or choice.lower() == "add tags to a note":
                edit_tags_name = self.ui.get_user_input("Enter the name of the note to add tags: ")
                record = self.find_record(edit_tags_name)
                if record:
                    new_tags = self.ui.get_user_input("Enter new tags (if multiple, separate by comma): ").split(", ")
                    for tag in new_tags:
                        record.add_tag(tag.strip())
                    self.ui.display_message(f"Tags have been added to note {edit_tags_name}.")
                else:
                    self.ui.display_message(f"Note with name '{edit_tags_name}' not found.")

            elif choice == "0" or choice.lower() == "exit notebook":
                self.save_to_file()
                self.ui.display_message(f"Data saved to file '{SAVE_FILENAME}'.")
                self.ui.display_message("Goodbye!")
                break

            else:
                self.ui.display_message("Invalid choice. Please select a valid option.")

            self.ui.get_user_input("Press Enter to continue.")


class UserInterface(ABC):
    @abstractmethod
    def display_options(self):
        pass

    @abstractmethod
    def get_user_input(self, prompt):
        pass

    @abstractmethod
    def display_message(self, message):
        pass


class ConsoleInterface(UserInterface):
    def display_options(self):
        print("\nOptions:")
        print("1. Add a note")
        print("2. Find a note by name")
        print("3. Search by tag")
        print("4. Show all notes")
        print("5. Edit a note")
        print("6. Edit note text")
        print("7. Edit note tags")
        print("8. Delete a note")
        print("9. Add tags to a note")
        print("0. Exit notebook")

    def get_user_input(self, prompt):
        return input(prompt)

    def display_message(self, message):
        print(message)


def run_notebook():
    console_interface = ConsoleInterface()
    note_book = Notebook(console_interface)
    note_book.load_from_file()
    note_book.run_notebook()


if __name__ == "__main__":
    run_notebook()


# Kovaleno Oleksandr 
# Абстрактний клас UserInterface і клас ConsoleInterface. 
# Клас Notebook тепер приймає екземпляр UserInterface, що дозволяє легко розширювати його до інших типів інтерфейсів. 
# Функція run_notebook ініціалізує ConsoleInterface і використовує його для взаємодії з користувачем. 
