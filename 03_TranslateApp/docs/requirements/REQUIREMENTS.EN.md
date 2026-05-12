# REQUIREMENT SPECIFICATION DOCUMENT (Version 1.2.0)
## Japanese-Vietnamese Specialized Document Translation Application

---

## 1. PROJECT OVERVIEW

### 1.1 Application Information
- **Type**: Desktop Application
- **Language**: Python 3.10+
- **UI Framework**: CustomTkinter
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Purpose**: Translate specialized documents from Japanese to Vietnamese while preserving 100% of the original formatting.

### 1.2 Main Processing Workflow
The application follows a standard transformation pipeline:
DOCX (Japanese) → Markdown → Segmentation → Translation → Markdown → DOCX (Vietnamese)

---

## 2. TECHNOLOGY STACK

### 2.1 Core Technologies
- **Programming Language**: Python 3.10 or higher
- **UI Framework**: CustomTkinter (Modern Python UI library)
- **Document Processing**: 
  - `python-docx` for DOCX manipulation
  - `markdown` for Markdown conversion
- **AI Integration**:
  - OpenAI API (GPT-4o, etc.)
  - Google Gemini API (Gemini 1.5 Flash/Pro)
- **Data Storage**: Local JSON files
- **Security**: `cryptography.fernet` for API key encryption

### 2.2 System Architecture
The application is built with four layers:

**Presentation Layer (UI)**
- Main Translation Window
- Glossary Management Interface
- API Settings Dialog
- Domain Detection/Suggestion Window

**Business Logic Layer**
- Document Processor (DOCX to/from Markdown)
- Translation Engine (AI-based translation)
- Terminology Matcher (Finding and highlighting terms)
- Consistency Checker (Validation logic)
- Session Manager (Save/Load progress)
- Token Tracker (API usage monitoring)

**Data Access Layer**
- Glossary Repository (CRUD operations)
- Configuration Manager (Encrypted storage)
- Session Repository (Persistence)

**External Services Layer**
- OpenAI/Gemini API Clients

---

## 3. DATA STRUCTURES

### 3.1 Glossary Data
Stored as JSON files per domain containing:
- Domain Name (e.g., "medical", "legal", "common")
- Dictionary mapping Japanese terms to Vietnamese translations
- Metadata (created_at, updated_at)

### 3.2 Session Data
Stored as JSON containing:
- Unique Session ID
- Original DOCX file path
- Selected Domain
- Array of Pages with:
  - Page ID
  - Japanese content
  - Vietnamese content
  - Translation status
  - Token count per page
  - **New in v1.2.0**: Persistence of term mismatch flags (X icons)

### 3.3 Configuration
Encrypted storage for:
- API Providers and Keys
- Default Model selection
- Global UI preferences (Appearance mode)

---

## 4. KEY FEATURES (v1.2.0)

### 4.1 Document Processing & Preservation
- **Formatting**: Full preservation of fonts, colors, sizes, bold/italic, tables, and lists.
- **Segmentation**: Smart splitting based on hard/soft returns and custom markers.

### 4.2 Translation & AI Integration
- **Specialized Translation**: AI-powered translation using domain-specific prompts.
- **Domain Detection**: Automatic content analysis to suggest the best glossary upon upload.
- **Bulk Import**: Automatically translate new terms in a glossary via AI.

### 4.3 UI/UX Excellence
- **Modern Design**: Dark Mode by default with 10px rounded corners.
- **Global Search**: Highlight terms across all pages with sidebar results.
- **Interactive Sidebar**: Click terms to toggle highlights in the text panel.
- **Startup Polish**: Application starts in **zoomed (maximized)** mode and restores this state after settings import.

### 4.4 Monitoring & Security
- **Daily Logging**: Timed rotating logs (`yyyyMMdd_app.log`, `yyyyMMdd_error.log`).
- **API Transparency**: Dedicated `api.log` for Prompt/Response tracking.
- **Token Tracking**: Real-time display of API cost/token usage.

---

## 5. ERROR HANDLING
- **Network Failures**: Failover mechanisms and user notifications.
- **Invalid API Keys**: Automatic start-up validation and disabling of failed keys.
- **System Logs**: Detailed error tracking in the `data/logs/` directory.

---
*Last Updated: 2026-05-12*
*Maintained by Antigravity Agent.*
