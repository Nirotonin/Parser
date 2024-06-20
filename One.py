import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from OOP import CSS, HTML, Links, Text, JS, Photo, Links_global, Photo_global, Video, SEE
import sys

class ParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Парсер")
        self.create_widgets()
        self.preview_windows = {}

    def create_widgets(self):
        self.url_label = tk.Label(self.root, text="Введите URL страницы:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        self.save_label = tk.Label(self.root, text="Выберите папку для сохранения файлов:")
        self.save_label.pack(pady=5)

        self.save_frame = tk.Frame(self.root)
        self.save_frame.pack(pady=5)
        self.save_entry = tk.Entry(self.save_frame, width=40)
        self.save_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.save_button = tk.Button(self.save_frame, text="Выбрать", command=self.select_directory)
        self.save_button.pack(side=tk.LEFT)

        self.options_label = tk.Label(self.root, text="Выберите функции для выполнения:")
        self.options_label.pack(pady=5)

        self.css_var = tk.BooleanVar()
        self.css_check = tk.Checkbutton(self.root, text="Парсинг CSS", variable=self.css_var, command=lambda: self.toggle_preview('css'))
        self.css_check.pack(anchor='w')

        self.html_var = tk.BooleanVar()
        self.html_check = tk.Checkbutton(self.root, text="Парсинг HTML", variable=self.html_var, command=lambda: self.toggle_preview('html'))
        self.html_check.pack(anchor='w')

        self.js_var = tk.BooleanVar()
        self.js_check = tk.Checkbutton(self.root, text="Парсинг JS", variable=self.js_var, command=lambda: self.toggle_preview('js'))
        self.js_check.pack(anchor='w')

        self.photo_var = tk.BooleanVar()
        self.photo_check = tk.Checkbutton(self.root, text="Парсинг изображений", variable=self.photo_var)
        self.photo_check.pack(anchor='w')

        self.photo_global_var = tk.BooleanVar()
        self.photo_global_check = tk.Checkbutton(self.root, text="Парсинг изображений (глобальный)", variable=self.photo_global_var)
        self.photo_global_check.pack(anchor='w')

        self.links_var = tk.BooleanVar()
        self.links_check = tk.Checkbutton(self.root, text="Парсинг ссылок", variable=self.links_var)
        self.links_check.pack(anchor='w')

        self.links_global_var = tk.BooleanVar()
        self.links_global_check = tk.Checkbutton(self.root, text="Парсинг ссылок (глобальный)", variable=self.links_global_var)
        self.links_global_check.pack(anchor='w')

        self.text_var = tk.BooleanVar()
        self.text_check = tk.Checkbutton(self.root, text="Парсинг текста", variable=self.text_var)
        self.text_check.pack(anchor='w')

        self.video_var = tk.BooleanVar()
        self.video_check = tk.Checkbutton(self.root, text="Парсинг видео", variable=self.video_var)
        self.video_check.pack(anchor='w')

        self.run_button = tk.Button(self.root, text="Запустить", command=self.start_parsing)
        self.run_button.pack(pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_entry.delete(0, tk.END)
            self.save_entry.insert(0, directory)

    def start_parsing(self):
        url = self.url_entry.get()
        save_directory = self.save_entry.get()
        if not url or not save_directory:
            messagebox.showerror("Ошибка", "Пожалуйста, введите URL и выберите путь к папке для сохранения файлов.")
            return

        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Прогресс")
        self.progress_label = tk.Label(self.progress_window, text="Выполнение парсинга...")
        self.progress_label.pack(pady=5)
        self.progress = ttk.Progressbar(self.progress_window, orient="horizontal", mode="indeterminate")
        self.progress.pack(pady=20)
        self.progress_window.protocol("WM_DELETE_WINDOW", self.on_progress_window_close)

        self.progress.start()

        parsing_thread = threading.Thread(target=self.run_parsers, args=(url, save_directory))
        parsing_thread.start()

    def on_progress_window_close(self):
        messagebox.showwarning("Предупреждение", "Пожалуйста, дождитесь завершения процесса парсинга.")
        return

    def run_parsers(self, url, save_directory):
        tasks = []
        if self.css_var.get():
            tasks.append(('Парсинг CSS', CSS.extract_css_from_page, (url, save_directory)))
        if self.js_var.get():
            tasks.append(('Парсинг JS', JS.get_js_from_page, (url, save_directory)))
        if self.photo_var.get():
            tasks.append(('Парсинг изображений', Photo.fetch_images_from_url, (url, save_directory)))
        if self.photo_global_var.get():
            tasks.append(('Парсинг изображений (глобальный)', Photo_global.main, (url, save_directory)))
        if self.html_var.get():
            tasks.append(('Парсинг HTML', HTML.save_html_to_file, (HTML.fetch_html_from_url(url), save_directory, 'page.html')))
        if self.links_var.get():
            tasks.append(('Парсинг ссылок', Links.extract_links_from_page, (url, save_directory)))
        if self.links_global_var.get():
            tasks.append(('Парсинг ссылок (глобальный)', Links_global.extract_links_from_site, (url, save_directory)))
        if self.text_var.get():
            tasks.append(('Парсинг текста', Text.main, (url, save_directory)))
        if self.video_var.get():
            tasks.append(('Парсинг видео', Video.download_videos, (url, save_directory)))

        if not tasks:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите хотя бы одну функцию для выполнения.")
            self.progress_window.destroy()
            return

        results = []
        for task_name, task_func, args in tasks:
            try:
                result = task_func(*args)
                if result is None:
                    result = "Операция успешно выполнена."
            except Exception as e:
                result = f"Ошибка: {str(e)}"
            results.append(f"Результат {task_name}:\n{result}")

        self.progress.stop()
        self.progress_window.destroy()
        result_message = "\n\n".join(results)
        messagebox.showinfo("Результаты парсинга", result_message)

    def toggle_preview(self, content_type):
        if self.preview_windows.get(content_type):
            self.preview_windows[content_type].destroy()
            del self.preview_windows[content_type]
        else:
            self.show_preview_window(content_type)

    def show_preview_window(self, content_type):
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Предварительный просмотр {content_type.upper()}")

        text_frame = tk.Frame(preview_window)
        text_frame.pack(expand=True, fill="both", padx=5, pady=5)

        text_widget = tk.Text(text_frame, wrap="none", width=80, height=24)
        text_widget.pack(expand=True, fill="both", side="left")

        scrollbar_y = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar_y.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(preview_window, orient="horizontal", command=text_widget.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        text_widget.configure(xscrollcommand=scrollbar_x.set)

        load_button = tk.Button(preview_window, text="Загрузить",
                                command=lambda: self.load_content(content_type, text_widget))
        load_button.pack(pady=5)

        self.preview_windows[content_type] = preview_window

    def load_content(self, content_type, text_widget):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Ошибка", "Пожалуйста, введите URL для предварительного просмотра.")
            return

        text_widget.delete(1.0, tk.END)
        try:
            if content_type == "css":
                content = SEE.view_css_from_page(url)
            elif content_type == "html":
                content = HTML.fetch_html_from_url(url)
            elif content_type == "js":
                content = SEE.view_js_from_page(url)
            else:
                content = "Неизвестный тип контента"
            text_widget.insert(tk.END, content)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить {content_type.upper()}: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ParserApp(root)
    root.mainloop()
