import customtkinter as ctk
from src.ui.components.left_sidebar import LeftSidebar

def test_sidebar():
    root = ctk.CTk()
    root.geometry("400x600")
    root.title("Test Sidebar UI")

    def on_page_selected(idx):
        print(f"Selected Page: {idx + 1}")

    sidebar = LeftSidebar(root, on_page_selected=on_page_selected)
    sidebar.pack(side="left", fill="y")

    # Simulate loading 20 pages
    sidebar.populate_pages(20, current_page_index=0)

    # Add a button to test dynamic update
    btn_test = ctk.CTkButton(root, text="Populate 5 Pages", command=lambda: sidebar.populate_pages(5, 2))
    btn_test.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    test_sidebar()
