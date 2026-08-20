"""
PARTH ASSISTANT AI — Rate Limiter Engine
Tracks request frequencies per user session and prevents automated flooding.
"""

import time
from typing import Dict, List
from fastapi import HTTPException, status


class RateLimiter:
    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.history: Dict[str, List[float]] = {}

    def check_rate_limit(self, identifier: str):
        now = time.time()
        if identifier not in self.history:
            self.history[identifier] = []

        # Remove timestamps outside window
        self.history[identifier] = [ts for ts in self.history[identifier] if now - ts < self.window_seconds]

        if len(self.history[identifier]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.max_requests} requests per {self.window_seconds} seconds."
            )

        self.history[identifier].append(now)


rate_limiter = RateLimiter(max_requests=1000, window_seconds=60)

