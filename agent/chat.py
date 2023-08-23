# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import copy
import dataclasses
import enum
from typing import Literal
from typing import Self
from typing import TypeVar
from typing import overload

# Can be replaced by Self in Python 3.11
TChatSequence = TypeVar("TChatSequence", bound="ChatSequence")


class TMessage(abc.ABC):
    @abc.abstractmethod
    def __iter__(self):
        ...


AbcTMessage = TMessage


class AbcChatSequence(abc.ABC):
    messages: list[TMessage]

    @abc.abstractmethod
    def add(self, *args, **kwargs) -> None:
        ...

    @abc.abstractmethod
    def raw(self):
        ...

    @overload
    def __getitem__(self: Self, key: int) -> TMessage:
        pass

    @overload
    def __getitem__(self: Self, key: slice) -> Self:
        pass

    def __getitem__(self: Self, key: int | slice) -> TMessage | Self:
        if isinstance(key, slice):
            other = copy.deepcopy(self)
            other.messages = self.messages[key]
            return other
        return self.messages[key]


@dataclasses.dataclass
class Message(TMessage):
    """default implementation of TMessage"""
    role: Literal['system', 'assistant', 'user']
    content: str

    class ROLE(enum.Enum):
        system = "system"
        assistant = "assistant"
        user = "user"

    def __iter__(self):
        return iter(dataclasses.asdict(self).items())


@dataclasses.dataclass
class OpenaiChatSequence(AbcChatSequence):
    messages: list[Message] = dataclasses.field(default_factory=lambda: [])

    def add(self, role: Message.ROLE, content: str):
        self.messages.append(Message(role.value, content))  # noqa

    def extend(self, messages: list[Message]):
        self.messages.extend(messages)

    @property
    def token_length(self):
        from agent.utils import count_tokens
        return count_tokens(self.messages)

    def raw(self) -> list[dict]:
        return list(map(dict, self.messages))


ChatSequence = OpenaiChatSequence
"""default ChatSequence"""

__all__ = ['ChatSequence', 'Message', 'AbcChatSequence', 'AbcTMessage']
