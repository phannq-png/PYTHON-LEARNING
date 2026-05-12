# REQUIREMENT SPECIFICATION DOCUMENT (Version 1.1.0)
## Japanese-Vietnamese Specialized Document Translation Application

---

## 1. PROJECT OVERVIEW
### 1.1 Application Information
- **Type**: Desktop Application
- **Language**: Python 3.10+
- **UI Framework**: CustomTkinter
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Purpose**: Translate specialized documents from Japanese to Vietnamese while preserving original formatting.

---

## 2. TECHNOLOGY STACK
- **Python 3.10+**, **CustomTkinter** (UI), **python-docx** (DOCX), **AI Clients** (Gemini/OpenAI), **cryptography.fernet** (Security).

---

## 3. KEY FEATURES (v1.1.0)

### 3.1 Document Processing
- **Format Preservation**: Full preservation of fonts, colors, tables, and lists.
- **Persistence**: Terminology mismatch results (X icons) and error lists are saved in the session and restored upon page navigation.

### 3.2 Main Translation Interface
- **Layout**: Top Bar (Search, Domain, Export), Left Sidebar (Page List, Legend), Center Panel (Split view), Right Sidebar (Active Glossary).
- **Global Search**: Search terms across all pages with yellow highlighting in both text and sidebar.
- **Collapsible Legend**: Sidebar status legend can be collapsed (🔼/🔽) to save space.

### 3.3 Glossary Management
- **Interactive Highlighting**: Click terminology in the sidebar to highlight occurrences (Toggle mode supported).
- **Bulk Import**: AI-powered terminology translation with conflict resolution.

### 3.4 Support & Help
- **Integrated User Guide**: Detailed instructions accessible via `Help -> User Guide`.
- **UI Refinement**: Action buttons (Check, Get Prompt) use high-contrast colors for better visibility.

---

## 4. ERROR HANDLING & LOGGING
- Timed rotating logs stored in `data/logs/app.log` and `error.log`.
- Critical failures trigger a recovery message for the user.

---

*Last Updated: 2026-05-12*
