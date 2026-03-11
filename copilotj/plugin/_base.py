# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import abc
import enum
import functools
from typing import ClassVar, Type, cast, override

import pydantic

__all__ = ["Request", "Response", "ResponseWithDescribeInfo", "FromTo"]


@functools.total_ordering
class Verbosity(enum.Enum):
    """Enum for verbosity levels."""

    LOW = enum.auto()
    NORMAL = enum.auto()
    HIGH = enum.auto()

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Response(pydantic.BaseModel, abc.ABC):
    @abc.abstractmethod
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]: ...

    def describe(self, *, level: int = 1, verbosity: Verbosity = Verbosity.NORMAL) -> str:
        return "\n".join(self._describe(level=level, verbosity=verbosity))

    def describe_with(self, *, level: int | None = None, verbosity: Verbosity | None = None) -> "Response":
        if level is None and verbosity is None:
            return self

        return ResponseWithDescribeInfo(self, level=level, verbosity=verbosity)

    def __str__(self) -> str:
        return self.describe()


class ResponseWithDescribeInfo[T: Response](Response, abc.ABC):
    def __init__(self, response: T, *, level: int | None = None, verbosity: Verbosity | None = None):
        self.response = response
        self.level = level
        self.verbosity = verbosity

    @override
    def _describe(self, *, level: int, verbosity: Verbosity) -> list[str]:
        return self.response._describe(level=level, verbosity=verbosity)

    @override
    def describe(self, *, level: int | None = None, verbosity: Verbosity | None = None) -> str:
        match (level, verbosity):
            case (None, None):
                _level = self.level
                _verbosity = self.verbosity
            case (_, None):
                _level = level
                _verbosity = self.verbosity
            case (None, _):
                _level = self.level
                _verbosity = verbosity
            case _:
                _level = level
                _verbosity = verbosity

        match (_level, _verbosity):
            case (None, None):
                return super().describe()
            case (_, None):
                return super().describe(level=_level)
            case (None, _):
                return super().describe(verbosity=_verbosity)
            case _:
                return super().describe(level=_level, verbosity=_verbosity)

    @override
    def describe_with(self, *, level: int | None = None, verbosity: Verbosity | None = None) -> Response:
        match (level, verbosity):
            case (None, None):
                return self
            case (_, None):
                return ResponseWithDescribeInfo(self.response, level=level, verbosity=self.verbosity)
            case (None, _):
                return ResponseWithDescribeInfo(self.response, level=self.level, verbosity=verbosity)
            case _:
                return ResponseWithDescribeInfo(self.response, level=level, verbosity=verbosity)


class Request[R: Response](pydantic.BaseModel):
    _event: ClassVar[str | None]
    _response_type: ClassVar[Type[Response] | None]
    _timeout: ClassVar[float | None]

    def __init_subclass__(
        cls, *, event: str | None = None, response_type: Type[R] | None = None, timeout: float | None = None, **kwargs
    ):
        super().__init_subclass__(**kwargs)
        cls._event = event
        cls._response_type = response_type  # TODO: automatic get from R
        cls._timeout = timeout

    @property
    def event(self) -> str:
        assert self._event is not None
        return self._event

    @property
    def response_type(self) -> Type[R]:
        assert self._response_type is not None
        return cast(Type[R], self._response_type)


class FromTo[T](pydantic.BaseModel):
    from_: T = pydantic.Field(alias="from")
    to: T

    def __str__(self) -> str:
        return f"{self.from_} -> {self.to}"
