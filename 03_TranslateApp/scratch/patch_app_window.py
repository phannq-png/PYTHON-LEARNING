import os

path = r'c:\Users\phann\OneDrive\Desktop\Project\Python-Learning\03_TranslateApp\src\ui\app_window.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update _on_page_selected
old_on_page = """        self.current_page_idx = index
        self.current_mismatches = [] # Reset on page change
        self.token_tracker.reset_page_counter()
        self._update_center_panel(self.current_page_idx)"""

new_on_page = """        self.current_page_idx = index
        page = self.current_session["pages"][index]
        self.current_mismatches = page.get("mismatches", []) # Load from session
        self.token_tracker.reset_page_counter()
        self._update_center_panel(self.current_page_idx)"""

if old_on_page in content:
    content = content.replace(old_on_page, new_on_page)
else:
    print("Warning: old_on_page not found")

# 2. Update _handle_consistency_check
old_check = """        page = self.current_session["pages"][self.current_page_idx]
        page["check_status"] = "error" if res else "ok"
        self.current_mismatches = res"""

new_check = """        page = self.current_session["pages"][self.current_page_idx]
        page["check_status"] = "error" if res else "ok"
        page["mismatches"] = res # Save to session
        self.current_mismatches = res"""

if old_check in content:
    content = content.replace(old_check, new_check)
else:
    print("Warning: old_check not found")

# 3. Update update_ui in _handle_check_all
old_ui = """                def update_ui(idx=page_idx, status=page["check_status"], mismatches=res):
                    p = self.current_session["pages"][idx]
                    self.left_sidebar.update_page_status(idx, True, status, p.get("is_reviewed", False))"""

new_ui = """                def update_ui(idx=page_idx, status=page["check_status"], mismatches=res):
                    p = self.current_session["pages"][idx]
                    p["mismatches"] = mismatches # Save to session
                    self.left_sidebar.update_page_status(idx, True, status, p.get("is_reviewed", False))"""

if old_ui in content:
    content = content.replace(old_ui, new_ui)
else:
    print("Warning: old_ui not found")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
