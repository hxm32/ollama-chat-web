# Ollama Chat

A lightweight, single-file web UI for chatting with local or remote Ollama models.

Built with plain HTML, CSS, and JavaScript - no build tools, frameworks, or backend required.

![License](https://img.shields.io/badge/license-MIT-blue)
![Ollama](https://img.shields.io/badge/Ollama-Compatible-green)

## Features

### Chat Experience

* Multi-conversation chat history
* Automatic conversation persistence
* Edit and resend previous messages
* Regenerate assistant responses
* Delete individual messages
* Copy messages with one click
* Streaming responses with live token statistics
* Stop generation mid-response
* Chat search
* Manual conversation renaming
* Export chats to JSON
* Import chats from JSON backups
  
### Model Controls

* Automatic Ollama model discovery
* Model selector
* Custom system prompts
* Optional thinking/reasoning mode
* Adjustable generation parameters:

  * Max tokens
  * Context size
  * Temperature
  * Top-p
  * Seed
  * Keep-alive duration

### Remote Access

Connect to Ollama running on another machine via SSH tunneling.

The interface generates the SSH command automatically:

```bash
ssh -L 11434:localhost:11434 user@server -N
```

### Rich Output Rendering

* GitHub-flavored Markdown
* Syntax-highlighted code blocks
* One-click code copying
* KaTeX math rendering
* Tables
* Blockquotes
* Checklists
* Links
* Inline and block LaTeX

### User Experience

* Dark and light themes
* Responsive layout
* Collapsible sidebar
* Keyboard shortcuts
* Accessibility-focused design
* Auto-resizing input box
* Scroll position preservation
* Virtualized rendering for large conversations
  
### Persistence

Stored locally using `localStorage`:

* Conversations
* Active chat
* Selected model
* System prompt
* Theme
* Generation settings
* SSH settings
* UI state
* Chat backup and restore via JSON export/import
---

## Screenshots
### Dark and light mode:
<img width="1470" height="801" alt="Screenshot 2026-06-17 at 6 22 01 PM" src="https://github.com/user-attachments/assets/fca25bc1-0815-4e47-a738-530118442f82" />

<img width="1470" height="802" alt="Screenshot 2026-06-17 at 6 22 15 PM" src="https://github.com/user-attachments/assets/26de1d11-14ed-472f-9a1d-bf6cb0186017" />

### Model responses:
<img width="1470" height="802" alt="Screenshot 2026-06-17 at 6 23 17 PM" src="https://github.com/user-attachments/assets/3612f23f-039e-4448-af27-275bf520cb38" />

<img width="1470" height="870" alt="Screenshot 2026-06-17 at 6 39 05 PM" src="https://github.com/user-attachments/assets/fc16d2b7-1de9-4da7-8a74-7e316caaf658" />

<img width="1470" height="872" alt="Screenshot 2026-06-17 at 6 41 00 PM" src="https://github.com/user-attachments/assets/b0d4a7a4-8cb8-4536-9748-18686854f17c" />

### Settings menu:
<img width="1232" height="257" alt="Screenshot 2026-06-17 at 6 39 52 PM" src="https://github.com/user-attachments/assets/2021e621-fd7c-49b6-87fb-30c0ea60c95d" />

---

## Requirements

### Install Ollama

Download and install Ollama:

https://ollama.com

Verify installation:

```bash
ollama --version
```

### Pull a Model

Example:

```bash
ollama pull llama3
```

### Start Ollama

```bash
ollama serve
```

Default API endpoint:

```text
http://localhost:11434
```

---

## Running

Save the file as:

```text
index.html
```

Open it directly in your browser:

```text
file:///path/to/index.html
```

Or serve it locally:

```bash
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

---

## Configuration

### System Prompt

Use the **System** panel to define assistant behavior.

Example:

```text
You are a concise technical assistant.
Respond in bullet points.
```

---

### Thinking Mode

Enable **Thinking** when using reasoning-capable models such as:

* deepseek-r1
* qwen3

Reasoning traces appear in a collapsible "Thinking" section.

---

### Generation Settings

| Setting     | Description                        |
| ----------- | ---------------------------------- |
| Max Tokens  | Maximum tokens generated per reply |
| Context     | Conversation context window        |
| Temperature | Response randomness                |
| Top-p       | Nucleus sampling threshold         |
| Seed        | Deterministic generation           |
| Keep Alive  | How long Ollama keeps model loaded |

---

## Keyboard Shortcuts

| Shortcut         | Action       |
| ---------------- | ------------ |
| Enter            | Send message |
| Shift + Enter    | New line     |
| Ctrl + Shift + N | New chat     |
| Esc              | Close dialog |

---

## Security

This project includes several security protections:

### Sanitized Output

All model-generated HTML is sanitized using DOMPurify before being inserted into the DOM.

### Safe Links

Links are restricted to HTTPS/HTTP URLs and automatically receive:

```html
rel="noopener noreferrer"
target="_blank"
```

Dangerous protocols are blocked:

```text
javascript:
data:
vbscript:
```

### No Inline Event Handlers

The UI avoids inline JavaScript handlers and uses delegated event listeners instead.

### KaTeX Protection

Although KaTeX 0.16.9 contains a known XSS vulnerability involving `\htmlData`, rendered output is sanitized before insertion.

### Local Storage

Stored locally:

* Conversations
* Settings
* Theme preferences

Not stored:

* Authentication tokens
* Passwords
* API keys
* SSH credentials

SSH commands are displayed only and never executed by the page.

---

## Architecture

```text
index.html
├── UI Layout
├── Theme System
├── Conversation Management
├── Markdown Rendering
├── Syntax Highlighting
├── KaTeX Rendering
├── Ollama API Integration
├── SSH Helper
├── Persistence Layer
└── Accessibility Features
```

### External Libraries

| Library      | Purpose           |
| ------------ | ----------------- |
| Marked       | Markdown parsing  |
| DOMPurify    | HTML sanitization |
| Highlight.js | Code highlighting |
| KaTeX        | Math rendering    |

---

## Ollama API Usage

The application communicates directly with:

### List Models

```http
GET /api/tags
```

### Chat

```http
POST /api/chat
```

Example payload:

```json
{
  "model": "llama3",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "stream": true
}
```

---

## Accessibility

The UI includes:

* ARIA labels
* Keyboard navigation
* Focus-visible styling
* Accessible dialogs
* Screen-reader-friendly status updates
* Semantic landmarks and roles

---

## Browser Support

Tested on modern browsers:

* Chrome
* Edge
* Firefox
* Safari

Requires:

* Fetch API
* Local Storage
* ES2020+ support

---

## Future Improvements

* Drag-and-drop file support
* Image model support
* Markdown export
* Prompt templates
* Multi-model conversations
* Conversation folders
* Full-text message search

---
## Recent Updates

### June 2026

- Added chat search
- Added manual chat renaming
- Added chat export/import
- Improved performance for large conversation histories
- Improved conversation management
  
---

## License

MIT License

Feel free to modify, distribute, and use this project in personal or commercial applications.

---

## Acknowledgements

* Ollama
* Marked
* DOMPurify
* Highlight.js
* KaTeX

Built as a fast, dependency-light interface for local AI models.
