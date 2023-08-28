import os
import re
import sys
import shutil

folder_path = sys.argv[1]

file_groups = {}
new_file_names = {}
file_extensions = {
    'зображення': ('.jpeg', '.jpg', '.png', '.svg'),
    'відео': ('.avi', '.mp4', '.mov', '.mkv'),
    'документи': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'музика': ('.mp3', '.ogg', '.wav', '.amr'),
    'архіви': ('.zip', '.gz', '.tar', '.rar')
}

def translate(name):

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANSLATION_str = ''.join(TRANSLATION)
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    latin_name = ""
    for i in name:
        if re.match(r'[абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ]', i, flags=re.IGNORECASE):
            latin_name += str(TRANS.get(ord(i), '_'))
        elif re.match(r'[a-zA-Z0-9]', i):
            latin_name += i
        else:
            latin_name += "_"
    return latin_name

# функція для визначення типу файлу за розширенням
def get_file_type(file_extension):

    for type_name, extensions in file_extensions.items():
        if file_extension.lower() in extensions:
            return type_name

# видалення всіх пустих папок крім file_extensions або ["archives", "video", "audio", "documents", "images"]
def remove_empty_folders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for directory in dirs:
            current_folder = os.path.join(root, directory)
            # print(directory)
            if directory in list(file_extensions.keys()) or directory in ["archives", "video", "audio", "documents", "images"]:
                continue
            if not os.listdir(current_folder):
                try:
                    os.rmdir(current_folder)
                    print(f'Папка видалена: {current_folder}')
                except Exception as e:
                    print(f'Помилка видалення папки {current_folder}: {str(e)}')

def extract_archive(archive_path, destination_folder):
    # Розпаковування архіву тут
    try:
        # Використовуємо shutil для розпакування архіву
        shutil.unpack_archive(archive_path, destination_folder)
        print(f'Архів {archive_path} розпаковано до {destination_folder}')
    except Exception as e:
        print(f'Помилка під час розпакування архіву {archive_path}: {str(e)}')


def main():
    remove_empty_folders(folder_path)

    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_extension = os.path.splitext(filename)[1]
            file_name = os.path.splitext(filename)[0]
            print("file_name ", file_name)
            file_type = get_file_type(file_extension)

            translated_name = translate(file_name)
            all_translated_name = translated_name + file_extension
            try:
                type_folder = os.path.join(folder_path, file_type)
                if not os.path.exists(type_folder):
                    os.makedirs(type_folder)
            except:
                type_folder = folder_path
            print("type_folder ", type_folder)


            new_file_names[filename] = os.path.join(type_folder, all_translated_name)

            if file_type == 'архіви':
                archive_path = os.path.join(folder_path, filename)
                archive_name = os.path.splitext(filename)[0]
                archive_destination_folder = os.path.join(type_folder, archive_name)

                # Розпаковуємо архів та переміщуємо відповідну папку
                print("archive_path :", archive_path)
                print("destination_folder :", archive_destination_folder)

                extract_archive(archive_path, archive_destination_folder, file_name, file_extension)

                # Видаляємо розпакований архів
                os.remove(archive_path)

    for old_name, new_name in new_file_names.items():
        source_path = os.path.join(folder_path, old_name)
        destination_path = os.path.join(folder_path, new_name)
        os.rename(source_path, destination_path)

    print(f"Папку {folder_path} відсортовано!")

if __name__ == '__main__':
    main()