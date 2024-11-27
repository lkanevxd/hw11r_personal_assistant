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


class Task:
    def __init__(
        self, task_id, title, descr, done=False, prior="Средний", due_date=None
    ):
        self.id = task_id
        self.title = title
        self.descr = descr
        self.done = done
        self.prior = prior
        self.due_date = due_date


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        data = load_data(TASKS_FILE, [])
        self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        data = [task.__dict__ for task in self.tasks]
        save_data(TASKS_FILE, data)

    def add_task(self, title, descr, prior, due_date):
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = Task(task_id, title, descr, False, prior, due_date)
        self.tasks.append(new_task)
        self.save_tasks()
        print("Задача успешно добавлена!")

    def list_tasks(self, filt_by=None):
        if not self.tasks:
            print("Список задач пуст.")
            return
        filt_tasks = self.tasks
        if filt_by == "done":
            filt_tasks = [task for task in self.tasks if task.done]
        elif filt_by == "not_done":
            filt_tasks = [task for task in self.tasks if not task.done]
        for task in filt_tasks:
            status = "Выполнена" if task.done else "Не выполнена"
            print(
                f"{task.id}. {task.title} [{status}] (Приоритет: {task.prior}, Срок: {task.due_date})"
            )

    def mark_task_done(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.done = True
            self.save_tasks()
            print("Задача отмечена как выполненная!")
        else:
            print("Задача не найдена.")

    def edit_task(self, task_id, title, descr, prior, due_date):
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title
            task.descr = descr
            task.prior = prior
            task.due_date = due_date
            self.save_tasks()
            print("Задача успешно обновлена!")
        else:
            print("Задача не найдена.")

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print("Задача успешно удалена!")
        else:
            print("Задача не найдена.")

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def export_tasks_to_csv(self):
        if not self.tasks:
            print("Список задач пуст.")
            return
        fname = "tasks_export.csv"
        with open(fname, mode="w", encoding="utf-8", newline="") as csv_file:
            fieldnames = [
                "ID",
                "Название",
                "Описание",
                "Статус",
                "Приоритет",
                "Срок выполнения",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow(
                    {
                        "ID": task.id,
                        "Название": task.title,
                        "Описание": task.descr,
                        "Статус": "Выполнена" if task.done else "Не выполнена",
                        "Приоритет": task.prior,
                        "Срок выполнения": task.due_date,
                    }
                )
        print(f"Задачи успешно экспортированы в файл {fname}")

    def import_tasks_from_csv(self):
        fname = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(fname):
            print("Файл не найден.")
            return
        with open(fname, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                task_id = max([task.id for task in self.tasks], default=0) + 1
                title = row.get("Название", "")
                descr = row.get("Описание", "")
                status = row.get("Статус", "Не выполнена")
                done = True if status == "Выполнена" else False
                prior = row.get("Приоритет", "Средний")
                due_date = row.get("Срок выполнения", None)
                new_task = Task(task_id, title, descr, done, prior, due_date)
                self.tasks.append(new_task)
            self.save_tasks()
        print("Задачи успешно импортированы из CSV-файла.")


def tasks_menu():
    manager = TaskManager()
    while True:
        print("\nУправление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть все задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Экспорт задач в CSV")
        print("7. Импорт задач из CSV")
        print("8. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            title = input("Введите название задачи: ")
            descr = input("Введите описание задачи: ")
            prior = input("Выберите приоритет (Высокий/Средний/Низкий): ")
            due_date = input("Введите срок выполнения (в формате ДД-ММ-ГГГГ): ")
            manager.add_task(title, descr, prior, due_date)
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.mark_task_done(task_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "4":
            try:
                task_id = int(input("Введите ID задачи: "))
                title = input("Введите новое название задачи: ")
                descr = input("Введите новое описание задачи: ")
                prior = input("Выберите приоритет (Высокий/Средний/Низкий): ")
                due_date = input("Введите срок выполнения (в формате ДД-ММ-ГГГГ): ")
                manager.edit_task(task_id, title, descr, prior, due_date)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "5":
            try:
                task_id = int(input("Введите ID задачи: "))
                manager.delete_task(task_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "6":
            manager.export_tasks_to_csv()
        elif choice == "7":
            manager.import_tasks_from_csv()
        elif choice == "8":
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


class Contact:
    def __init__(self, contact_id, name, phone, mail):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.mail = mail


class ContactManager:
    def __init__(self):
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        data = load_data(CONTACTS_FILE, [])
        self.contacts = [Contact(**contact) for contact in data]

    def save_contacts(self):
        data = [contact.__dict__ for contact in self.contacts]
        save_data(CONTACTS_FILE, data)

    def add_contact(self, name, phone, mail):
        contact_id = max([contact.id for contact in self.contacts], default=0) + 1
        new_contact = Contact(contact_id, name, phone, mail)
        self.contacts.append(new_contact)
        self.save_contacts()
        print("Контакт успешно добавлен!")

    def search_contacts(self, query):
        ress = [
            contact
            for contact in self.contacts
            if query.lower() in contact.name.lower() or query in contact.phone
        ]
        if ress:
            for contact in ress:
                print(
                    f"{contact.id}. {contact.name} (Телефон: {contact.phone}, E-mail: {contact.mail})"
                )
        else:
            print("Контакты не найдены.")

    def edit_contact(self, contact_id, name, phone, mail):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            contact.name = name
            contact.phone = phone
            contact.mail = mail
            self.save_contacts()
            print("Контакт успешно обновлён!")
        else:
            print("Контакт не найден.")

    def delete_contact(self, contact_id):
        contact = self.get_contact_by_id(contact_id)
        if contact:
            self.contacts.remove(contact)
            self.save_contacts()
            print("Контакт успешно удалён!")
        else:
            print("Контакт не найден.")

    def get_contact_by_id(self, contact_id):
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None

    def export_contacts_to_csv(self):
        if not self.contacts:
            print("Список контактов пуст.")
            return
        fname = "contacts_export.csv"
        with open(fname, mode="w", encoding="utf-8", newline="") as csv_file:
            fieldnames = ["ID", "Имя", "Телефон", "E-mail"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for contact in self.contacts:
                writer.writerow(
                    {
                        "ID": contact.id,
                        "Имя": contact.name,
                        "Телефон": contact.phone,
                        "E-mail": contact.mail,
                    }
                )
        print(f"Контакты успешно экспортированы в файл {fname}")

    def import_contacts_from_csv(self):
        fname = input("Введите имя CSV-файла для импорта: ")
        if not os.path.exists(fname):
            print("Файл не найден.")
            return
        with open(fname, mode="r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                contact_id = (
                    max([contact.id for contact in self.contacts], default=0) + 1
                )
                name = row.get("Имя", "")
                phone = row.get("Телефон", "")
                mail = row.get("E-mail", "")
                new_contact = Contact(contact_id, name, phone, mail)
                self.contacts.append(new_contact)
            self.save_contacts()
        print("Контакты успешно импортированы из CSV-файла.")


def contacts_menu():
    manager = ContactManager()
    while True:
        print("\nУправление контактами:")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Экспорт контактов в CSV")
        print("6. Импорт контактов из CSV")
        print("7. Назад")
        choice = input("Выберите действие: ")
        if choice == "1":
            name = input("Введите имя контакта: ")
            phone = input("Введите номер телефона: ")
            mail = input("Введите e-mail: ")
            manager.add_contact(name, phone, mail)
        elif choice == "2":
            query = input("Введите имя или номер телефона для поиска: ")
            manager.search_contacts(query)
        elif choice == "3":
            try:
                contact_id = int(input("Введите ID контакта: "))
                name = input("Введите новое имя: ")
                phone = input("Введите новый номер телефона: ")
                mail = input("Введите новый e-mail: ")
                manager.edit_contact(contact_id, name, phone, mail)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "4":
            try:
                contact_id = int(input("Введите ID контакта: "))
                manager.delete_contact(contact_id)
            except ValueError:
                print("Некорректный ID.")
        elif choice == "5":
            manager.export_contacts_to_csv()
        elif choice == "6":
            manager.import_contacts_from_csv()
        elif choice == "7":
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")
