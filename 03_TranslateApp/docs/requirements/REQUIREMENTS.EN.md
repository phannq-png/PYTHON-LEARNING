# REQUIREMENT SPECIFICATION DOCUMENT
## Japanese-Vietnamese Technical Document Translation Application

---

## 1. PROJECT OVERVIEW

### 1.1 Application Information
- **Application Type**: Desktop Application
- **Programming Language**: Python 3.10+
- **UI Framework**: CustomTkinter
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Purpose**: Translate technical documents from Japanese to Vietnamese while preserving document formatting

### 1.2 Main Workflow
The application follows this conversion flow:
DOCX (Japanese) → Markdown → Segmentation → Translation → Markdown → DOCX (Vietnamese)

---

## 2. TECHNOLOGY STACK

### 2.1 Core Technologies
- **Programming Language**: Python 3.10 or higher
- **UI Framework**: CustomTkinter (modern Python UI library)
- **Document Processing**: 
  - python-docx for DOCX file manipulation
  - markdown for Markdown conversion
- **AI Integration**:
  - OpenAI API
  - Google Gemini API
- **Data Storage**: JSON files stored locally
- **Security**: cryptography.fernet for API key encryption

### 2.2 System Architecture
The application is built with four layers:

**Presentation Layer (UI)**
- Main translation window
- Glossary management interface
- API settings interface
- Domain detection interface

**Business Logic Layer**
- Document processor (DOCX to Markdown conversion)
- Translation engine (AI-powered translation)
- Glossary matcher (term finding and highlighting)
- Consistency checker (validation)
- Session manager (save/load progress)
- Token tracker (API usage monitoring)

**Data Access Layer**
- Glossary repository (CRUD operations)
- Configuration manager (encrypted storage)
- Session repository (progress persistence)

**External Services Layer**
- OpenAI/Gemini API clients

---

## 3. DATA STRUCTURES

### 3.1 Glossary Data
Each glossary is stored as a JSON file containing:
- Domain name (e.g., "medical", "legal", "common")
- Dictionary of Japanese terms mapped to Vietnamese translations
- Creation timestamp
- Last update timestamp

**CSV Format for Import/Export**:
Each line contains: Japanese term, Vietnamese term, domain name

### 3.2 Session Data
Session files store:
- Unique session identifier
- Path to original DOCX file
- Selected domain
- Array of pages with:
  - Page ID number
  - Japanese text content
  - Vietnamese text content
  - Translation status (completed or not)
  - Token count used for that page
- Current active page number
- Total tokens used across all pages
- Creation and modification timestamps

### 3.3 API Configuration
Encrypted configuration file stores:
- **Translation API settings**:
  - Provider name (OpenAI or Gemini)
  - Encrypted API key
  - Selected model name
- **Domain Detection API settings**:
  - Provider name
  - Encrypted API key
  - Selected model name

---

## 4. FEATURE REQUIREMENTS

### 4.1 Document Processing

#### 4.1.1 Format Preservation
The application must preserve the following formatting elements:
- Font family and size
- Text color
- Bold and italic styles
- Table structures
- Bullet points
- Numbered lists

**Not Supported**:
- Images (will be ignored, not processed)
- Headers and footers (may not preserve perfectly)
- Track changes and comments

#### 4.1.2 Document Conversion Rules
- Convert DOCX to Markdown while storing format metadata
- Store format information separately for reverse conversion
- Each paragraph's format (font, size, color, styles) must be preserved
- When converting back to DOCX, apply stored formatting to Vietnamese text

#### 4.1.3 Text Segmentation
- Each segment begins with the pattern 【text】
- Examples: 【序論】, 【方法】, 【結果】
- Segments must never be split in the middle
- Always keep complete segments intact
- If a segment is very long, keep it as a single unit

#### 4.1.4 Page Creation
- Minimum: 1 segment per page
- Maximum: As many segments as can fit without requiring vertical scrolling
- Calculate based on estimated text height
- Goal: No scroll bar needed within each page view

---

### 4.2 Main Translation Interface

