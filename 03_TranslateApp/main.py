import customtkinter as ctk
import docx
import cryptography
import markdown

def main():
    # Cấu hình giao diện mặc định
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Khởi tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Translate App - Setup Test")
    root.geometry("400x200")

    # Thêm Label để kiểm tra hiển thị
    label = ctk.CTkLabel(root, text="Project Setup Successful!", font=ctk.CTkFont(size=20, weight="bold"))
    label.pack(pady=40)

    # Hiển thị phiên bản thư viện
    version_label = ctk.CTkLabel(root, text=f"CustomTkinter v{ctk.__version__}")
    version_label.pack()

    # Chạy ứng dụng
    root.mainloop()

if __name__ == '__main__':
    main()
