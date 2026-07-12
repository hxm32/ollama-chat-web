# Ollama Chat

A lightweight, single-file web UI for chatting with local or remote Ollama models.

Built with plain HTML, CSS, and JavaScript - no build tools, frameworks, or backend required. (The one optional exception is the Web Search feature, which needs a tiny companion script — see [Web Search](#web-search).)

![License](https://img.shields.io/badge/license-MIT-blue)
![Ollama](https://img.shields.io/badge/Ollama-Compatible-green)

## Features

### Chat Experience

* Multi-conversation chat history
* Automatic conversation persistence
* Edit and resend previous messages, including attached images/documents
* Regenerate assistant responses
* Fork a conversation from any message into a new chat
* Delete individual messages
* Copy messages with one click
* Streaming responses with live token statistics
* Stop generation mid-response
* Chat search (titles and message content, with match snippets)
* Manual conversation renaming
* Export a single chat as a Markdown transcript
* Export chats to JSON
* Import chats from JSON backups
* Voice input (dictation) in supporting browsers
* Saved system prompt templates
  
### Attachments

* Attach images to messages for vision-capable models (drag-and-drop, paste, or file picker)
* Attach `.txt`, `.md`, and `.pdf` documents, parsed client-side and folded into the prompt
* Per-file and per-message size limits to keep things snappy

### Model Controls

* Automatic Ollama model discovery
* Model selector
* Custom system prompts
* Optional thinking/reasoning mode
* Optional web search tool for tool-calling models (via Ollama's hosted search API)
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
* Syntax-highlighted code blocks with language labels
* Line numbers, line-wrap toggle, and download-as-file for code blocks
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
* Scroll position preservation, with a "jump to latest" control when you've scrolled up during streaming
* Virtualized rendering for large conversations
  
### Persistence

Stored locally using `localStorage`:

* Conversations
* Active chat
* Selected model
* System prompt
* Saved system prompt templates
* Theme
* Generation settings
* SSH settings
* UI state
* Chat backup and restore via JSON export/import
---

## Screenshots
### Dark and light mode:
<img width="1470" height="871" alt="Screenshot 2026-06-18 at 4 39 39 PM" src="https://github.com/user-attachments/assets/cac65789-14f0-4df4-b597-c14eb4f052b5" />

<img width="1470" height="871" alt="Screenshot 2026-06-18 at 4 39 53 PM" src="https://github.com/user-attachments/assets/52f57345-99a5-46cf-9c27-b50966d51ff4" />

### Model responses:
<img width="1470" height="870" alt="Screenshot 2026-06-18 at 4 42 56 PM" src="https://github.com/user-attachments/assets/c20595ce-7775-4afa-84a1-26f92508d51e" />

<img width="1470" height="799" alt="Screenshot 2026-06-18 at 4 44 27 PM" src="https://github.com/user-attachments/assets/75f4ec16-18fe-4565-a4bf-7f10286c1580" />

<img width="1470" height="800" alt="Screenshot 2026-06-18 at 4 46 23 PM" src="https://github.com/user-attachments/assets/3b0ffcff-973a-4523-afbb-eb363d1717ab" />

### System prompt, ssh, settings and diagonstics menu:
<img width="1232" height="297" alt="Screenshot 2026-06-18 at 4 48 03 PM" src="https://github.com/user-attachments/assets/de5d7fe9-0b83-407d-b2ac-ff89510c3deb" />

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

### Web Search

Click **Search** to enable a `web_search` tool the model can call mid-reply, backed by [Ollama's hosted web search API](https://ollama.com/blog/web-search) — a separate cloud service from your local Ollama server.

**Browsers block calling that API directly** (it doesn't send CORS headers, so `fetch` fails with a CORS error no matter what). This isn't a bug in the app or specific to Ollama — it's standard for any API that requires a key, since allowing direct browser calls would expose the calling pattern to abuse. Making it work requires a small local proxy that forwards requests server-to-server, where CORS doesn't apply. A zero-dependency one is included: `ollama-search-proxy.py` (Python standard library only, nothing to install).

Setup:

1. Sign in or sign up for a free Ollama account, then go to [ollama.com/settings/keys](https://ollama.com/settings/keys). Click **Add API Key** — this generates a new key for you, it isn't asking for one you already have. Copy it right away; it's shown only once.
2. Run the proxy: `python3 ollama-search-proxy.py` (on Windows, that's usually just `python` instead of `python3`). Defaults to port 8787; pass a different port as an argument if that's taken.
3. Click **Search** in the header. Paste your API key, and set **Proxy URL** to `http://127.0.0.1:8787` (or whatever the script printed).
4. Use a tool-calling model (llama3.1+, qwen3, mistral-nemo, command-r, etc.) — the panel shows a note on whether your currently selected model reports tool support.

The proxy only relays your request to `ollama.com/api/web_search` and adds CORS headers to its own response; it doesn't read, log, or store your API key. If you skip it, search will fail with a clear error explaining why, and the model will be told the search failed so it can respond gracefully instead of the whole reply erroring out.

When the model decides to search, up to 3 search rounds run automatically per reply, and any pages it drew from are shown as source chips under the reply. This is the only feature in the app that talks to a server other than your own Ollama instance (plus the local proxy, if you run it); see [Security](#security) for details. Because tool-calling support varies by model and by Ollama version, treat the "supports tools" note as a hint, not a guarantee — if a model doesn't actually support tools, it will just reply normally without searching.

### Visit Usage.md to find a more detailed set of instructions.

> The **Port** field (and the local/remote port fields in SSH mode) only accept whole numbers from 1–65535. An invalid value is not silently ignored: it disables sending until fixed.
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
| Ctrl + Shift + N (Win/Linux) / Cmd + Shift + N (Mac) | New chat     |
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

Although KaTeX 0.16.9 contains a known XSS vulnerability involving `\htmlData`, the HTML that KaTeX generates is itself passed through DOMPurify before being inserted into the page, in addition to the surrounding Markdown output.

### Local Storage

Stored locally:

* Conversations
* Settings, including your Ollama web search API key if you set one (see [Web Search](#web-search) below)
* Theme preferences

Not stored:

* Authentication tokens or passwords for any service other than the optional web search key above
* SSH credentials

SSH commands are displayed only and never executed by the page.

### Web Search Network Access

Everything else in this app talks only to your own Ollama server. The optional web search feature is the one exception: when enabled, it sends your search queries and API key to `https://ollama.com/api/web_search` over HTTPS — routed through the local `ollama-search-proxy.py` script if you're running it (required in practice, since the browser blocks calling that URL directly; see [Web Search](#web-search)). The proxy runs on your own machine, only relays the request, and doesn't read, log, or store your API key. No conversation content, images, or documents are sent to ollama.com, only the query text the model chooses to search for. Your API key is stored in `localStorage` like the rest of the app's settings and never leaves your browser except in that request. It is *not* included in chat export/import backups.

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
├── Web Search Tool Calling
├── SSH Helper
├── Persistence Layer
└── Accessibility Features

ollama-search-proxy.py   (optional, only needed for Web Search)
```

### External Libraries

| Library      | Purpose           |
| ------------ | ----------------- |
| Marked       | Markdown parsing  |
| DOMPurify    | HTML sanitization |
| Highlight.js | Code highlighting |
| KaTeX        | Math rendering    |
| pdf.js       | PDF text extraction for document attachments |

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

Attached images are sent as raw base64 in a per-message `images` array (the `data:...;base64,` prefix is stripped first). Attached documents aren't sent as a separate field — their extracted text is appended to the message's `content` before the request is made, wrapped with a `[Attached file: name]` marker.

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

Voice dictation (Web Speech API) is currently only available in Chromium-based browsers (Chrome, Edge); the microphone button is hidden automatically elsewhere.

---

## Future Improvements

* Multi-model conversations (side-by-side comparison)
* Conversation folders and pinning
* Additional document formats

---
## Recent Updates

### July 2026

- Added an optional web search tool (via Ollama's hosted search API) for tool-calling models
- Added image and document (txt/md/pdf) attachments, including while editing a message
- Added full-text chat search with match snippets
- Added saved system prompt templates
- Added code block language labels, line numbers, wrap toggle, and download-as-file
- Added voice input (dictation) for supporting browsers
- Added a jump-to-latest control that appears when auto-scroll pauses
- Added per-chat Markdown export and conversation forking
- Fixed several storage, sanitization, and cross-chat attachment-leak issues

### June 2026

- Added chat search
- Added manual chat renaming
- Added chat export/import
- Improved performance for large conversation histories
- Improved conversation management
- Add truncation notice, auto-context sync, and settings reset button
- Fix cross-chat generation bleed and harden connection/storage handling
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
