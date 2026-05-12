"""Bottom bar component — action buttons and token counter (placeholder)."""

from typing import Callable, Optional, List

import customtkinter as ctk
from src.utils import constants as c
from src.ui.components.tooltip import add_tooltip


class BottomBar(ctk.CTkFrame):
    """Bottom bar containing translation action buttons and token counter."""

    def __init__(
        self, 
        master: ctk.CTk, 
        on_check_page_callback: Optional[Callable[[], None]] = None,
        on_check_all_callback: Optional[Callable[[], None]] = None,
        on_translate_callback: Optional[Callable[[], None]] = None,
        on_translate_all_callback: Optional[Callable[[], None]] = None,
        on_get_prompt_callback: Optional[Callable[[], None]] = None,
        on_save_callback: Optional[Callable[[], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(
            master, 
            height=60, 
            fg_color=("gray90", "gray15"), 
            corner_radius=0, 
            **kwargs
        )
        self.on_check_page_callback = on_check_page_callback
        self.on_check_all_callback = on_check_all_callback
        self.on_translate_callback = on_translate_callback
        self.on_translate_all_callback = on_translate_all_callback
        self.on_get_prompt_callback = on_get_prompt_callback
        self.on_save_callback = on_save_callback
        self.pack_propagate(False)
        self._build_widgets()

    def _build_widgets(self) -> None:
        """Build action buttons and token counter label."""
        # ── Progress indicator (centered, hidden by default) ───────────────
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame, 
            width=250,
            corner_radius=c.CORNER_RADIUS,
            progress_color=c.COLOR_PRIMARY
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(side="top", fill="x")
        
        self.lbl_status = ctk.CTkLabel(
            self.progress_frame, 
            text="", 
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL),
            text_color=c.COLOR_PRIMARY
        )
        self.lbl_status.pack(side="top")
        
        # ── Action buttons (left side) ──────────────────────────────────────
        self.buttons: List[ctk.CTkButton] = []
        btn_configs = [
            ("⚡ Translate",     c.COLOR_PRIMARY,  self.on_translate_callback, "Dịch trang hiện tại"),
            ("✨ Translate All",  c.COLOR_AI,       self.on_translate_all_callback, "Dịch tất cả các trang chưa dịch"),
            ("📋 Get Prompt",    c.COLOR_WARNING,  self.on_get_prompt_callback, "Sao chép prompt dịch"),
            ("✅ Check Page",    "#2980B9",        self.on_check_page_callback, "Kiểm tra thuật ngữ trang này"),
            ("✔️ Check All",     "#16A085",        self.on_check_all_callback, "Kiểm tra thuật ngữ tất cả các trang"),
            ("💾 Save",          c.COLOR_SUCCESS,  self.on_save_callback, "Lưu tiến độ"),
        ]

        for label, color, cmd, tooltip_text in btn_configs:
            kwargs: dict = {
                "text": label, 
                "width": 125, # Slightly reduced width to fit 6 buttons
                "command": cmd,
                "corner_radius": c.CORNER_RADIUS,
                "font": ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL) # Smaller font
            }
            
            if color == "gray":
                kwargs["fg_color"] = ("gray75", "gray30")
                kwargs["hover_color"] = ("gray65", "gray40")
            else:
                kwargs["fg_color"] = color
            
            btn = ctk.CTkButton(self, **kwargs)
            btn.pack(side="left", padx=(c.PADDING_LARGE, 4), pady=c.PADDING_LARGE)
            add_tooltip(btn, tooltip_text)
            self.buttons.append(btn)

        # ── Token counter (right side) ──────────────────────────────────────
        self.lbl_tokens = ctk.CTkLabel(
            self,
            text="Tokens: — (Trang) | — (Tổng)",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL),
            text_color=("gray40", "gray60"),
        )
        self.lbl_tokens.pack(side="right", padx=(8, c.PADDING_LARGE), pady=10)

    # ── Progress Control ───────────────────────────────────────────────────

    def show_progress(self, text: str = "") -> None:
        """Display the progress bar and status text."""
        self.lbl_status.configure(text=text)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="top", fill="x")

        # Position it in the middle of the frame
        self.progress_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.set_buttons_state("disabled")

    def hide_progress(self) -> None:
        """Hide the progress bar and status text."""
        self.progress_frame.place_forget()
        self.set_buttons_state("normal")

    def set_progress(self, value: float, text: Optional[str] = None) -> None:
        """Update progress value (0.0 to 1.0) and optionally status text."""
        self.progress_bar.set(value)
        if text is not None:
            self.lbl_status.configure(text=text)

    def set_buttons_state(self, state: str) -> None:
        """Set all action buttons to 'normal' or 'disabled'."""
        for btn in self.buttons:
            btn.configure(state=state)

    # ── Placeholder callbacks ───────────────────────────────────────────────
    def _on_translate(self) -> None:
        """Placeholder: will be wired to translation engine."""
        pass

    def _on_get_prompt(self) -> None:
        """Placeholder: will be wired to prompt builder."""
        pass

    def _on_check_page(self) -> None:
        """Placeholder: will be wired to consistency checker."""
        pass

    def _on_save(self) -> None:
        """Placeholder: will be wired to session manager."""
        pass

    def update_tokens(self, status_text: str) -> None:
        """Update the token counter label with the provided status text."""
        self.lbl_tokens.configure(text=status_text)
