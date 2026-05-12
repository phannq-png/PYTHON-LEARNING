"""Tooltip helper for CustomTkinter widgets."""

import tkinter as tk
import customtkinter as ctk

class Tooltip:
    """A simple tooltip that shows a text when hovering over a widget."""
    
    def __init__(self, widget: tk.Widget, text: str, delay: int = 500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.id = None
        
        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)
        self.widget.bind("<ButtonPress>", self._on_leave)

    def _on_enter(self, event=None):
        self._schedule()

    def _on_leave(self, event=None):
        self._unschedule()
        self._hide()

    def _schedule(self):
        self._unschedule()
        self.id = self.widget.after(self.delay, self._show)

    def _unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def _show(self):
        if self.tooltip_window:
            return
        
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        # Create toplevel window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True) # Remove borders
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(
            self.tooltip_window, 
            text=self.text, 
            justify='left',
            background="#2b2b2b", # Dark grey consistent with CTk
            foreground="#ffffff",
            relief='solid', 
            borderwidth=1,
            font=("Inter", 9, "normal"),
            padx=5,
            pady=3
        )
        label.pack()

    def _hide(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def add_tooltip(widget, text):
    """Convenience function to add a tooltip to a widget."""
    return Tooltip(widget, text)