#### 4.2.1 Layout Structure
The main window is divided into:
- **Top Bar**: File upload button, Domain selection dropdown, Export button
- **Left Sidebar**: Page navigation list
- **Center Panel (Split Horizontal)**:
  - Top: Japanese text (read-only display)
  - Bottom: Vietnamese text (editable text area)
  - Horizontal separator bar between them
- **Right Sidebar**: Active glossary terms for current page
- **Bottom Bar**: Action buttons and token counter

#### 4.2.2 Display Requirements
- Split orientation: Horizontal (Japanese above, Vietnamese below)
- No synchronized scrolling between Japanese and Vietnamese panels
- Japanese text area is read-only
- Vietnamese text area is fully editable
- Default theme: Dark mode

#### 4.2.3 Page Navigation
- Display format: ◀ [Current Page Number]/[Total Pages] ▶
- Click arrow buttons to move between pages
- Click page number in left sidebar to jump directly
- Auto-save current page when navigating to another page

#### 4.2.4 Button Functions

**Translate Button**
- Sends Japanese text to AI API with glossary enforcement
- Displays progress bar during API call
- Updates Vietnamese text area with translation result
- Tracks and records tokens used
- Shows error message if API call fails (no automatic retry)

**Get Prompt Button**
- Generates complete translation prompt including glossary
- Copies prompt to clipboard
- Displays prompt in a dialog window
- User can manually copy to ChatGPT, Gemini, or other AI tools

**Check Page Button**
- Runs consistency validation on current page
- Compares glossary term frequency between Japanese and Vietnamese
- Shows popup dialog with check results
- Lists any mismatches found

**Save Button**
- Saves entire session to JSON file
- Includes all pages and their translation status
- Updates last modified timestamp
- Confirms save completion to user

---

### 4.3 Right Sidebar - Active Glossary Display

#### 4.3.1 Display Rules
- Shows only glossary terms that appear in the current page
- Updates automatically when switching pages
- Display format for each term:
  - Checkmark indicator
  - Japanese term
  - Arrow symbol
  - Vietnamese translation
- Shows occurrence count in parentheses

#### 4.3.2 Interactive Features
- Click on any term to jump to first occurrence in text
- Highlight all occurrences of the clicked term
- Clicking again removes highlighting
- Visual indication of which term is currently selected

---

### 4.4 Glossary Management System

#### 4.4.1 Domain Organization
- **Common Domain**: Automatically applied to all other domains
- **Specific Domains**: medical, legal, IT, engineering, etc.
- **Priority Rule**: Specific domain glossary overrides Common glossary
- Users can create custom domains as needed

#### 4.4.2 Glossary Manager Interface
The glossary manager window contains:
- Domain tabs at the top for switching between domains
- Action buttons: Add, Delete, Import CSV, Export CSV, Bulk Import
- Table displaying all terms with columns:
  - Japanese term
  - Vietnamese translation
  - Domain name
  - Actions (Edit, Delete buttons)

#### 4.4.3 CRUD Operations

**Add Term**
- Single term entry form
- Fields: Japanese term, Vietnamese translation
- Duplicate check before saving
- Error message if duplicate exists in same domain

**Edit Term**
- Click Edit button or double-click table row
- Inline editing in table
- Save changes immediately
- Validate for duplicates

**Delete Term**
- Single deletion: Click Delete button on specific row
- Batch deletion: Select multiple rows and delete
- Confirmation dialog before deleting
- Cannot undo deletion

**Delete All**
- Button to clear all terms in current domain
- Confirmation dialog with warning
- Does not affect other domains

**Duplicate Detection**
- No duplicate Japanese terms allowed within the same domain
- Duplicates across different domains are permitted
- Case-sensitive checking for Japanese terms
- Display error message showing existing term

#### 4.4.4 Import and Export

**Import CSV**
- Accept CSV files with format: JP_term, VN_term, domain
- Parse each line and validate format
- Check for duplicates against existing glossary
- For conflicts:
  - Show confirmation dialog
  - List all conflicting terms
  - Allow user to choose: Skip, Replace, or Cancel
- Import successful entries
- Display summary of imported, skipped, and failed entries

**Export CSV**
- Export current domain only or all domains
- Generate CSV file with proper encoding (UTF-8)
- Include header row: JP_term, VN_term, domain
- **Security requirement**: Never include API keys in export file
- Allow user to choose save location

