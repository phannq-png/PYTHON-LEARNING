# Task P4-AI-003: AI Domain Detection

## Metadata
- **Task ID**: P4-AI-003
- **Priority**: HIGH
- **Phase**: 4
- **Status**: closed
- **Dependencies**: P2-API-001, P1-DOC-001

## Description

### Purpose
Utilize AI to analyze text content and automatically suggest or set the appropriate domain. Supports both automatic detection during file upload and manual trigger via the UI.

### Scope
**Included:**
- [x] Dedicated AI prompt to identify domains in **Vietnamese** (e.g., "Y tế", "Công nghệ thông tin").
- [x] **Automatic Detection**: Triggered immediately after DOCX upload.
    - If domain exists: Automatically select it.
    - If domain is new: Show a suggestion dialog.
- [x] **Manual Trigger**: Added a **✨** button next to the domain dropdown in the TopBar.
    - When clicked: AI analyzes the current page.
    - If domain is new: **Automatically create and select** (no confirmation popup).
- [x] Display "Toast" notifications in the BottomBar during processing and on completion.

**Excluded:**
- Automatic translation of the entire glossary. Only creates the new domain container.

### Acceptance Criteria
- [x] AC1: Clicking the ✨ button on medical text automatically changes the dropdown to "Y tế".
- [x] AC2: When AI detects a new domain, the app automatically creates a new JSON file and selects it (Manual mode).
- [x] AC3: During file upload, a popup appears to suggest the domain (Automatic mode).

### Technical Notes
- AI is prompted to return Vietnamese names, concise (1-3 words), capitalized.
- Analyzes the first 5000 characters.
- Differentiation between Auto Flow (Popup) and Manual Flow (Silent Auto-create).

## Testing Checklist

### Manual Testing
- [x] Upload a document and verify the suggestion popup.
- [x] Click the ✨ button and verify the automatic creation of a new domain if not existing.
- [x] Verify that domain names are returned in Vietnamese.
