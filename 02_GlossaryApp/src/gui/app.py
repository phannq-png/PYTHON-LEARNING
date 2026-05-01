import customtkinter as ctk
from tkinter import ttk, messagebox
from .components.menu_bar import MenuBar as AppMenu

class GlossaryApp(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        
        self.db = db_manager
        self.title("Glossary App")
        self.geometry("800x500")

        # 1. Khởi tạo Menu
        self.config(menu=AppMenu(self, self.db))
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left: input form
        self.frame_left = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label_title = ctk.CTkLabel(self.frame_left, text="Glossary manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_title.pack(pady=20)

        # Japanese input
        self.entry_jp = ctk.CTkEntry(self.frame_left, placeholder_text="Japanese")
        self.entry_jp.pack(fill = "x", padx = 10, pady = 10)

        # Vietnamese input
        self.entry_vi = ctk.CTkEntry(self.frame_left, placeholder_text="Vietnamese")
        self.entry_vi.pack(fill = "x", padx = 10, pady = 10)

        # Add button
        self.btn_add = ctk.CTkButton(self.frame_left, text="Add", command=self.add_entry)
        self.btn_add.pack(fill = "x", padx = 20, pady = 20)

        # Right: list of words
        self.frame_right = ctk.CTkFrame(self, corner_radius=10)
        self.frame_right.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        # Sử dụng Treeview của ttk để hiển thị bảng (do CustomTkinter chưa có bảng sẵn)
        columns = ("id", "jp", "vi")
        self.tree = ttk.Treeview(self.frame_right, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("jp", text="Japanese")
        self.tree.heading("vi", text="Vietnamese")
        self.tree.column("id", width=50, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Delete button
        self.btn_delete = ctk.CTkButton(self.frame_left, text="Delete", command=self.delete_entry)
        self.btn_delete.pack( pady = 10)

        # Load words from database
        self.refresh_table()

    def refresh_table(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Lấy dữ liệu mới từ database
        words = self.db.fetch_all()
        # Thêm dữ liệu vào bảng
        for word in words:
            self.tree.insert("", "end", values=word)

    def add_entry(self):
        # Lấy dữ liệu từ ô nhập liệu                                
        jp = self.entry_jp.get()
        vi = self.entry_vi.get()
        if not jp or not vi:
            messagebox.showwarning("Warning", "Please fill in both Japanese and Vietnamese fields.")
            return
        
        # Kiểm tra trùng lặp trước khi thêm
        if self.db.is_dupplicate(jp):
            messagebox.showerror("Error", f"The word '{jp}' already exists in the glossary.")
            return
        
        self.db.add_entry(jp, vi)
        self.refresh_table()
        self.entry_jp.delete(0, "end")
        self.entry_vi.delete(0, "end")
    
    def delete_entry(self):
        # Lấy danh sách các dòng được chọn
        selected_items = self.tree.selection()
    
        # KIỂM TRA: Nếu tuple rỗng (không có dòng nào được chọn)
        if not selected_items:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một từ trong danh sách để xóa!")
            return
    
        # Nếu có chọn, lấy dòng đầu tiên (trong trường hợp chọn nhiều dòng)
        target_item = selected_items[0]
    
        # Lấy dữ liệu của dòng đó
        item_data = self.tree.item(target_item)["values"]
        item_id = item_data[0]
    
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa từ: {item_data[1]}?"):
            self.db.delete_entry(item_id)
            self.refresh_table()


        

        
        
        
        