#### 4.4.5 Bulk Import with AI Translation

**Workflow**
1. User opens bulk import dialog
2. Pastes list of Japanese terms (one per line)
3. Clicks "Translate & Import" button
4. System calls AI API to translate all terms in batch
5. For each translated term:
   - **If term is new**: Automatically add to glossary
   - **If term exists with same translation**: Skip silently
   - **If term exists with different translation**:
     - Pause and show confirmation dialog
     - Display both old and new translations
     - User chooses: Keep Old or Use New
6. Save all accepted terms to glossary
7. Display summary of results

**User Interface Flow**
- Text area for pasting Japanese terms
- AI Translate button
- Progress indicator during translation
- Review dialog showing:
  - New terms (auto-accepted)
  - Conflicts requiring user decision
  - Options for each conflict: Keep Old / Use New
- Confirm All button to complete import

---

### 4.5 Domain Detection Feature

#### 4.5.1 Detection Methods
Users can trigger domain detection by:
- Selecting a page from the main interface
- Pasting a text sample into the domain detector

#### 4.5.2 Detection Workflow
1. User provides input (page selection or text paste)
2. System calls Domain Detection API
3. AI analyzes text and suggests domain name
4. System searches existing domains for a match
5. If match found: Display matched domain name
6. If no match: Suggest creating new domain with AI-provided name
7. User confirms or edits domain name
8. System loads corresponding glossary for that domain

#### 4.5.3 Domain Matching Logic
- AI returns suggested domain name (e.g., "Medical", "Legal")
- System performs case-insensitive search in existing domains
- Fuzzy matching to find close matches
- If confidence is high: Auto-select matched domain
- If confidence is low: Show multiple suggestions for user to choose

#### 4.5.4 New Domain Creation
- AI suggests domain name based on text content
- User can accept or edit the suggested name
- System creates new empty glossary file for that domain
- **Important**: No automatic template glossary is created
- New domain appears in domain list immediately
- User must manually add terms to new domain

---

### 4.6 Consistency Checker

#### 4.6.1 Validation Algorithm
For each glossary term, the checker performs:
1. Count total occurrences in Japanese text
2. Count total occurrences in Vietnamese text
3. Compare the two counts
4. Record mismatch if counts differ

**Normalization Rules**
- **Case Sensitivity**: 
  - Vietnamese: Ignore case differences
  - "Hệ thống" equals "hệ thống"
  - "HỆ THỐNG" equals "hệ thống"
- **Fullwidth/Halfwidth (Japanese)**:
  - Distinguish between fullwidth and halfwidth characters
  - "システム" (fullwidth) is NOT equal to "システム" (halfwidth)
  - Must match exactly
