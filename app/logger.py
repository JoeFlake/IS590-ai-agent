"""Structured logging configuration for IS590 AI Agent.

Emits JSON-formatted log lines so tool calls, arguments, and results
can be parsed by log aggregators or reviewed as plain text.
"""

import json
import logging
import sys
from datetime import datetime, timezone


class _JSONFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Merge any extra structured fields attached to the record
        for key, value in record.__dict__.items():
            if key not in (
                "args", "asctime", "created", "exc_info", "exc_text",
                "filename", "funcName", "id", "levelname", "levelno",
                "lineno", "message", "module", "msecs", "msg", "name",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "thread", "threadName", "taskName",
            ):
                payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger that writes structured JSON to stdout."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger


def log_tool_call(logger: logging.Logger, tool: str, args: dict, result: str) -> None:
    """Log a tool invocation with its arguments and result summary."""
    logger.info(
        "tool_call",
        extra={
            "tool": tool,
            "tool_args": args,
            "result_preview": result[:200] if result else "",
            "result_length": len(result) if result else 0,
        },
    )


def log_tool_error(logger: logging.Logger, tool: str, args: dict, error: str) -> None:
    """Log a tool invocation that resulted in an error."""
    logger.error(
        "tool_error",
        extra={
            "tool": tool,
            "tool_args": args,
            "error": error,
        },
    )
