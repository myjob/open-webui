# Sending Event Tags from Backend to Frontend in Open WebUI

Open WebUI provides a built-in mechanism to send real-time "event tags" (like "Thinking...", "Generating...", or custom status updates) from backend tools/functions to the frontend UI using the `__event_emitter__`.

## How it Works

When defining a Tool or Function in Open WebUI, you can request the `__event_emitter__` callable by adding it to your function signature. The system automatically injects this function at runtime.

### 1. Function Signature

Add `__event_emitter__` as an argument to your function. It should be typed as a `Callable` or `Any`.

```python
from typing import Callable, Any

class Tools:
    async def my_tool_function(
        self, 
        input_data: str, 
        __event_emitter__: Callable[[Any], Any] = None
    ) -> str:
        # Implementation...
        pass
```

### 2. Sending Status Events ("Thinking...")

To show a status update (event tag) in the UI, emit an event with `type: "status"`.

```python
if __event_emitter__:
    await __event_emitter__(
        {
            "type": "status",
            "data": {
                "description": "Searching database...",
                "done": False,
            },
        }
    )
```

The UI will display "Searching database..." with a loading indicator.

### 3. Completing the Status

When the action is finished, send another event with `done: True` to remove the loading state for that specific operation (though usually the tool returning will also effectively end the "thinking" state of the main generation, explicit updates are good for multi-step tools).

```python
if __event_emitter__:
    await __event_emitter__(
        {
            "type": "status",
            "data": {
                "description": "Search complete.",
                "done": True,
            },
        }
    )
```

## Other Supported Event Types

The `__event_emitter__` supports several other event types processed by `open_webui/socket/main.py`:

- **`message`**: Appends text to the current message content.
    ```python
    await __event_emitter__({"type": "message", "data": {"content": "Found 5 results.\n"}})
    ```
- **`replace`**: Replaces the entire message content.
    ```python
    await __event_emitter__({"type": "replace", "data": {"content": "New content."}})
    ```
- **`source`** / **`citation`**: Adds a source citation.
    ```python
    await __event_emitter__({
        "type": "source", 
        "data": {
            "source": {"name": "Doc 1", "url": "..."}, 
            "document": [...]
        }
    })
    ```

## Testing Locally

If you are writing a manual test script (like `test_celex_tool.py`), you need to mock the emitter since it won't be injected automatically outside the Open WebUI runtime.

```python
# Mock implementation for testing
async def mock_emitter(event):
    print(f"Server Event: {event}")

# Call your tool with the mock
await tool.get_celex_timeline(celex_id, __event_emitter__=mock_emitter)
```
