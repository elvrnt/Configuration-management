import unittest
from datetime import datetime
import calendar
from main import ShellEmulator
import tkinter as tk


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Настройка GUI и пути к тестовым файлам
        cls.root = tk.Tk()
        cls.root.withdraw()  # скрываем основное окно GUI для тестирования
        cls.zip_path = "test.zip"  # укажите правильный путь к вашему zip-файлу
        cls.log_path = "session_log.json"

        # Инициализация эмулятора
        cls.emulator = ShellEmulator(cls.root, "TestHost", cls.zip_path, cls.log_path)

    @classmethod
    def tearDownClass(cls):
        # Закрытие GUI после завершения тестов
        cls.root.destroy()

    def setUp(self):
        # Очищаем файл лога перед каждым тестом
        open(self.log_path, 'w').close()

    def tearDown(self):
        # Возвращаемся в корневой каталог после каждого теста
        self.emulator.current_dir = "/"
        self.emulator.output_area.delete("1.0", tk.END)
    def test_ls_command_root(self):
        self.emulator.parse_command("ls")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn("dir1", output)
        self.assertIn("dir2", output)

    def test_ls_command_subdirectory(self):
        self.emulator.parse_command("cd dir1")
        self.emulator.parse_command("ls")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    def test_ls_command_empty_directory(self):
        self.emulator.parse_command("cd dir2")
        self.emulator.parse_command("ls")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn("file3.txt", output)

    def test_cd_command_to_subdirectory(self):
        self.emulator.parse_command("cd dir1")
        self.assertEqual(self.emulator.current_dir, "/dir1")

    def test_cd_command_invalid_directory(self):
        self.emulator.parse_command("cd invalid_dir")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn("No such directory", output)

    def test_cd_command_root(self):
        self.emulator.parse_command("cd dir1")
        self.emulator.parse_command("cd ..")
        self.assertEqual(self.emulator.current_dir, "/")

    def test_du_command(self):
        self.emulator.parse_command("du")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        total_size = 50  # укажите общий размер всех файлов в виртуальной ФС
        self.assertIn(str(total_size), output)

    def test_uniq_command_file_with_duplicates(self):
        self.emulator.parse_command("uniq dir1/file1.txt")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn( "Hello\nWorld", output)

    def test_uniq_command_file_no_duplicates(self):
        self.emulator.parse_command("uniq dir1/file2.txt")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn("Content\nFile\nTest", output)

    def test_uniq_command_nonexistent_file(self):
        self.emulator.parse_command("uniq nonexistent.txt")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        self.assertIn("No such file", output)

    def test_cal_command(self):
        self.emulator.parse_command("cal")
        output = self.emulator.output_area.get("1.0", tk.END).strip()
        current_month_calendar = calendar.month(datetime.now().year, datetime.now().month).strip()
        self.assertIn(current_month_calendar, output)

if __name__ == "__main__":
    unittest.main()
