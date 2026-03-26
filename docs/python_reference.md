# Python Reference — Chicken Joe's Coding Handbook

Bro, Python is the longboard of programming languages. Easy to get started, incredibly versatile, and the whole AI/ML world runs on it. Here's the gnarliest stuff you need to know.

## Python Basics

### Data Types
```python
name = "Chicken Joe"        # str
wave_height = 20.5          # float
wipeouts = 3                # int
is_stoked = True            # bool
boards = ["corn", "foam"]   # list (mutable)
coords = (34.0, -118.5)     # tuple (immutable)
vibe = {"mood": "chill"}    # dict
unique_tricks = {"aerial"}  # set
```

### F-strings (the good way to format strings)
```python
name = "Chicken Joe"
waves = 42
print(f"{name} rode {waves} waves today. Totally rad!")
```

### List Comprehensions
```python
wave_heights = [2, 8, 15, 3, 20, 6]
gnarly_waves = [h for h in wave_heights if h >= 10]
# [15, 20]
```

## Functions

```python
def rate_wave(height: float, wind: str = "offshore") -> str:
    """Rate a wave based on height and wind conditions."""
    if height >= 15 and wind == "offshore":
        return "Totally tubular, dude!"
    elif height >= 8:
        return "Pretty gnarly, worth paddling out"
    else:
        return "Mellow, good for groms"

result = rate_wave(20.0)  # "Totally tubular, dude!"
```

Type hints (`height: float`, `-> str`) are optional but great for readability and tooling. LangChain tools use them for schema generation.

## Classes

```python
class Surfer:
    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill
        self.wipeouts = 0

    def ride_wave(self, height: float) -> str:
        if height > 15 and self.skill != "pro":
            self.wipeouts += 1
            return f"{self.name} wiped out!"
        return f"{self.name} shredded a {height}ft wave!"

joe = Surfer("Chicken Joe", "pro")
print(joe.ride_wave(30))  # "Chicken Joe shredded a 30ft wave!"
```

## Async / Await

Python's async model is crucial for FastAPI and LangChain streaming. Instead of blocking while waiting (like sitting on the beach doing nothing), async lets you handle other things while waiting for a response.

```python
import asyncio

async def fetch_wave_report(location: str) -> dict:
    await asyncio.sleep(1)  # simulate network call
    return {"location": location, "height": "15ft", "vibe": "gnarly"}

async def main():
    report = await fetch_wave_report("Pipeline")
    print(report)

asyncio.run(main())
```

`async def` defines a coroutine. `await` pauses execution until the awaited thing finishes — without blocking other coroutines.

## Error Handling

```python
try:
    result = risky_surf_maneuver()
except ValueError as e:
    print(f"Bad input, bro: {e}")
except Exception as e:
    print(f"Total wipeout: {e}")
finally:
    clean_up_board()  # always runs, no matter what
```

## Working with Files

```python
# Reading
with open("surf_report.md", "r", encoding="utf-8") as f:
    content = f.read()

# Writing
with open("session_log.txt", "w") as f:
    f.write("Rode 12 waves. Stoked.\n")

# Reading all lines
with open("wave_data.txt") as f:
    lines = f.readlines()
```

`with` statements automatically close the file when done, even if an error occurs.

## Path Handling with pathlib

```python
from pathlib import Path

docs_dir = Path("docs")
for md_file in docs_dir.glob("*.md"):
    print(md_file.name, md_file.stat().st_size)

# Read a file
content = (docs_dir / "ai_concepts.md").read_text(encoding="utf-8")
```

`pathlib.Path` is way cleaner than `os.path` for file system operations.

## Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file into environment

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No API key found, dude. Check your .env file.")
```

Never hardcode secrets. Always use environment variables loaded from `.env` (which is gitignored).

## Dictionaries — Common Patterns

```python
wave_stats = {"height": 15, "period": 12, "direction": "NW"}

# Safe access with default
height = wave_stats.get("height", 0)

# Iterate
for key, value in wave_stats.items():
    print(f"{key}: {value}")

# Dict comprehension
doubled = {k: v * 2 for k, v in wave_stats.items() if isinstance(v, (int, float))}
```

## Type Hints and Pydantic

Python type hints + Pydantic = automatic validation. FastAPI uses Pydantic for all request/response models:

```python
from pydantic import BaseModel
from typing import Optional, List

class WaveSession(BaseModel):
    surfer: str
    wave_count: int
    location: str
    notes: Optional[str] = None
    board_lengths: List[float] = []
```

Pydantic validates types, provides defaults, and generates JSON schemas automatically.

## Generators and yield

```python
def chunk_text(text: str, chunk_size: int = 300):
    """Split text into chunks — used in RAG document processing."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])

for chunk in chunk_text(long_document):
    process(chunk)
```

`yield` makes a generator — memory-efficient iteration without building the whole list at once. Used in the RAG tool for document chunking.

## Decorators

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Done: {result}")
        return result
    return wrapper

@log_call
def calculate(expression):
    return eval(expression)  # don't actually use eval, bro — use AST!
```

LangChain's `@tool` decorator works similarly — it wraps your function with metadata and schema generation.

## Common Standard Library Modules

| Module | What it does |
|---|---|
| `os` | Environment variables, file system ops |
| `pathlib` | Modern file path handling |
| `json` | JSON encode/decode |
| `ast` | Safe expression parsing (calculator tool!) |
| `math` | sqrt, sin, cos, log, pi, e |
| `logging` | Structured logging |
| `asyncio` | Async event loop, coroutines |
| `datetime` | Dates, times, timezones |
| `typing` | Type hint utilities (List, Dict, Optional) |
| `re` | Regular expressions |
