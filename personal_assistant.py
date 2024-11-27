import os
import json
import datetime
import csv


NOTES_FILE = "notes.json"
TASKS_FILE = "tasks.json"
CONTACTS_FILE = "contacts.json"
FINANCE_FILE = "finance.json"


def load_data(file_path, default_data):
    if not os.path.exists(file_path):
        save_data(file_path, default_data)
        return default_data
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


class Note:
    def __init__(self, note_id, title, content, timestamp):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp


class NoteManager:
    def __init__(self):
        self.notes = []
        self.load_notes()

    def load_notes(self):
        data = load_data(NOTES_FILE, [])
        self.notes = [Note(**note) for note in data]

    def save_notes(self):
        data = [note.__dict__ for note in self.notes]
        save_data(NOTES_FILE, data)

    def add_note(self, title, content):
        note_id = max([note.id for note in self.notes], default=0) + 1
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_note = Note(note_id, title, content, timestamp)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена!")

    def list_notes(self):
        if not self.notes:
            print("Список заметок пуст.")
            return
        for note in self.notes:
            print(f"{note.id}. {note.title} (дата: {note.timestamp})")

    def view_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            print(f"Заголовок: {note.title}")
            print(f"Содержимое: {note.content}")
            print(f"Дата создания/изменения: {note.timestamp}")
        else:
            print("Заметка не найдена.")

    def edit_note(self, note_id, new_title, new_content):
        note = self.get_note_by_id(note_id)
        if note:
            note.title = new_title
            note.content = new_content
            note.timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.save_notes()
            print("Заметка успешно обновлена!")
        else:
            print("Заметка не найдена.")

    def delete_note(self, note_id):
        note = self.get_note_by_id(note_id)
        if note:
            self.notes.remove(note)
            self.save_notes()
            print("Заметка успешно удалена!")
        else:
            print("Заметка не найдена.")

    def get_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def export_notes_to_csv(self):
        if not self.notes:
            print("Список заметок пуст.")
            return
        fname = "notes_export.csv"
        with open(fname, mode="w", encoding="utf-8", newline="") as csv_file:
            fieldnames = ["ID", "Заголовок", "Содержимое", "Дата"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for note in self.notes:
                writer.writerow(
                    {
                        "ID": note.id,
                        "Заголовок": note.title,
                        "Содержимое": note.content,
                        "Дата": note.timestamp,
                    }
                )
        print(f"Заметки успешно экспортированы в файл {fname}")

    def import_notes_from_csv(self):
        fname = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(fname):
            print("Файл не найден.")
            return
        with open(fname, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                note_id = max([note.id for note in self.notes], default=0) + 1
                title = row.get("Заголовок", "")
                content = row.get("Содержимое", "")
                timestamp = row.get(
                    "Дата", datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                )
                new_note = Note(note_id, title, content, timestamp)
                self.notes.append(new_note)
            self.save_notes()
        print("Заметки успешно импортированы из CSV-файла.")


def notes_menu():
    manager = NoteManager()
    while True:
        print("\nУправление заметками:")
        print("1. Добавить новую заметку")
        print("2. Просмотреть список заметок")
        print("3. Просмотреть заметку")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Экспорт заметок в CSV")
        print("7. Импорт заметок из CSV")
        print("8. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            manager.add_note(title, content)
        elif choice == "2":
            manager.list_notes()
        elif choice == "3":
            try:
                note_id = int(input("Введите ID заметки: "))
                manager.view_note(note_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "4":
            try:
                note_id = int(input("Введите ID заметки: "))
                new_title = input("Введите новый заголовок заметки: ")
                new_content = input("Введите новое содержимое заметки: ")
                manager.edit_note(note_id, new_title, new_content)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "5":
            try:
                note_id = int(input("Введите ID заметки: "))
                manager.delete_note(note_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "6":
            manager.export_notes_to_csv()
        elif choice == "7":
            manager.import_notes_from_csv()
        elif choice == "8":
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")
