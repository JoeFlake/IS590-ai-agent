# Python Programming Reference

## Data Structures
- **list**: ordered, mutable sequence. `append()`, `extend()`, `pop()`, slicing `lst[1:3]`.
- **dict**: key-value pairs. `dict.get(key, default)`, `dict.items()`, `dict.keys()`.
- **set**: unordered unique elements. Supports union `|`, intersection `&`, difference `-`.
- **tuple**: immutable ordered sequence. Used for unpacking: `a, b = (1, 2)`.

## List Comprehensions
```python
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]
matrix  = [[r*c for c in range(3)] for r in range(3)]
```

## Generators
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```
Generators are lazy — values are produced on demand, saving memory.

## Decorators
```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def greet(name): return f"Hello, {name}"
```

## Async / Await
```python
import asyncio

async def fetch_data(url):
    await asyncio.sleep(1)  # non-blocking wait
    return {"data": "..."}

async def main():
    result = await fetch_data("https://example.com")
```
Use `asyncio.gather()` to run multiple coroutines concurrently.

## Type Hints
```python
from typing import Optional, List, Dict

def process(items: List[str], limit: Optional[int] = None) -> Dict[str, int]:
    return {item: len(item) for item in items[:limit]}
```

## Context Managers
```python
with open("file.txt", "r") as f:
    content = f.read()
# file is automatically closed

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer():
    import time; start = time.time()
    yield
    print(f"Elapsed: {time.time() - start:.2f}s")
```

## Common Libraries
- **requests**: HTTP calls. `requests.get(url).json()`
- **pathlib.Path**: modern file paths. `Path("dir") / "file.txt"`
- **dataclasses**: `@dataclass` auto-generates `__init__`, `__repr__`.
- **pydantic**: data validation with type hints, used heavily in FastAPI.
- **dotenv**: load `.env` files with `load_dotenv()`.