- **Fullwidth/Halfwidth (Vietnamese)**:
  - No distinction needed (Vietnamese doesn't use these)

#### 4.6.2 Result Display
After checking, show popup dialog with:
- Success message if all terms match
- List of mismatches if any found
- For each mismatch:
  - Japanese term
  - Vietnamese term
  - Occurrence count in Japanese text
  - Occurrence count in Vietnamese text
- Close button to dismiss dialog
- Option to export results to file (future enhancement)

**Example Popup Content**
- Title: "Consistency Check - Page 1"
- Status: "Found 2 mismatches"
- Mismatch 1:
  - Term: システム → Hệ thống
  - Japanese: 5 occurrences
  - Vietnamese: 4 occurrences
- Mismatch 2:
  - Term: 診断 → Chẩn đoán
  - Japanese: 3 occurrences
  - Vietnamese: 2 occurrences

---

### 4.7 Translation Engine

#### 4.7.1 Glossary Enforcement in Translation
The translation engine must:
- Merge Common and Domain glossaries before translation
- Apply domain glossary priority over common glossary
- Generate prompt that strictly enforces glossary usage
- Include all glossary terms in the API prompt
- Instruct AI to use exact translations from glossary
- Preserve 【】 markers in their original positions
- Maintain natural Vietnamese grammar

#### 4.7.2 Glossary Merging Logic
When preparing for translation:
1. Load Common domain glossary
2. Load selected Domain glossary
3. Create merged dictionary
4. For conflicts: Domain glossary overrides Common
5. Use merged glossary for translation

**Example**
- Common glossary: {"システム": "Hệ thống"}
- Medical glossary: {"システム": "Hệ thống y tế"}
- Merged result: {"システム": "Hệ thống y tế"} (Medical wins)

#### 4.7.3 Translation Prompt Structure
The prompt sent to AI must include:
- Role definition (professional translator)
- Critical glossary rules section
- List of all glossary terms with translations
- Instruction to strictly follow glossary
- Instruction to maintain formatting markers
- The Japanese text to translate
- Request for Vietnamese translation output

---

### 4.8 API Management

#### 4.8.1 Dual API Configuration
The application requires two separate API configurations:

**Translation API**
- Used for: Translating document content
- Configurable provider: OpenAI or Gemini
- User selects specific model (e.g., gpt-4o, gemini-1.5-pro)

**Domain Detection API**
- Used for: Identifying document domain/subject area
- Configurable provider: OpenAI or Gemini
- User selects specific model (typically lighter/faster model)

#### 4.8.2 API Settings Interface
The API settings window contains:
- Two separate configuration sections (Translation and Domain Detection)
- For each API:
  - Provider dropdown (OpenAI / Gemini)
  - API Key text field (password-masked)
  - Model selection dropdown
- Import/Export configuration buttons
- Save and Cancel buttons

#### 4.8.3 Security Requirements
- All API keys must be encrypted before storage
- Use Fernet symmetric encryption from cryptography library
- Encryption key stored in separate file: data/config/.secret.key
- Never expose API keys in UI (show as masked: **********)
- API keys never included in exported glossary files
- API keys never included in session files
- API keys never written to log files

#### 4.8.4 Token Usage Tracking
The application must track:
- **Per-page token usage**: Tokens consumed for each page translation
- **Total token usage**: Sum of all pages in current session
- Display format: "Tokens: 1.5K (Page) | 15.2K (Total)"
- Track separately for Translation API and Domain Detection API
- Store token counts in session data
- Display in bottom bar of main window

**No Rate Limiting**
- Do not impose artificial limits on API calls
- Track usage for information purposes only
- Let API provider handle rate limiting
- Display usage to help user manage costs

---

### 4.9 Session Management

#### 4.9.1 Session Data Content
Each session stores:
- Unique session ID (UUID)
- Path to original DOCX file
- Selected domain name
- Complete page array with:
  - Page ID
  - Japanese text
  - Vietnamese text
  - Translation completion status
  - Tokens used
- Current active page number
- Total tokens used
- Session creation timestamp
- Last modification timestamp

#### 4.9.2 Session Save Behavior
Sessions are automatically saved when:
- User clicks Save button
- User navigates to different page
- User closes the application
- Every 5 minutes (auto-save timer)

Session save process:
- Serialize current state to JSON
- Write to file: data/sessions/{session_id}.json
- Update last_modified timestamp
- Show brief confirmation (toast notification)

#### 4.9.3 Session Load Behavior
On application startup:
- Check for existing session files
- If session exists:
  - Display "Resume last session?" dialog
  - Show session info: filename, date, progress percentage
  - Options: Resume or Start New
- If user resumes:
  - Load complete session data
  - Restore page position
  - Restore all translations
  - Continue from where user left off

#### 4.9.4 Single Session Limitation
- Only one session can be active at a time
- Opening new file prompts to save current session
- Cannot work on multiple documents simultaneously
- Session switching requires save or discard confirmation

---

### 4.10 Export Functionality

#### 4.10.1 Export Options
Export dialog provides:
- **Checkbox**: Export only translated pages
  - When checked: Only pages with is_translated=true are exported
  - When unchecked: All pages exported (empty for untranslated)
- **Checkbox**: Export bilingual version
  - When checked: Each segment shows JP then VN
  - When unchecked: Only Vietnamese text
- **File path selector**: Choose output location and filename
- **Export button**: Execute export
- **Cancel button**: Close without exporting

#### 4.10.2 Export Processing Rules
Standard Export (Vietnamese only):
- Take each translated page
- Apply stored format metadata to Vietnamese text
- Preserve font, size, color from original
- Maintain table structures
- Preserve bullet points and numbering
- Skip untranslated pages if option selected

Bilingual Export:
- For each segment:
  - Insert Japanese paragraph
  - Insert Vietnamese paragraph below
  - Apply original formatting to both
  - Add subtle separator or spacing
- Alternate throughout document

#### 4.10.3 Format Preservation During Export
The export process must:
- Retrieve format metadata stored during import
- Apply font family to Vietnamese text
- Apply font size to Vietnamese text
- Apply text color (RGB values)
- Apply bold/italic styles
- Recreate table structures with same column widths
- Preserve bullet point styles
- Preserve numbering formats
- Maintain paragraph spacing and indentation

---

## 5. ERROR HANDLING

### 5.1 File Operation Errors

**Invalid DOCX File**
- Detect corrupted or invalid DOCX files
- Display specific error message explaining the issue
- Examples: "File is corrupted", "Not a valid DOCX format"
- Suggest user actions: check file, try re-saving, convert from DOC

**File Permission Errors**
- Detect when file cannot be read
- Display error: "Cannot access file. Check file permissions."
- Suggest closing file in other applications

**Large File Warning**
- For files over 100 pages:
  - Show warning dialog
  - Estimate processing time
  - Display progress bar during processing
  - Allow user to cancel

### 5.2 API Operation Errors

**Invalid API Key**
- Detect authentication failures
- Display error message: "Invalid API key for [Provider]"
- Automatically open API Settings dialog
- Highlight the problematic API key field

**Network Timeout**
- Detect network timeout errors
- Display error message with timeout duration
- **Do not automatically retry**
- Provide Retry button for user to manually retry

**API Rate Limit**
- Detect rate limit errors from provider
- Display error with rate limit details
- Show estimated wait time if provided
- Suggest user wait or check API quota

**Invalid API Response**
- Detect malformed or unexpected responses
- Log full error details to error.log
- Display user-friendly message: "Translation failed. Please try again."
- Offer to save partial results

### 5.3 Data Operation Errors

**Glossary Duplicate**
- Prevent saving duplicate terms in same domain
- Highlight the duplicate entry
- Show existing term with same Japanese text
- Offer to edit existing term instead

**Invalid CSV Format**
- Detect malformed CSV during import
- Show error with specific line number
- Display expected format example
- Allow user to fix file and retry

**Session Load Failure**
- Detect corrupted session files
- Display error: "Cannot load saved session"
- Offer to start fresh session
- Option to attempt recovery or delete corrupted session

### 5.4 Error Logging
- All errors logged to: data/logs/error.log
- Log format includes:
  - Timestamp
  - Error type
  - Error message
  - Stack trace (for developers)
  - User action at time of error
- Log file auto-rotates when exceeds 10MB
- Keep last 5 log files

---

## 6. USER INTERFACE REQUIREMENTS

### 6.1 Visual Design

**Theme**
- Default: Dark mode
- Color scheme: Modern, high contrast
- Background: Dark gray (#1E1E1E)
- Text: Light gray (#CCCCCC)
- Accent color: Blue (#0078D4)
- Error color: Red (#E74856)
- Success color: Green (#107C10)

**Typography**
- System default font
- Must support Japanese characters (MS Gothic, Yu Gothic, etc.)
- Must support Vietnamese characters with diacritics
- Font sizes: 
  - Body text: 11pt
  - Headers: 14pt
  - UI labels: 9pt

**Spacing**
- Consistent padding: 8px standard, 16px large
- Margins between sections: 16px
- Button spacing: 8px between buttons

### 6.2 Progress Indicators

**Progress Bar Required For**
- File upload and DOCX to Markdown conversion
- API translation calls (per page)
- Bulk import translation (batch processing)
- DOCX export generation
- Large file processing (over 100 pages)

**Progress Bar Format**
- Horizontal bar with percentage
- Descriptive text below bar
- Example: "[████████░░] 80% - Translating page 20/25"
- Estimated time remaining (when calculable)
- Cancel button where appropriate

**Loading States**
- Spinner for short operations (under 3 seconds)
- Disable UI elements during processing
- Change cursor to loading cursor
- Prevent user interaction during critical operations

### 6.3 Window Behavior

**Main Window**
- Minimum size: 1200px width × 800px height
- Resizable by user
- Remember last size and position
- Restore on application restart

**Panel Resizing**
- Left sidebar: Resizable, minimum 150px
- Right sidebar: Resizable, minimum 200px
- Center panels: Resizable between JP and VN
- Draggable separator bars

**Responsive Layout**
- Adapt to window size changes
- Maintain minimum readable sizes
- Collapse sidebars when window too small
- Show collapse/expand buttons

### 6.4 Interaction Requirements

**No Keyboard Shortcuts**
- All interactions via mouse/buttons
- No keyboard shortcut implementation required
- Standard text editing shortcuts work in text areas (Ctrl+C, Ctrl+V, etc.)

**Button States**
- Normal, Hover, Pressed, Disabled
- Visual feedback on click
- Disable buttons during processing
- Tooltip on hover showing button function

**Dialog Behavior**
- Modal dialogs block main window
- Non-modal dialogs allow background interaction
- Confirmation dialogs for destructive actions
- ESC key closes dialogs (where appropriate)

---

## 7. FILE ORGANIZATION

### 7.1 Directory Structure
The application creates and manages these directories:

**Root Directory**
- main.py: Application entry point
- requirements.txt: Python dependencies
- README.md: User documentation
- .gitignore: Git ignore rules

**data/ Directory** (Created on first run, excluded from git)
- glossary/: All glossary JSON files
  - common.json
  - medical.json
  - legal.json
  - it.json
  - (user-created domains)
- sessions/: Session save files
  - {session_id}.json for each session
- config/: Configuration files
  - .secret.key: Encryption key (CRITICAL: never commit)
  - api_config.json: Encrypted API settings
- temp/: Temporary working files
  - Cleared on application close
- logs/: Error and activity logs
  - error.log: Error logging

**src/ Directory** (Source code)
- ui/: User interface components
- core/: Business logic modules
- data/: Data access layer
- utils/: Utility functions

**tests/ Directory** (Unit tests)
- Test files for each module

### 7.2 File Naming Conventions
- Session files: session_{timestamp}_{uuid}.json
- Exported files: {original_name}_vn.docx or {original_name}_bilingual.docx
- Log files: error_{date}.log
- Glossary files: {domain_name}.json

---

## 8. DEPENDENCIES

### 8.1 Required Python Packages
The application requires these Python packages:

**UI Framework**
- customtkinter version 5.2.0 or higher

**Document Processing**
- python-docx version 1.1.0 or higher
- markdown version 3.5.1 or higher

**AI Integration**
- openai version 1.12.0 or higher
- google-generativeai version 0.3.2 or higher

**Security**
- cryptography version 41.0.7 or higher

**Utilities**
- python-dateutil version 2.8.2 or higher

**Testing**
- pytest version 7.4.3 or higher
- pytest-cov version 4.1.0 or higher

### 8.2 Python Version
- Minimum: Python 3.10
- Recommended: Python 3.11 or higher
- Not compatible with: Python 3.9 or lower

### 8.3 Operating System
- Windows 10 or higher
- macOS 10.15 or higher
- Linux (Ubuntu 20.04 or equivalent)

---

## 9. IMPLEMENTATION PRIORITIES

### Phase 1: Foundation (CRITICAL - Must Complete First)
These features are essential for basic functionality:
1. Project structure setup and configuration
2. Document processor (DOCX to Markdown conversion)
3. Text segmentation by 【text】 pattern
4. Basic UI skeleton with CustomTkinter
5. Configuration manager with encryption

### Phase 2: Core Features (HIGH - Primary Functionality)
These features enable core translation workflow:
6. Glossary repository with JSON storage
7. Main translation UI (JP/VN split view)
8. API integration for translation
9. Page navigation system
10. Session save and load functionality

### Phase 3: Advanced Features (MEDIUM - Enhanced Functionality)
These features improve usability and efficiency:
11. Glossary manager user interface
12. Bulk import with AI translation
13. Consistency checker implementation
14. Right sidebar glossary display
15. Export to DOCX with format preservation

### Phase 4: Polish (LOW - Nice to Have)
These features enhance user experience:
16. Domain detection feature
17. Token tracking display
18. Progress bars and loading indicators
19. Comprehensive error handling
20. Dark mode theming refinement

---

## 10. TESTING REQUIREMENTS

### 10.1 Unit Testing
Required unit tests for:
- Document processor (conversion accuracy)
- Glossary operations (CRUD, merge, duplicate detection)
- Consistency checker (term counting with normalization)
- Session save and load functionality
- API client error handling
- Encryption and decryption

### 10.2 Integration Testing
Required integration tests for:
- Complete translation workflow end-to-end
- API integration with mocked responses
- UI component interactions
- Data persistence across sessions
- Multi-page document processing

### 10.3 Manual Testing Checklist
Before release, manually verify:
- Upload various DOCX formats and sizes
- Test with document over 100 pages
- Verify format preservation (fonts, colors, tables)
- Test glossary bulk import with term conflicts
- Verify consistency checker accuracy on various texts
- Test session resume after forced application close
- Export bilingual document and verify formatting
- Test all API error scenarios
- Verify encryption of API keys
- Test on different operating systems
- Verify Japanese and Vietnamese character rendering

---

## 11. KNOWN LIMITATIONS

Users should be aware of these limitations:

### 11.1 Document Features Not Supported
- **Images**: Ignored and not included in translation
- **Headers and Footers**: May not preserve perfectly in all cases
- **Track Changes**: Not supported, changes will be accepted
- **Comments**: Not preserved in translation
- **Embedded Objects**: Charts, diagrams will be ignored
- **Macros**: Will be removed during conversion

### 11.2 Performance Limitations
- **Large Files**: Documents over 100 pages may be slow
- **Memory Usage**: Very large documents may consume significant RAM
- **API Speed**: Translation speed depends on API provider response time

### 11.3 Functional Limitations
- **Single Session**: Cannot work on multiple documents simultaneously
- **Internet Required**: Must have internet connection for API calls
- **API Dependencies**: Features depend on external API availability
- **Manual Review**: AI translation may require human review for accuracy

### 11.4 Technical Limitations
- **Complex Tables**: Very complex table formatting may have minor issues
- **Custom Fonts**: Non-standard fonts may not preserve if not installed
- **Right-to-Left Text**: Not designed for RTL languages
- **Mixed Languages**: Best for primarily Japanese documents

---

## 12. FUTURE ENHANCEMENTS (OUT OF SCOPE)

These features are not included in current version but may be considered for future releases:

### 12.1 Batch Processing
- Process multiple documents in queue
- Automated batch translation overnight
- Batch export of multiple documents

### 12.2 Cloud Integration
- Cloud storage for glossaries (Google Drive, Dropbox)
- Cloud backup of sessions
- Sync glossaries across devices

### 12.3 Collaboration Features
- Multi-user translation projects
- Real-time collaboration
- Comment and review system
- Version control for translations

### 12.4 Advanced AI Features
- Custom AI model training
- Domain auto-detection improvement
- Translation quality scoring
- Automated post-editing suggestions

### 12.5 Additional Formats
- PDF export with searchable text
- HTML export for web publishing
- XLIFF format for CAT tools
- TMX format for translation memory

### 12.6 Enhanced UI
- Mobile app version
- Web-based interface
- Light theme option
- Customizable color schemes
- Configurable keyboard shortcuts

---

## 13. DEPLOYMENT

### 13.1 Distribution Format
- Standalone executable (no Python installation required)
- Packaged using PyInstaller
- All dependencies bundled
- Single-file executable preferred

### 13.2 Installation Process
- Download executable file
- No installation wizard needed
- Portable mode (run from any directory)
- First-run setup wizard for API configuration
- Create data directories automatically

### 13.3 Update Mechanism
- Manual download and replace executable
- Display current version in About dialog
- Optional: Check for updates on startup (future enhancement)

### 13.4 Uninstallation
- Delete executable file
- Optionally delete data directory
- No registry entries or system modifications
- Clean uninstall without residue

---

## 14. GLOSSARY OF TECHNICAL TERMS

### Application-Specific Terms

| Term | Japanese | Vietnamese | Description |
|------|----------|------------|-------------|
| Segment | 段落 (danraku) | Đoạn văn | Text block starting with 【text】 marker |
| Domain | 分野 (bunya) | Lĩnh vực | Subject area or field of expertise |
| Glossary | 用語集 (yōgoshū) | Bộ thuật ngữ | Dictionary of specialized terms |
| Page | ページ (pēji) | Trang | UI page containing one or more segments |
| Session | セッション (sesshon) | Phiên làm việc | Saved work state with progress |
| Consistency | 一貫性 (ikkansei) | Tính nhất quán | Term usage matching between languages |

### Technical Terms

| Term | Description |
|------|-------------|
| DOCX | Microsoft Word Open XML document format |
| Markdown | Lightweight markup language for formatting |
| API | Application Programming Interface |
| Token | Unit of text processed by AI (roughly 4 characters) |
| Encryption | Process of encoding data for security |
| JSON | JavaScript Object Notation (data format) |
| CSV | Comma-Separated Values (spreadsheet format) |

---

## 15. QUALITY STANDARDS

### 15.1 Translation Quality
- Glossary terms must be applied 100% consistently
- Natural Vietnamese grammar required
- Preserve technical accuracy
- Maintain original meaning and tone

### 15.2 Format Preservation
- Fonts must match original exactly
- Colors must be preserved accurately
- Table structures must remain intact
- Bullet and numbering styles must match

### 15.3 Application Performance
- Application startup: Under 5 seconds
- Page navigation: Instant (under 0.5 seconds)
- Save operation: Under 2 seconds
- API response handling: Display within 1 second of receiving

### 15.4 Reliability
- Zero data loss during normal operation
- Auto-save prevents work loss
- Session recovery after unexpected close
- Error logging for all failures

### 15.5 Security
- API keys encrypted at rest
- No sensitive data in logs
- No data transmitted except to chosen AI provider
- Secure deletion of temporary files

---

## 16. DOCUMENTATION REQUIREMENTS

### 16.1 User Documentation
Must include:
- Installation guide
- Getting started tutorial
- Feature explanations with screenshots
- Glossary management guide
- API configuration instructions
- Troubleshooting common issues
- FAQ section

### 16.2 Technical Documentation
Must include:
- Architecture overview
- Data structure specifications
- API integration details
- File format specifications
- Error code reference
- Development setup guide

### 16.3 Video Tutorials
Recommended topics:
- First-time setup and configuration
- Basic translation workflow
- Glossary management
- Bulk import usage
- Consistency checking

---

## 17. SUPPORT AND MAINTENANCE

### 17.1 User Support
- README file with common issues
- Error messages with helpful suggestions
- Built-in help documentation
- FAQ section in application

### 17.2 Maintenance Plan
- Bug fixes as needed
- Security updates for dependencies
- Compatibility updates for new OS versions
- API integration updates for provider changes

### 17.3 Feedback Collection
- In-app feedback button (future)
- Error report generation
- Usage statistics (opt-in only)

---

## 18. COMPLIANCE AND STANDARDS

### 18.1 Data Privacy
- No data sent to external servers except AI APIs
- User controls all data locally
- No telemetry or analytics
- API keys never shared

### 18.2 Licensing
- Clear license terms for software
- Attribution for open-source dependencies
- User agreement for AI API usage

### 18.3 Accessibility
- High contrast UI for visibility
- Resizable text areas
- Clear error messages
- Keyboard navigation in text fields

---

## VERSION HISTORY

- **Version 1.0.0** - Initial specification document
- **Date**: 2024-01-XX
- **Status**: Draft for Development

---

## DOCUMENT CONTROL

- **Document Type**: Requirements Specification
- **Purpose**: Guide software development
- **Audience**: Development team, project stakeholders
- **Maintenance**: Update as requirements evolve
- **Approval Required**: Yes, before implementation begins

---

**END OF REQUIREMENTS SPECIFICATION**

This document defines all requirements for the Japanese-Vietnamese Technical Document Translation Application. Implementation must follow this specification. Changes require documentation and version updates.