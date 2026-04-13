"""Shared helpers for resolving and inspecting chat models."""

from __future__ import annotations

import importlib.util
import os
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from deepagents.profiles import _get_harness_profile


def _gigachat_env_kwargs() -> dict[str, str]:
    """Read GigaChat kwargs from environment variables."""
    env_to_kwarg = {
        "GIGACHAT_AUTH_URL": "auth_url",
        "GIGACHAT_BASE_URL": "base_url",
        "GIGACHAT_CREDENTIALS": "credentials",
        "GIGACHAT_PASSWORD": "password",
        "GIGACHAT_SCOPE": "scope",
        "GIGACHAT_USER": "user",
    }
    result: dict[str, str] = {}
    for env_name, kwarg in env_to_kwarg.items():
        value = os.environ.get(env_name)
        if value:
            result[kwarg] = value
    return result


def _resolve_gigachat_model(spec: str, kwargs: dict[str, Any]) -> BaseChatModel:
    """Resolve a `gigachat:` model spec without relying on `init_chat_model`.

    LangChain's built-in provider registry does not currently expose
    `gigachat`, so `init_chat_model("gigachat:...")` raises
    `Unsupported provider`. We instantiate `langchain_gigachat.GigaChat`
    directly instead.

    Args:
        spec: Model spec in `gigachat:model-name` format.
        kwargs: Extra constructor kwargs forwarded to `GigaChat`.

    Returns:
        Instantiated `GigaChat` chat model.

    Raises:
        ImportError: If `langchain-gigachat` is not installed.
    """
    _provider, _sep, model_name = spec.partition(":")
    try:
        from langchain_gigachat import GigaChat  # noqa: PLC0415  # Optional provider import should stay lazy
    except ImportError as exc:
        try:
            spec_found = importlib.util.find_spec("langchain_gigachat") is not None
        except (ImportError, ValueError):
            spec_found = False
        if spec_found:
            msg = (
                "Provider package 'langchain-gigachat' is installed but failed "
                f"to import for model '{spec}': {exc}"
            )
        else:
            msg = (
                "Missing package for provider 'gigachat'. "
                "Install it with `pip install langchain-gigachat`."
            )
        raise ImportError(msg) from exc

    return GigaChat(model=model_name, **kwargs)


def resolve_model(model: str | BaseChatModel) -> BaseChatModel:
    """Resolve a model string to a `BaseChatModel`.

    If `model` is already a `BaseChatModel`, returns it unchanged.

    String models are resolved via `init_chat_model`. OpenAI models
    (prefixed with `openai:`) default to the Responses API.

    OpenRouter models include default app attribution headers unless overridden
    via `OPENROUTER_APP_URL` / `OPENROUTER_APP_TITLE` env vars.

    Args:
        model: Model string (e.g. `"openai:gpt-5.4"`) or pre-configured
            `BaseChatModel` subclass instance.

    Returns:
        Resolved `BaseChatModel` instance.
    """
    if isinstance(model, BaseChatModel):
        return model

    profile = _get_harness_profile(model)

    # Execute any pre-initialization logic
    if profile.pre_init is not None:
        profile.pre_init(model)

    # Combine static and factory kwargs, with factory taking precedence
    kwargs: dict[str, Any] = {**profile.init_kwargs}
    if profile.init_kwargs_factory is not None:
        kwargs.update(profile.init_kwargs_factory())

    if model.startswith("gigachat:"):
        kwargs.update(_gigachat_env_kwargs())
        return _resolve_gigachat_model(model, kwargs)

    return init_chat_model(model, **kwargs)  # kwargs may be empty


def get_model_identifier(model: BaseChatModel) -> str | None:
    """Extract the provider-native model identifier from a chat model.

    Providers do not agree on a single field name for the identifier. Some use
    `model_name`, while others use `model`. Reading the serialized model config
    lets us inspect both without relying on reflective attribute access.

    Args:
        model: Chat model instance to inspect.

    Returns:
        The configured model identifier, or `None` if it is unavailable.
    """
    config = model.model_dump()
    return _string_value(config, "model_name") or _string_value(config, "model")


def get_model_provider(model: BaseChatModel) -> str | None:
    """Extract the provider name from a chat model instance.

    Uses the model's `_get_ls_params` method. The base `BaseChatModel`
    implementation derives `ls_provider` from the class name, and all major
    providers override it with a hardcoded value (e.g. `"anthropic"`).

    Args:
        model: Chat model instance to inspect.

    Returns:
        The provider name, or `None` if unavailable.
    """
    try:
        ls_params = model._get_ls_params()
    except (AttributeError, TypeError, NotImplementedError):
        return None
    provider = ls_params.get("ls_provider")
    if isinstance(provider, str) and provider:
        return provider
    return None


def model_matches_spec(model: BaseChatModel, spec: str) -> bool:
    """Check whether a model instance already matches a string model spec.

    Matching is performed in two ways: first by exact string equality between
    `spec` and the model identifier, then by comparing only the model-name
    portion of a `provider:model` spec against the identifier. For example,
    `"openai:gpt-5"` matches a model with identifier `"gpt-5"`.

    Assumes the `provider:model` convention (single colon separator).

    Args:
        model: Chat model instance to inspect.
        spec: Model spec in `provider:model` format (e.g., `openai:gpt-5`).

    Returns:
        `True` if the model already matches the spec, otherwise `False`.
    """
    current = get_model_identifier(model)
    if current is None:
        return False
    if spec == current:
        return True

    _, separator, model_name = spec.partition(":")
    return bool(separator) and model_name == current


def _string_value(config: dict[str, Any], key: str) -> str | None:
    """Return a non-empty string value from a serialized model config."""
    value = config.get(key)
    if isinstance(value, str) and value:
        return value
    return None
