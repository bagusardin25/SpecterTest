"""SSE Manager — Server-Sent Events broadcasting for real-time frontend updates."""
import json
import queue
import threading
from typing import Generator


class SSEManager:
    """Thread-safe SSE manager that supports multiple subscribers per scan."""

    def __init__(self):
        self._subscribers: dict[str, list[queue.Queue]] = {}
        self._lock = threading.Lock()

    def subscribe(self, scan_id: str) -> queue.Queue:
        """Register a new subscriber for a scan_id. Returns a Queue."""
        q = queue.Queue()
        with self._lock:
            if scan_id not in self._subscribers:
                self._subscribers[scan_id] = []
            self._subscribers[scan_id].append(q)
        return q

    def unsubscribe(self, scan_id: str, q: queue.Queue):
        """Remove a subscriber queue."""
        with self._lock:
            if scan_id in self._subscribers:
                try:
                    self._subscribers[scan_id].remove(q)
                except ValueError:
                    pass
                if not self._subscribers[scan_id]:
                    del self._subscribers[scan_id]

    def publish(self, scan_id: str, event: str, data: dict):
        """Send an event to all subscribers of a scan_id."""
        message = f"event: {event}\ndata: {json.dumps(data)}\n\n"
        with self._lock:
            queues = self._subscribers.get(scan_id, [])
            for q in queues:
                try:
                    q.put_nowait(message)
                except queue.Full:
                    pass  # Drop if subscriber is too slow

    def stream(self, scan_id: str) -> Generator[str, None, None]:
        """Generator that yields SSE messages for a given scan_id."""
        q = self.subscribe(scan_id)
        try:
            while True:
                try:
                    message = q.get(timeout=30)
                    yield message
                except queue.Empty:
                    # Send keepalive comment to prevent connection timeout
                    yield ": keepalive\n\n"
        except GeneratorExit:
            self.unsubscribe(scan_id, q)


# Global singleton
sse_manager = SSEManager()
