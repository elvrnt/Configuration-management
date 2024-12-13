import tkinter as tk
from tkinter import scrolledtext
import zipfile
import os
import json
from datetime import datetime
import calendar
from io import BytesIO
import argparse


class ShellEmulator:
    def __init__(self, root, hostname, zip_path, log_path, startup_script=None):
        self.root = root
        self.root.title("UNIX Shell Emulator")

        # Параметры эмулятора
        self.hostname = hostname  # Имя хоста для отображения в оболочке
        self.log_path = log_path  # Путь для сохранения логов команд
        self.command_log = []  # Список для хранения команд и их метаданных

        # Настройка графического интерфейса (GUI)
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=80)
        self.output_area.pack(pady=5)
        self.entry = tk.Entry(root, width=80)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.execute_command)  # Связываем нажатие Enter с выполнением команды

        # Виртуальная файловая система
        self.fs = self.load_virtual_fs(zip_path)  # Загружаем виртуальную ФС из ZIP-архива
        self.current_dir = "/"  # Начальная директория - корень
        self.update_output(f"{hostname}: Shell Emulator Initialized. Type 'exit' to close.")

        # Выполнение стартового скрипта, если указан
        if startup_script:
            self.run_startup_script(startup_script)

    def load_virtual_fs(self, zip_path):
        """Загружает виртуальную файловую систему из ZIP-архива."""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            fs = {name: BytesIO(zip_ref.read(name)) for name in zip_ref.namelist()}
        return fs

    def log_command(self, command):
        """Логирует команды с временными метками в JSON-файл."""
        timestamp = datetime.now().isoformat()
        log_entry = {"timestamp": timestamp, "command": command}
        self.command_log.append(log_entry)
        with open(self.log_path, 'w') as log_file:
            json.dump(self.command_log, log_file, indent=2)

    def execute_command(self, event):
        """Выполняет команду, введенную пользователем."""
        command = self.entry.get().strip()  # Получаем команду из поля ввода
        self.entry.delete(0, tk.END)  # Очищаем поле ввода
        if command:
            self.log_command(command)  # Логируем команду
            self.parse_command(command)  # Анализируем и выполняем команду

    def parse_command(self, command):
        """Определяет и вызывает соответствующую функцию для выполнения команды."""
        parts = command.split()  # Разбиваем команду на части
        if parts[0] == "ls":
            self.ls_command()
        elif parts[0] == "cd":
            self.cd_command(parts[1] if len(parts) > 1 else "")
        elif parts[0] == "du":
            self.du_command()
        elif parts[0] == "uniq":
            self.uniq_command(parts[1] if len(parts) > 1 else "")
        elif parts[0] == "cal":
            self.cal_command()
        elif parts[0] == "pwd":
            self.pwd_command()
        elif parts[0] == "exit":
            self.root.quit()
        else:
            self.update_output(f"Unknown command: {command}")

    def pwd_command(self):
        """Отображает текущую директорию."""
        self.update_output(f"Current directory: {self.current_dir}")

    def ls_command(self):
        """Выводит содержимое текущей директории."""
        # Форматируем путь текущей директории
        path = self.current_dir.strip("/")
        if path:
            path += "/"

        # Получаем элементы, находящиеся в текущей директории
        contents = set()
        for item in self.fs:
            if item.startswith(path):
                subpath = item[len(path):].split("/", 1)[0]
                contents.add(subpath)

        # Выводим содержимое
        if contents:
            self.update_output("\n".join(sorted(contents)))
        else:
            self.update_output(f"No files or directories in '{self.current_dir}'.")

    def cd_command(self, directory):
        """Меняет текущую директорию."""
        if directory == "..":
            # Переход на уровень выше
            if self.current_dir != "/":
                self.current_dir = os.path.dirname(self.current_dir.rstrip("/"))
                if not self.current_dir:
                    self.current_dir = "/"
            self.update_output(f"Changed directory to {self.current_dir}")
            return

        # Переход в указанную поддиректорию
        new_dir = os.path.join(self.current_dir, directory).replace("\\", "/").strip("/")
        new_dir_path = f"{new_dir}/" if new_dir else "/"

        if any(name.startswith(new_dir_path) for name in self.fs if name != new_dir_path):
            self.current_dir = f"/{new_dir}".rstrip("/")
            self.update_output(f"Changed directory to {self.current_dir}")
        else:
            self.update_output(f"No such directory: {directory}")

    def du_command(self):
        """Подсчитывает общий размер файлов в текущей директории."""
        path = self.current_dir.strip("/")
        if path:
            path += "/"

        total_size = 0
        for name, content in self.fs.items():
            relative_path = name[len(path):] if path else name
            if "/" not in relative_path and name.startswith(path):
                total_size += len(content.getvalue())

        if total_size > 0:
            self.update_output(f"Total size of '{self.current_dir}': {total_size} bytes")
        else:
            self.update_output(f"No files in directory '{self.current_dir}' or directory does not exist.")

    def uniq_command(self, file):
        """Удаляет дублирующиеся строки в указанном файле и выводит результат."""
        file_path = os.path.join(self.current_dir.strip("/"), file).strip("/")
        if file_path in self.fs:
            lines = self.fs[file_path].getvalue().decode().splitlines()
            unique_lines = "\n".join(sorted(set(lines)))
            self.update_output(unique_lines)
        else:
            self.update_output(f"No such file: {file}")

    def cal_command(self):
        """Выводит календарь текущего месяца."""
        month_calendar = calendar.month(datetime.now().year, datetime.now().month)
        self.update_output(month_calendar)

    def update_output(self, text):
        """Выводит текст в поле вывода и прокручивает вниз."""
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)

    def run_startup_script(self, script_path):
        """Выполняет команды из стартового скрипта."""
        with open(script_path, 'r') as script:
            for line in script:
                command = line.strip()
                if command:
                    self.log_command(command)
                    self.parse_command(command)


if __name__ == "__main__":
    # Аргументы командной строки
    parser = argparse.ArgumentParser(description="UNIX Shell Emulator")
    parser.add_argument("--hostname", required=True, help="Hostname for the shell prompt")
    parser.add_argument("--zip_path", required=True, help="Path to the ZIP archive of the virtual file system")
    parser.add_argument("--log_path", required=True, help="Path to the JSON log file")
    parser.add_argument("--startup_script", help="Path to the startup script to execute on launch")

    args = parser.parse_args()

    # Инициализация и запуск GUI
    root = tk.Tk()
    app = ShellEmulator(root, args.hostname, args.zip_path, args.log_path, args.startup_script)
    root.mainloop()

