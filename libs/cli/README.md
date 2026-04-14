# 🧠🤖 Deep Agents CLI

[![PyPI - Version](https://img.shields.io/pypi/v/deepagents-cli?label=%20)](https://pypi.org/project/deepagents-cli/#history)
[![PyPI - License](https://img.shields.io/pypi/l/deepagents-cli)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pepy/dt/deepagents-cli)](https://pypistats.org/packages/deepagents-cli)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchain.svg?style=social&label=Follow%20%40LangChain)](https://x.com/langchain)

<p align="center">
  <img src="https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/images/cli.png" alt="Deep Agents CLI" width="600"/>
</p>

## Quick Install

```bash
curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash
```

```bash
# With model provider extras
# OpenAI, Anthropic, and Gemini are included by default
DEEPAGENTS_EXTRAS="nvidia,ollama" curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash

# GigaChat
DEEPAGENTS_EXTRAS="gigachat" curl -LsSf https://raw.githubusercontent.com/langchain-ai/deepagents/main/libs/cli/scripts/install.sh | bash
```

Or install directly with `uv`:

```bash
# Install with chosen model providers
uv tool install 'deepagents-cli[nvidia,ollama]'

# Install GigaChat support
uv tool install 'deepagents-cli[gigachat]'

# Or add the provider package to an existing installation
uv tool install deepagents-cli --with langchain-gigachat
```

Run the CLI:

```bash
deepagents
```

## GigaChat

`deepagents-cli` can run with [`langchain-gigachat`](https://pypi.org/project/langchain-gigachat/), which is compatible with LangChain 1.x.

Install the CLI with the `gigachat` extra:

```bash
uv tool install 'deepagents-cli[gigachat]'
```

Configure authentication in `~/.deepagents/.env`:

```bash
# Recommended: OAuth authorization key
GIGACHAT_CREDENTIALS="<your_authorization_key>"

# Optional: select a scope when using B2B or CORP access
# GIGACHAT_SCOPE="GIGACHAT_API_B2B"

# Optional: custom endpoints
# GIGACHAT_BASE_URL="https://gigachat.devices.sberbank.ru/api/v1"
# GIGACHAT_AUTH_URL="https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
```

The CLI also supports username/password auth when `GIGACHAT_CREDENTIALS` is not set:

```bash
GIGACHAT_USER="<username>"
GIGACHAT_PASSWORD="<password>"
```

Start Deep Agents with a GigaChat model explicitly:

```bash
deepagents --model gigachat:GigaChat-2-Max
```

Or make GigaChat the persistent default in `~/.deepagents/config.toml`:

```toml
[models]
default = "gigachat:GigaChat-2-Max"
```

If your environment requires the Russian trusted root certificate chain, configure the underlying SDK via `GIGACHAT_CA_BUNDLE_FILE`. See the [`gigachat`](https://pypi.org/project/gigachat/) package docs for the full TLS and authentication options.

## 🤔 What is this?

The fastest way to start using Deep Agents. `deepagents-cli` is a pre-built coding agent in your terminal — similar to Claude Code or Cursor — powered by any LLM that supports tool calling. One install command and you're up and running, no code required.

**What the CLI adds on top of the SDK:**

- **Interactive TUI** — rich terminal interface with streaming responses
- **Conversation resume** — pick up where you left off across sessions
- **Web search** — ground responses in live information
- **Remote sandboxes** — run code in isolated environments (LangSmith, AgentCore, Daytona, Modal, Runloop, & more)
- **Persistent memory** — agent remembers context across conversations
- **Custom skills** — extend the agent with your own slash commands
- **Headless mode** — run non-interactively for scripting and CI
- **Human-in-the-loop** — approve or reject tool calls before execution

## 📖 Resources

- **[CLI Documentation](https://docs.langchain.com/oss/python/deepagents/cli/overview)**
- **[Changelog](https://github.com/langchain-ai/deepagents/blob/main/libs/cli/CHANGELOG.md)**
- **[Source code](https://github.com/langchain-ai/deepagents/tree/main/libs/cli)**
- **[Deep Agents SDK](https://github.com/langchain-ai/deepagents)** — underlying agent harness

## 📕 Releases & Versioning

See our [Releases](https://docs.langchain.com/oss/python/release-policy) and [Versioning](https://docs.langchain.com/oss/python/versioning) policies.

## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it be in the form of a new feature, improved infrastructure, or better documentation.

For detailed information on how to contribute, see the [Contributing Guide](https://docs.langchain.com/oss/python/contributing/overview).

## 🤝 Acknowledgements

This project was primarily inspired by Claude Code, and initially was largely an attempt to see what made Claude Code general purpose, and make it even more so.
