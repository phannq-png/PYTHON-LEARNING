"""Application entry point for TranslatorApp."""

import customtkinter as ctk

from src.ui.app_window import AppWindow


def main() -> None:
    # Cấu hình giao diện mặc định — phải set trước khi tạo bất kỳ widget nào
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
