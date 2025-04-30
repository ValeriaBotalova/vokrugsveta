def check_null_bytes(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        if b'\x00' in content:
            print("В файле есть нулевые байты.")
        else:
            print("Нулевых байт не обнаружено.")

# Замените 'your_models.py' на путь к вашему файлу
check_null_bytes('C:/Users/Public/4semestr/КП/kp/vokrugsveta/main/models.py')
