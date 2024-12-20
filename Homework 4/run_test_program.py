import os
from assembler import assembler, save_to_bin
from interpreter import interpreter

def generate_instructions():
    """Генерирует инструкции для выполнения операции взятия остатка над двумя векторами."""
    instructions = []
    vector_a = [12, 15, 20, 25, 30, 35]
    vector_b = [3, 4, 5, 6, 7, 8]  # Все значения во втором векторе ненулевые

    # Загрузка элементов первого вектора (A) в регистры и запись в память
    for i, value in enumerate(vector_a):
        instructions.append(("load_const", i, value))  # Загружаем в регистры 0-5
        instructions.append(("write_mem", i * 2, i, i))  # Записываем в память по адресам 0, 2, 4, ...

    # Загрузка элементов второго вектора (B) в регистры
    for i, value in enumerate(vector_b, start=6):
        instructions.append(("load_const", i, value))  # Загружаем в регистры 6-11
        instructions.append(("write_mem", (i - 6) * 2 + 1, i, i))  # Записываем в память по адресам 1, 3, 5, ...

    # Выполнение операции взятия остатка для каждого элемента
    for i in range(6):
        instructions.append(("mod_mem", i * 2 + 2, i * 2, i * 2 + 1, i + 6))  # Результаты записываются в память

    return instructions

def write_csv_instructions(instructions, file_path):
    """Сохраняет инструкции в CSV файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("operation,B,C\n")
        for instruction in instructions:
            f.write(",".join(map(str, instruction)) + "\n")

def main():
    # Параметры файлов
    instructions_file = "test_instructions.csv"
    binary_file = "test_binary.bin"
    result_file = "test_result.csv"  # Файл для записи результата
    log_file = "test_log.csv"

    # Генерация инструкций
    instructions = generate_instructions()
    write_csv_instructions(instructions, instructions_file)

    # Запуск ассемблера
    print("Сборка программы...")
    assembled_instructions = assembler(instructions, log_file)
    save_to_bin(assembled_instructions, binary_file)
    print(f"Программа собрана, бинарный файл: {binary_file}")

    # Запуск интерпретатора
    print("Запуск интерпретатора...")
    interpreter(binary_file, result_file, (0, 50))  # Убедимся, что обрабатываем всю память
    print(f"Результат интерпретации сохранён в файл: {result_file}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
