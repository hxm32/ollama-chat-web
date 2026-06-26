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

- **Search** – filter your chat list by title using the search field at the top of the sidebar.
- **Rename** – hover over any chat and click the ✎ icon to give it a more meaningful name.
- **Delete** – hover and click the ✕ icon; you’ll be asked to confirm before anything is removed.
- **New Chat** – click the **＋** button at the top of the sidebar (or use `Ctrl+Shift+N` on Windows/Linux, `Cmd+Shift+N` on Mac) to start a fresh conversation.
- **Export / Import** – the two buttons at the bottom let you back up all your chats as a single JSON file, or restore a previously exported file. This is handy for moving between machines or keeping a safety copy.

---

## The Header – Controls at a Glance

Across the top bar you’ll find the main controls:

- **Port** – change this if your Ollama instance listens on a non‑standard port.
- **Model** – select which model to use for the *next* message. You can switch mid‑conversation, the new model will handle subsequent replies.
- **System** – opens a panel where you can write a system prompt. This sets a persistent persona or set of rules for the AI, for example, “You are a terse assistant that answers in bullet points.” The character counter helps you stay under the 4,000‑character limit.
- **Thinking** – toggles the model’s “extended thinking” mode. This is specifically for models that support it (like `deepseek-r1` or `qwen3`); when enabled, you’ll see a collapsible block that reveals the model’s internal reasoning before it gives you the final answer.
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

## Message Interactions – Edit, Regenerate, Copy, Delete

Hover over any message (yours or the assistant’s) to reveal a row of action buttons:

- **Edit** (user messages only) – replace the content of your message and resend it. The conversation is truncated at that point, and a new response is generated.
- **Regenerate** (assistant messages only) – discards the current reply and asks the model to try again, using the same prompt and conversation history.
- **Copy** – copies the raw message text to your clipboard.
- **Delete** – permanently removes that single message. A confirmation dialog appears before anything is deleted.

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
All conversations are stored in your browser’s `localStorage`. Clearing your browser data will erase them. Use the **Export** button periodically to back up your chats.

---

## A Note on Performance

The app uses a virtualised message list, only the last 100 messages are rendered at any time, with a spacer that approximates the height of older messages. This keeps the interface snappy even for very long conversations.

If you notice lag while a reply is streaming, remember that the rendering throttles itself to about 80ms between updates, this balances responsiveness with CPU usage.

---

That should be enough to get you chatting comfortably. The rest is exploration, tweak the temperature, write a colourful system prompt, or tunnel into a remote machine and see how it feels. Enjoy.
