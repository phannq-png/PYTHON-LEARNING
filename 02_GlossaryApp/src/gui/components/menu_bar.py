from tkinter import Menu, filedialog, messagebox
import csv

class MenuBar(Menu):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.parent = parent

        file_menu = Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import CSV", command=self.import_csv)
        file_menu.add_command(label="Export CSV", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.parent.quit)
    
    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                next(reader) # Skip header row

                added_entries = 0
                skipped_entries = 0

                for row in reader:
                    if len(row) == 2 :
                        if self.db.is_dupplicate(row[0]):
                            skipped_entries += 1
                            continue 
                        self.db.add_entry(row[0], row[1])
                        added_entries += 1
                    else: 
                        messagebox.showerror("Invalid Data", f"Invalid data format in row: {row}")
                        return
            self.parent.refresh_table()
            messagebox.showinfo("Import Successful", f"CSV data imported successfully. Added: {added_entries}, Skipped: {skipped_entries}")
    
    def export_csv(self):
        file_path= filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = self.db.fetch_all()
            with open(file_path, mode="w", encoding="utf-8-sig", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Japanese", "Vietnamese"])
                writer.writerows([(row[1], row[2]) for row in data])
                messagebox.showinfo("Export Successful", "CSV data exported successfully")
    
    def clear_all(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all entries? This action cannot be undone."):
            self.db.clear_all()
            self.parent.refresh_table()
