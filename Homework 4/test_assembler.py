from assembler import assembler

def test_load_const():
    instructions = [
        ("load_const", 40, 803)  # Пример: Загрузка константы
    ]
    expected_bytes = bytes([0x86, 0x8E, 0x0C, 0x00, 0x00, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test load_const failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test load_const passed.")

def test_read_mem():
    instructions = [
        ("read_mem", 28, 934)  # Пример: Чтение значения из памяти
    ]
    expected_bytes = bytes([0xCA, 0x99, 0x0E, 0x00, 0x00, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test read_mem failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test read_mem passed.")

def test_write_mem():
    instructions = [
        ("write_mem", 46, 31, 60)  # Пример: Запись значения в память
    ]
    expected_bytes = bytes([0xEC, 0xFA, 0x78, 0x00, 0x00, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test write_mem failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test write_mem passed.")

def test_mod_mem():
    instructions = [
        ("mod_mem", 92, 42, 57, 33)  # Пример: Бинарная операция (взятие остатка)
    ]
    expected_bytes = bytes([0xCE, 0x55, 0xF3, 0x10, 0x00, 0x00])
    result = assembler(instructions)
    assert result == list(expected_bytes), f"Test mod_mem failed. Expected {expected_bytes}, got {bytes(result)}"
    print("Test mod_mem passed.")

if __name__ == "__main__":
    test_load_const()
    test_read_mem()
    test_write_mem()
    test_mod_mem()
    print("All tests passed successfully!")
