import argparse


def popcnt(value):
    """Подсчет количества установленных битов (единиц) в числе."""
    return bin(value).count('1')


def interpreter(binary_path, result_path, memory_range):
    # Инициализация памяти и регистров
    memory = [0] * 64  # 64 ячейки памяти
    registers = [0] * 32  # 32 регистра

    with open(binary_path, "rb") as binary_file:
        byte_code = binary_file.read()

    i = 0
    while i < len(byte_code):
        command = byte_code[i] & 0x0F  # Биты 0-3 для команды

        if command == 6:  # load_const (Загрузка константы)
            B = (int.from_bytes(byte_code[i:i + 6], "little") >> 4) & 0x1F  # Индекс регистра
            C = (int.from_bytes(byte_code[i:i + 6], "little") >> 10) & 0xFFFFF  # Константа
            if 0 <= B < len(registers):  # Проверка на допустимый индекс регистра
                registers[B] = C
                print(f"Загрузка константы: регистр[{B}] = {C}")
            else:
                print(f"Ошибка: Неверный индекс регистра {B}")
        elif command == 10:  # read_mem (Чтение значения из памяти)
            B = (int.from_bytes(byte_code[i:i + 6], "little") >> 4) & 0x1F  # Регистр для хранения
            C = (int.from_bytes(byte_code[i:i + 6], "little") >> 10) & 0xFFFFF  # Адрес памяти
            if 0 <= B < len(registers) and 0 <= C < len(memory):  # Проверка на допустимые индексы
                registers[B] = memory[C]
                print(f"Чтение из памяти: регистр[{B}] = память[{C}]")
            else:
                print(f"Ошибка: Неверный индекс {B} или {C} (регистр или память)")
        elif command == 12:  # write_mem (Запись значения в память)
            B = (int.from_bytes(byte_code[i:i + 6], "little") >> 4) & 0x3F  # Смещение
            C = (int.from_bytes(byte_code[i:i + 6], "little") >> 11) & 0x1F  # Адрес памяти
            D = (int.from_bytes(byte_code[i:i + 6], "little") >> 17) & 0x1F  # Регистр для записи
            if 0 <= C + B < len(memory) and 0 <= D < len(registers):  # Проверка индексов
                memory[C + B] = registers[D]
                print(f"Запись в память: память[{C + B}] = регистр[{D}]")
            else:
                print(f"Ошибка: Неверный адрес памяти или индекс регистра. C={C}, B={B}, D={D}")
        elif command == 14:  # mod_mem (Остаток от деления)
            B = (int.from_bytes(byte_code[i:i + 6], "little") >> 4) & 0x3F  # Смещение
            C = (int.from_bytes(byte_code[i:i + 6], "little") >> 11) & 0x1F  # Адрес памяти
            D = (int.from_bytes(byte_code[i:i + 6], "little") >> 17) & 0x1F  # Регистр D
            E = (int.from_bytes(byte_code[i:i + 6], "little") >> 23) & 0x1F  # Регистр E
            if 0 <= C + B < len(memory) and 0 <= D < len(registers) and 0 <= E < len(registers):
                if registers[E] != 0:
                    memory[C + B] = memory[registers[D]] % registers[E]
                    print(f"Остаток: память[{C + B}] = память[{registers[D]}] % регистр[{E}]")
                else:
                    print(f"Ошибка: деление на ноль!")
                    return False
            else:
                print(f"Ошибка: Неверные индексы для модификации памяти или регистров. C={C}, B={B}, D={D}, E={E}")
        i += 6  # Переход к следующей команде (каждая команда занимает 6 байт)

    # Запись значений в файл-результат
    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Address,Value\n")
        for address in range(memory_range[0], memory_range[1] + 1):
            if 0 <= address < len(memory):  # Проверка диапазона адресов
                result_file.write(f"{address},{memory[address]}\n")
                print(f"Память[{address}] = {memory[address]}")
            else:
                print(f"Ошибка: Адрес {address} выходит за пределы памяти.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Interpreting the bytes like instructions (from binary file) to the csv-table.")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("result_path", help="Path to the result file (csv)")
    parser.add_argument("first_index", help="The first index of the displayed memory")
    parser.add_argument("last_index", help="The last index of the displayed memory")
    args = parser.parse_args()
    interpreter(args.binary_path, args.result_path, (int(args.first_index), int(args.last_index)))
