# Buddy Tools

Micro-tools for **SEO** and **daily-life hacks** that you can run from the terminal.

---

## 🚀 Quick install

```bash
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install the package in editable mode
pip install -e .
```

Now you can run:

```bash
axle list
axle run 1 "your prompt"
axle scan
```

---

## 📦 Features

- SEO-focused microtools (keyword checker, meta-tag auditor, etc.)
- Daily-life automation helpers from the terminal
- `axle list` shows all tools with numbers
- `axle run <tool_number_or_name> <prompt>` executes a tool
- Security and dependency checks via `axle scan`
- Configurable tools folder path

---

## 🛠️ Commands

| Command                     | Purpose                                      |
| --------------------------- | -------------------------------------------- |
| `axle list`              | List all tools in the `tools/` directory.  |
| `axle run 1 "prompt"`    | Run tool by number and pass a prompt.        |
| `axle run tool_name ...` | Run by filename (without `.py`).           |
| `axle info tool_name`    | Show tool description.                       |
| `axle scan`              | Scan dependencies for known vulnerabilities. |
| `axle doctor`            | Check Python, disk, and required modules.    |
| `axle path`              | Show current tools folder location.          |
| `axle help`              | Show all commands.                           |

---

## 🧱 Requirements

- Python 3.10+
- RAM: 8 GB minimum, 16 GB preferred
- Disk: 5–8 GB free for models and caches
- CPU: 2 cores minimum, 4 cores preferred

Install via `pip install -r requirements.txt` and `pip install -e .`

---

## 📝 Docs

See:

- `docs/index.md` – overview
- `docs/installation.md` – step-by-step setup
- `docs/usage.md` – how to use tools
- `docs/commands.md` – detailed command reference

---

## 🌐 Community & Support

If this helps your workflow:

- **Give the GitHub repo a star** ⭐
- **Follow on X**: [@_skpaul82](https://x.com/_skpaul82)
- **Instagram**: [skpaul82](https://instagram.com/skpaul82)
- **Newsletter**: [axle.sanjoypaul.com](https://axle.sanjoypaul.com)

---

## 📄 License

MIT License – see `LICENSE` for details.

---

## 🤝 Contributing

Contributions are welcome! Please see `docs/contributing.md` for guidelines.

---

## 📚 Troubleshooting

Having issues? Check `docs/troubleshooting.md` for common problems and solutions.

---

♥ Built for the community.
♥ Shared with love for creators, builders, and learners.
