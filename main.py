from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ

# Функция для нормализации ФИО
def normalize_name(full_name):
    parts = full_name.split()
    # Заполняем фамилию, имя, отчество
    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""
    return lastname, firstname, surname


# Функция для нормализации телефона
def normalize_phone(phone):
    if not phone:
        return ""

    # Удаляем все нецифровые символы, кроме "+" и "доб."
    phone_clean = re.sub(r'[^\d+]', '', phone)

    # Если есть "доб." или "доб" в оригинальном номере
    extension_match = re.search(r'доб\.?\s*(\d+)', phone, re.IGNORECASE)
    extension = f" доб.{extension_match.group(1)}" if extension_match else ""

    # Извлекаем только цифры основного номера
    digits = re.sub(r'\D', '', phone)

    # Форматируем основной номер
    if len(digits) >= 11:
        # Если номер начинается с 8 или 7, заменяем на +7
        if digits.startswith('8') or digits.startswith('7'):
            main_number = digits[1:] if len(digits) == 11 else digits
            if len(main_number) == 10:
                formatted = f"+7({main_number[:3]}){main_number[3:6]}-{main_number[6:8]}-{main_number[8:10]}"
            else:
                formatted = phone  # оставляем как есть, если формат не распознан
        else:
            formatted = phone  # оставляем как есть, если формат не распознан
    else:
        formatted = phone  # оставляем как есть, если номер слишком короткий

    return formatted + extension


# Обрабатываем каждую запись
processed_contacts = []
for contact in contacts_list[1:]:  # пропускаем заголовок
    # Нормализуем ФИО
    lastname, firstname, surname = normalize_name(" ".join(contact[:3]))

    # Нормализуем телефон
    phone = normalize_phone(contact[5])

    # Создаем новую запись
    new_contact = [
        lastname,
        firstname,
        surname,
        contact[3],  # организация
        contact[4],  # должность
        phone,
        contact[6]  # email
    ]
    processed_contacts.append(new_contact)

# Объединяем дублирующиеся записи
unique_contacts = {}
for contact in processed_contacts:
    key = (contact[0], contact[1])  # ключ по Фамилии и Имени

    if key in unique_contacts:
        # Объединяем данные, отдавая предпочтение непустым значениям
        existing = unique_contacts[key]
        for i in range(len(contact)):
            if contact[i] and not existing[i]:
                existing[i] = contact[i]
    else:
        unique_contacts[key] = contact.copy()

# Преобразуем словарь обратно в список
final_contacts = [contacts_list[0]]  # добавляем заголовок
final_contacts.extend(unique_contacts.values())

# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts)

# Выводим результат для проверки
print("Обработанные контакты:")
pprint(final_contacts)