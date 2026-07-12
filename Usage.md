# Ollama Chat – User Guide

Welcome to the Ollama Chat interface, a lightweight, browser‑based front‑end for chatting with any model served by [Ollama](https://ollama.com). It stores your conversations locally, renders Markdown, LaTeX, and code with syntax highlighting, and gives you fine‑grained control over generation parameters, all without ever sending your data anywhere.

Below you’ll find everything you need to get started, from the first connection to tweaking the most obscure settings.

---

## Getting Started

**1. Make sure Ollama is running**  
This app is just a front‑end; it needs a live Ollama server behind it. By default it expects one on `localhost:11434`, the standard port. If you’ve changed the port, update the **Port** field in the header.

You can verify the connection by glancing at the status pill in the top‑left corner, it changes from *connecting…* to *connected* (or *offline*) and you can click it anytime to force a re‑check.

**2. Pick a model**  
Once connected, the **Model** dropdown populates with every model you have available locally. If the list is empty, open a terminal and run:

```bash
ollama pull llama3
```

(or any other model name) then refresh the list by clicking the status pill.

**3. Start chatting**  
Type a message into the input box at the bottom and press **Enter** to send it. The assistant’s replies appear with Markdown formatting, code blocks, and even mathematical expressions written in LaTeX, all rendered on the fly.

> **Tip:** Use **Shift+Enter** to insert a line break without sending the message.

---

## The Sidebar – Your Conversation History

The sidebar on the left holds every chat you’ve ever started. Conversations save automatically as you type, no manual “save” button required.

- **Search** – filter your chat list by title *or* message content. If a match is only inside a message (not the title), a short snippet is shown under the chat title so you can see why it matched.
- **Rename** – hover over any chat and click the ✎ icon to give it a more meaningful name.
- **Export as Markdown** – hover over any chat and click the ⇩ icon to download that single conversation as a readable `.md` transcript (separate from the full backup below).
- **Delete** – hover and click the ✕ icon; you’ll be asked to confirm before anything is removed.
- **New Chat** – click the **＋** button at the top of the sidebar (or use `Ctrl+Shift+N` on Windows/Linux, `Cmd+Shift+N` on Mac) to start a fresh conversation.
- **Export / Import** – the two buttons at the bottom let you back up all your chats as a single JSON file, or restore a previously exported file. This is handy for moving between machines or keeping a safety copy.

---

## The Header – Controls at a Glance

Across the top bar you’ll find the main controls:

- **Port** – change this if your Ollama instance listens on a non‑standard port. Must be a whole number between 1 and 65535; an invalid value disables sending until it's corrected.
- **Model** – select which model to use for the *next* message. You can switch mid‑conversation, the new model will handle subsequent replies.
- **System** – opens a panel where you can write a system prompt. This sets a persistent persona or set of rules for the AI, for example, “You are a terse assistant that answers in bullet points.” The character counter helps you stay under the 4,000‑character limit. A **Saved prompts** dropdown at the top lets you save the current text as a reusable template, load one back in, or delete it — handy if you switch between a few personas often.
- **Thinking** – toggles the model’s “extended thinking” mode. This is specifically for models that support it (like `deepseek-r1` or `qwen3`); when enabled, you’ll see a collapsible block that reveals the model’s internal reasoning before it gives you the final answer.
- **Search** – lets the model search the web mid‑reply using Ollama’s hosted search API. Clicking it opens a panel for your Ollama API key (free, from ollama.com) and shows a note on whether your current model reports tool‑calling support. See “Web Search” below for the full picture.
- **SSH** – opens a panel for connecting to an Ollama instance on a *remote* machine via an SSH tunnel. Fill in the remote host, remote port, and local port, then copy the command shown and run it in your terminal. Once the tunnel is established, the app behaves as if Ollama were running locally.
- **Settings** – reveals fine‑grained generation parameters (more on these below).
- **Diagnostics** – displays the Ollama version, currently loaded models, and the host/port the app is actually talking to, useful for debugging.
- **Theme** – toggles between dark and light mode.
- **Clear** – wipes the current conversation’s message history. The chat remains in your sidebar (with a blank slate), so you can reuse the same title and settings.

---

## Generation Settings – Tuning the Output

When you open the **Settings** panel, you have control over the engine that drives every reply:

| Setting | What it does |
|---------|--------------|
| **Max Tokens** | The hard ceiling on how many tokens the model can generate in a single reply. If a response gets cut off mid‑sentence, you’ll see a notice with a button that automatically doubles this value for you. |
| **Context** | The size of the conversation history (in tokens) that the model considers. Larger values let the model “remember” more of the conversation, but consume more memory. |
| **Temperature** | Controls randomness, `0` makes the model deterministic and focused, `1` is balanced, and `2` can produce very creative (but sometimes chaotic) outputs. |
| **Top‑p** | Nucleus sampling: lower values restrict the model to a smaller set of probable tokens, making outputs more focused; higher values allow more diversity. |
| **Seed** | Set a fixed integer to get reproducible responses. Leave at `-1` for random seeds. |
| **Keep‑Alive** | How long Ollama keeps the model loaded in memory after the last request. Use `5m` (default), `1h`, or `-1` to keep it loaded indefinitely. |

All settings apply to the *next* message you send, you don’t need to restart the chat.

---

---

## Attachments & Voice Input

Next to the message box you’ll find two attach buttons and, in supporting browsers, a microphone:

- **Image attach** (picture icon) – attach one or more images to your next message for vision‑capable models (e.g. `llava`, `bakllava`). You can also drag and drop image files onto the input area, or paste an image directly from your clipboard. Each image is capped at 10MB, up to 8 per message. If the model you’re using doesn’t support images, the app will automatically retry the request without them and let you know.
- **Document attach** (paperclip icon) – attach `.txt`, `.md`, or `.pdf` files. Their text content is quietly folded into your prompt (so the model can read it) without cluttering the visible message, which just shows a small file chip. PDFs are parsed in your browser, up to 100 pages; documents are capped at 10MB per file and roughly 50,000 characters of extracted text, up to 4 files per message. Nothing is uploaded anywhere except to your own Ollama server as part of the prompt.
- **Dictate** (microphone icon, Chrome/Edge only) – click to start voice‑to‑text dictation into the input box; click again (or it’ll stop automatically) to finish. This uses your browser’s built‑in speech recognition and doesn’t send audio anywhere the browser itself doesn’t.

Attachments you haven’t sent yet appear as removable chips above the input box.

---

## Web Search

The **Search** button in the header lets the model look things up on the web while it's answering, using [Ollama's hosted search API](https://ollama.com/blog/web-search) — a separate cloud service from your own local Ollama server, so it needs internet access even if the rest of the app is fully local.

**Important:** browsers block calling that API directly from a web page (it's blocked by CORS, a browser security rule for APIs that need a key). This isn't specific to Ollama or a bug in this app — it's how essentially every API of this kind behaves. To actually make search work, you need to run a tiny included helper script, `ollama-search-proxy.py`, alongside the app. It only needs Python (nothing to install) and does nothing except forward your search request to Ollama and hand the response back with the right headers — it doesn't read or store your API key.

**Setup:**

1. Sign in or sign up for a free Ollama account, then go to [ollama.com/settings/keys](https://ollama.com/settings/keys). Click **Add API Key** — this generates a new key for you, it isn't asking for one you already have. Copy it right away; it's shown only once.
2. Open a terminal in the folder with `ollama-search-proxy.py` and run:
   ```
   python3 ollama-search-proxy.py
   ```
   On Windows, that's usually just `python ollama-search-proxy.py` instead. Leave it running. It'll print an address like `http://127.0.0.1:8787`.
3. Click **Search** in the header. Paste your API key into the **API Key** field, and paste the address from step 2 into the **Proxy URL** field.
4. Pick a model that supports tool calling (e.g. `llama3.1` and newer, `qwen3`, `mistral-nemo`, `command-r`). The panel shows a small note on whether your current model reports tool support — treat it as a hint rather than a hard guarantee, since not every Ollama version exposes this reliably.

Once set up, click **Search** again any time to turn the tool on or off for your next message (it stays on until you turn it off). When the model chooses to search, you'll see a brief "🔍 Searching the web for…" line appear in its reply while the search runs, and once it responds, any pages it drew from show up as clickable source chips underneath. Up to 3 search rounds can happen automatically within a single reply, so the model can search, read the results, and search again if needed.

**Things to know:**

- Your API key is stored in your browser's local storage like everything else in this app. It's sent only to the proxy (on your own machine) and, from there, to `ollama.com` — never to your local Ollama server. It's not included in chat export/import backups.
- Only your search queries go to ollama.com — not your conversation, images, or attached documents.
- If you don't run the proxy, search will fail with a clear error explaining why (rather than a confusing generic failure).
- If a model doesn't actually support tools, it'll just answer normally without searching; nothing breaks.
- If the search call fails (bad key, proxy not running, etc.), the model is told the search failed so it can respond gracefully instead of the whole reply failing.

---

## Message Interactions – Edit, Regenerate, Copy, Delete, Fork

Hover over any message (yours or the assistant’s) to reveal a row of action buttons:

- **Edit** (user messages only) – replace the content of your message and resend it. Any images or documents already attached to that message stay attached, and you can add or remove attachments (using the same picture/paperclip buttons) before resending. The conversation is truncated at that point, and a new response is generated.
- **Regenerate** (assistant messages only) – discards the current reply and asks the model to try again, using the same prompt and conversation history.
- **Copy** – copies the raw message text to your clipboard.
- **Fork** – duplicates the conversation up to and including that message into a brand‑new chat, so you can explore a different direction without losing the original thread.
- **Delete** – permanently removes that single message. A confirmation dialog appears before anything is deleted.

Code blocks in replies have their own toolbar: a language label, a **wrap** toggle for long lines, a **download** button to save the snippet as a file, and the usual copy button.

If you scroll up while a reply is streaming in, auto‑scroll pauses so you can keep reading; a small “↓ New messages” pill appears so you can jump back to the bottom whenever you’re ready.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send the current message (when focused in the input box). |
| `Shift+Enter` | Insert a newline in the input box without sending. |
| `Ctrl+Shift+N` (Win/Linux) / `Cmd+Shift+N` (Mac) | Create a new chat. |
| `Esc` | Close any open modal dialog (rename, delete confirmation, etc.). |

---

## Troubleshooting Common Issues

**“No models” in the dropdown**  
Ollama is running, but you haven’t pulled any models yet. Open a terminal and run `ollama pull <model-name>` (e.g., `ollama pull llama3.2`). After the pull completes, click the status pill to refresh the list.

**“Connection failed” / “offline”**  
Check that Ollama is actually running (try `ollama list` in a terminal). If it is, verify the port number matches. If you’re using SSH mode, make sure the tunnel command is still active, SSH connections can time out.

**Responses are cut off**  
Your **Max Tokens** setting is probably too low. Click the “Increase Max Tokens” button that appears on the truncated notice, or manually raise the value in the Settings panel.

**The “Thinking” block doesn’t appear**  
Not every model supports extended thinking. Only models specifically trained for reasoning (like DeepSeek‑R1 or Qwen3) will produce a thinking block. For other models, the toggle has no effect.

**My chats disappeared after an update**  
All conversations are stored in your browser’s `localStorage`. Clearing your browser data will erase them. Use the **Export** button periodically to back up your chats. If storage fills up (localStorage is limited to a few MB total), you’ll see a notice, delete or export some old chats to free up space.

**The microphone button isn’t showing up**  
Voice dictation uses the Web Speech API, which is currently only available in Chromium‑based browsers (Chrome, Edge). The button is hidden automatically in browsers that don’t support it.

**A PDF didn’t attach, or attached with no text**  
Only text‑based PDFs can be read (scanned/image‑only PDFs have no extractable text). Very large PDFs are capped at the first 100 pages.

**Search is on, but the model never searches**  
First, check that `ollama-search-proxy.py` is running and the Proxy URL in the Search panel matches what it printed — without it, every search attempt fails with a CORS error (visible in the browser console) before the model even gets a result back. If the proxy is running and it still doesn't search: not every model supports tool calling, and the app can't always detect this in advance (see the note in the Search panel). Some models also just decide a search isn't necessary for a given question, or claim they "can't access the web" without ever actually trying — that's the model guessing, not a real error; check the console for a log line saying whether it called the tool. Try asking something explicitly time‑sensitive ("what's the latest version of X") to test it.

**The proxy reports an SSL certificate error**  
This is a local Python/OS issue, not a problem with Ollama, and it's common the first time you use Python for HTTPS requests (especially on macOS with Python installed from python.org). The proxy prints exactly which Python it's running as when it starts — run the `pip install certifi` command it suggests using *that exact path* (not just `pip3 install certifi` generically), since installing certifi for a different Python than the one running the script won't help. Then restart the proxy.

If that still doesn't fix it, run the proxy once with `OLLAMA_SEARCH_PROXY_INSECURE=1` set in your environment (e.g. `OLLAMA_SEARCH_PROXY_INSECURE=1 python3 ollama-search-proxy.py` on macOS/Linux) to temporarily skip certificate checks. If search then works, it really was a certificate problem — go back to fixing certifi. If it *still* fails, the problem isn't certificates at all — it's more likely a firewall, VPN, or network policy blocking the connection to ollama.com, which is outside what this script can fix. Turn this off again once you're done diagnosing; it's not safe to leave on.

---

## A Note on Performance

The app uses a virtualised message list, only the last 100 messages are rendered at any time, with a spacer that approximates the height of older messages. This keeps the interface snappy even for very long conversations.

If you notice lag while a reply is streaming, remember that the rendering throttles itself to about 80ms between updates, this balances responsiveness with CPU usage.

---

That should be enough to get you chatting comfortably. The rest is exploration, tweak the temperature, write a colourful system prompt, or tunnel into a remote machine and see how it feels. Enjoy.
