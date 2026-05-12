# REQUIREMENT SPECIFICATION DOCUMENT
## Japanese-Vietnamese Specialized Document Translation Application

---

## 1. PROJECT OVERVIEW

### 1.1 Application Information
- **Type**: Desktop Application
- **Language**: Python 3.10+
- **UI Framework**: CustomTkinter
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Purpose**: Translate specialized documents from Japanese to Vietnamese while preserving original formatting.

### 1.2 Main Processing Workflow
The application follows this conversion flow:
DOCX (JP) → Markdown → Segmentation → Translation → Markdown → DOCX (VN)

---

## 2. TECHNOLOGY STACK

### 2.1 Core Technologies
- **Python 3.10+**
- **CustomTkinter** (UI)
- **python-docx** (DOCX manipulation)
- **markdown** (Markdown conversion)
- **OpenAI API / Google Gemini API** (AI integration)
- **cryptography.fernet** (API key encryption)
- **JSON** (Local data storage)

---

## 3. DATA STRUCTURES

### 3.1 Glossary Data
Stored as JSON files per domain (medical, legal, common, etc.).
- JP Term -> VN Translation mapping.
- Metadata: creation and update timestamps.
- Import/Export format: CSV (JP_term, VN_term, domain).

### 3.2 Session Data
Stored as JSON files:
- Session ID (UUID).
- Original DOCX path.
- Selected Domain.
- Array of Pages (JP text, VN text, translated status, token usage).
- Total token usage and timestamps.

---

## 4. FUNCTIONAL REQUIREMENTS

### 4.1 Document Processing
- **Format Preservation**: Preservation of fonts, sizes, colors, bold/italic, tables, bullet points, and numbered lists.
- **Excluded**: Images, headers/footers (partial), track changes, comments.
- **Segmentation**: Segments must start with 【text】 patterns and must never be split across pages.

### 4.2 Main Translation Interface
- **Layout**: Top Bar (Upload, Domain, Export), Left Sidebar (Navigation), Center Panel (Split view: JP Read-only, VN Editable), Right Sidebar (Active Glossary), Bottom Bar (Actions, Tokens).
- **Navigation**: Page-by-page movement with auto-save.
- **Translation Actions**: AI Translate button, Get Prompt (Clipboard), Consistency Check.

### 4.3 Active Glossary (Right Sidebar)
- Displays only terms found in the current page.
- Interaction: Click to highlight all occurrences in the JP text panel.

### 4.4 Glossary Management
- Domain-based organization (Common vs. Specialized).
- CRUD operations with duplicate detection.
- **Bulk Import**: Paste JP terms list, AI translates, handles conflicts (Keep Old vs. Use New).

### 4.5 Domain Detection
- **Trigger Methods**:
    - **Automatic**: Triggered immediately after a successful DOCX upload.
    - **Manual**: Triggered by clicking the **✨** button next to the domain dropdown in the TopBar.
- **Processing Logic**:
    - AI analyzes a text sample (up to 5000 chars) and returns a domain name in **Vietnamese** (e.g., "Y tế", "Công nghệ thông tin").
    - **Match Found**: Automatically updates the dropdown selection.
    - **New Domain Found**:
        - Automatic Mode: Displays a suggestion popup.
        - Manual Mode: Automatically creates the new domain repository and selects it silently.
- **Manual Domain Addition**:
    - A **(+)** button next to the dropdown allows users to manually add a domain via a popup dialog.
    - **Validation**: If the domain exists, inform the user and select it. If new, create the repository and select it.
- **Feedback**: Displays Toast notifications in the Bottom Bar indicating the analysis status and result.

### 4.6 Consistency Checker
- Compares term counts between JP and VN text.
- Normalization: Case-insensitive for VN, width-sensitive (full-width/half-width) for JP.

### 4.7 Translation Engine
- Merges Common and Domain glossaries (Domain overrides).
- Strict glossary enforcement in AI prompts.

---

## 5. ERROR HANDLING
- Robust handling for File I/O, API authentication, and network timeouts.
- **Logging**: All errors logged to `data/logs/error.log` with rotation (10MB).

---

## 6. USER INTERFACE
- **Theme**: Default Dark Mode (#1E1E1E background).
- **Typography**: Support for both JP and VN characters.
- **Progress Indicators**: Mandatory for long operations (processing, translation, export).

---

## 7. DEPLOYMENT & QUALITY
- **Distribution**: Standalone executable (PyInstaller).
- **Testing**: Unit tests for core logic, Integration tests for full workflows, and Manual testing scenarios.

---
*Version 1.0.0 - Initial Specification (Translated from Vietnamese version)*
