"""Modal progress window (Polished)."""

from typing import Optional

import customtkinter as ctk
from src.utils import constants as c


class ProgressWindow(ctk.CTkToplevel):
    """Polished modal window with a progress bar."""

    def __init__(self, master, title: str = "Đang xử lý...", **kwargs):
        super().__init__(master, **kwargs)
        self.title(title)
        self.geometry("420x200")
        
        self.after(10, self._center_window)
        self.grab_set() 
        self.protocol("WM_DELETE_WINDOW", lambda: None) # Disable close

        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure((0, 1, 2), weight=1)

        self.lbl_title = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=15, weight="bold"))
        self.lbl_title.grid(row=0, column=0, pady=(25, 10))

        self.progress_bar = ctk.CTkProgressBar(self, width=320, corner_radius=c.CORNER_RADIUS, progress_color=c.COLOR_PRIMARY)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, padx=50, pady=10)

        self.lbl_status = ctk.CTkLabel(self, text="Vui lòng đợi...", font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=11), text_color="gray60")
        self.lbl_status.grid(row=2, column=0, pady=(0, 25))

    def _center_window(self):
        self.lift(); self.focus_force()
        if self.master:
            mx, my = self.master.winfo_x(), self.master.winfo_y()
            mw, mh = self.master.winfo_width(), self.master.winfo_height()
            x = mx + (mw // 2) - 210
            y = my + (mh // 2) - 100
            self.geometry(f"+{x}+{y}")

    def set_progress(self, value: float, text: Optional[str] = None):
        self.progress_bar.set(value)
        if text: self.lbl_status.configure(text=text)
        self.update_idletasks()

    def complete(self):
        self.grab_release(); self.destroy()
