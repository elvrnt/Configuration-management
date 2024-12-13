import xml.etree.ElementTree as ET
from config_language import convert_xml_to_custom_language, ConfigSyntaxError

def run_test(test_input, expected_output):
    """Запускает тест и выводит результат."""
    root = ET.fromstring(test_input)
    result = convert_xml_to_custom_language(root)
    assert result == expected_output, f"Ошибка: ожидалось '{expected_output}', получено '{result}'"
    print(f"Тест прошел: {result}")

def main():
    try:
        # Тест 1: Одна переменная
        xml_input_1 = '''<root>
            <variable name="MY_VAR">42</variable>
        </root>'''
        run_test(xml_input_1, "var MY_VAR := 42;")

        # Тест 2: Массив
        xml_input_2 = '''<root>
            <array>
                <value>1</value>
                <value>2</value>
                <value>3</value>
            </array>
        </root>'''
        run_test(xml_input_2, "<< 1, 2, 3 >>")

        # Тест 3: Определение константы
        xml_input_3 = '''<root>
            <constant name="PI">3.14</constant>
        </root>'''
        run_test(xml_input_3, "(define PI 3.14)")

        # Тест 4: Вычисление константы
        xml_input_4 = '''<root>
            <constant name="SPEED_OF_LIGHT">299792458</constant>
            <variable name="LIGHT_SPEED_VAR">$(SPEED_OF_LIGHT)</variable>
        </root>'''
        run_test(xml_input_4, "(define SPEED_OF_LIGHT 299792458)\nvar LIGHT_SPEED_VAR := 299792458;")

        # Тест 5: Неверное имя переменной
        xml_input_5 = '''<root>
            <variable name="InvalidName">42</variable>
        </root>'''
        try:
            run_test(xml_input_5, "")
        except ConfigSyntaxError as e:
            print(f"Тест на неверное имя переменной прошел: {e}")

        # Тест 6: Неверное имя константы
        xml_input_6 = '''<root>
            <constant name="InvalidName">3.14</constant>
        </root>'''
        try:
            run_test(xml_input_6, "")
        except ConfigSyntaxError as e:
            print(f"Тест на неверное имя константы прошел: {e}")

        # Пример 1: Конфигурация для вычислений
        computation_config = '''<root>
            <constant name="EULER_NUMBER">2.718</constant>
            <variable name="E_VAR">$(EULER_NUMBER)</variable>
            <array>
                <value>10</value>
                <value>20</value>
                <value>30</value>
            </array>
        </root>'''
        run_test(computation_config, "(define EULER_NUMBER 2.718)\nvar E_VAR := 2.718;\n<< 10, 20, 30 >>")

        # Пример 2: Конфигурация для сетевых настроек
        network_config = '''<root>
            <constant name="DEFAULT_PORT">8080</constant>
            <variable name="PORT_VAR">$(DEFAULT_PORT)</variable>
            <array>
                <value>192.168.1.1</value>
                <value>192.168.1.2</value>
            </array>
        </root>'''
        run_test(network_config, "(define DEFAULT_PORT 8080)\nvar PORT_VAR := 8080;\n<< 192.168.1.1, 192.168.1.2 >>")

        # Тест 7: Вложенные массивы
        nested_array_config = '''<root>
            <array>
                <value>1</value>
                <value>2</value>
                <array>
                    <value>3</value>
                    <value>4</value>
                    <array>
                        <value>5</value>
                    </array>
                </array>
            </array>
        </root>'''
        expected_nested_output = "<< 1, 2, << 3, 4, << 5 >> >> >>"
        run_test(nested_array_config, expected_nested_output)

        print("Все тесты выполнены успешно!")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()