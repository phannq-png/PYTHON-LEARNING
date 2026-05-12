"""Reusable loading spinner component using a rotating image in a centered Toplevel window."""

import customtkinter as ctk
from PIL import Image
import os
from src.utils import constants as c

class LoadingSpinner(ctk.CTkToplevel):
    """A rotating spinner component inside a centered Toplevel window."""

    def __init__(
        self, 
        master, 
        image_path="src/assets/spinner.png", 
        size=(48, 48), 
        speed_ms=80,
        text="Đang xử lý...",
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.master_window = master
        
        # ── Window Properties ──────────────────────────────────────────────
        self.title("Processing")
        self.withdraw()  # Hide initially
        self.overrideredirect(True)  # Remove title bar
        self.attributes("-topmost", True)  # Stay on top
        
        self.size = size
        self.speed_ms = speed_ms
        self.angle = 0
        self.is_spinning = False
        
        # ── The Card Container ──────────────────────────────────────────────
        self.container = ctk.CTkFrame(
            self,
            width=260,
            height=160,
            corner_radius=15,
            border_width=2,
            border_color=c.COLOR_PRIMARY,
            fg_color=("gray95", "gray20")
        )
        self.container.pack(fill="both", expand=True)
        
        # Load and prepare image
        if os.path.exists(image_path):
            self.raw_image = Image.open(image_path).convert("RGBA")
            self.raw_image = self.raw_image.resize(size, Image.Resampling.LANCZOS)
        else:
            self.raw_image = Image.new("RGBA", size, (255, 255, 255, 0))
            
        self.label = ctk.CTkLabel(self.container, text="", image=None)
        self.label.place(relx=0.5, rely=0.4, anchor="center")
        
        self.status_label = ctk.CTkLabel(
            self.container, 
            text=text, 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13, weight="bold")
        )
        self.status_label.place(relx=0.5, rely=0.7, anchor="center")
        
        self.tk_image = None

    def _center_window(self):
        """Center the toplevel relative to its master."""
        self.update_idletasks()
        width = 260
        height = 160
        
        # Get master window position and size
        m_x = self.master_window.winfo_x()
        m_y = self.master_window.winfo_y()
        m_w = self.master_window.winfo_width()
        m_h = self.master_window.winfo_height()
        
        x = m_x + (m_w // 2) - (width // 2)
        y = m_y + (m_h // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _rotate(self):
        """Internal loop to rotate the image."""
        if not self.is_spinning:
            return
            
        self.angle = (self.angle - 30) % 360
        rotated = self.raw_image.rotate(self.angle)
        
        self.tk_image = ctk.CTkImage(
            light_image=rotated, 
            dark_image=rotated, 
            size=self.size
        )
        self.label.configure(image=self.tk_image)
        self.after(self.speed_ms, self._rotate)

    def set_text(self, text: str):
        """Update the status text below the spinner."""
        self.status_label.configure(text=text)

    def start(self, text: str = None):
        """Start rotation and show as centered toplevel."""
        if text: self.set_text(text)
        self._center_window()
        self.deiconify()
        self.lift()
        self.focus_set()
        self.grab_set()  # Block interaction with main window
        
        if not self.is_spinning:
            self.is_spinning = True
            self._rotate()

    def stop(self):
        """Stop rotation and hide window."""
        self.is_spinning = False
        self.label.configure(image=None)
        self.grab_release()
        self.withdraw()
