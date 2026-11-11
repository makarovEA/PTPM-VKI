from __future__ import annotations

from abc import ABC, abstractmethod


class ExternalDependency(ABC):
    @abstractmethod
    def send_result(self, result: str) -> None:
        raise NotImplementedError


class EmailServerStub(ExternalDependency):
    def __init__(self) -> None:
        self.sent_messages: list[str] = []

    def send_result(self, result: str) -> None:
        self.sent_messages.append(result)