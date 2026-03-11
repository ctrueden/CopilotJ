# SPDX-FileCopyrightText: Copyright contributors to the CopilotJ project.
#
# SPDX-License-Identifier: Apache-2.0

import abc
import asyncio
import functools
import inspect
import typing
from collections.abc import Callable
from typing import Annotated, Any, Mapping, NotRequired, Sequence, Type, TypedDict, override

import jsonref
import pydantic
from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined

__all__ = ["Tool", "FunctionTool", "ToolSchema", "ParametersSchema"]


class ParametersSchema(TypedDict):
    type: str
    properties: dict[str, Any]
    required: NotRequired[Sequence[str]]
    additionalProperties: NotRequired[bool]


class ToolSchema(TypedDict):
    parameters: NotRequired[ParametersSchema]
    name: str
    description: NotRequired[str]
    strict: NotRequired[bool]


class Tool(pydantic.BaseModel, abc.ABC):
    @pydantic.computed_field
    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @pydantic.computed_field
    @property
    def display_name(self) -> str:
        return self.name.replace("_", " ").title()

    @pydantic.computed_field
    @property
    @abc.abstractmethod
    def description(self) -> str: ...

    @property
    @abc.abstractmethod
    def json_schema(self) -> ToolSchema: ...

    @abc.abstractmethod
    def args_type(self) -> Type[BaseModel]: ...

    @abc.abstractmethod
    def return_type(self) -> Type[Any]: ...

    @abc.abstractmethod
    def state_type(self) -> Type[BaseModel] | None: ...

    @abc.abstractmethod
    async def run(self, args: BaseModel) -> BaseModel: ...

    async def run_json(self, args: Mapping[str, Any]) -> Any:
        return await self.run(self.args_type().model_validate(args))


class FunctionTool(Tool):
    def __init__(
        self,
        func: Callable[..., Any],
        description: str,
        name: str | None = None,
        *,
        strict: bool = False,
        display_name: str | None = None,
    ) -> None:
        super().__init__()
        self._func = func
        self._description = description
        self._strict = strict
        signature = inspect.signature(func)
        self._name = name or func.func.__name__ if isinstance(func, functools.partial) else name or func.__name__
        assert self._name is not None, "Name is not set"
        self._display_name = display_name
        self._args_type = _args_base_model_from_signature(self._name, signature)
        self._return_type = signature.return_annotation

    @property
    @override
    def name(self) -> str:
        return self._name

    @property
    @override
    def display_name(self) -> str:
        if self._display_name is not None:
            return self._display_name

        return super().display_name

    @property
    @override
    def description(self) -> str:
        return self._description

    @property
    @override
    def json_schema(self) -> ToolSchema:
        model_schema: dict[str, Any] = self._args_type.model_json_schema()

        if "$defs" in model_schema:
            model_schema = typing.cast(dict[str, Any], jsonref.replace_refs(obj=model_schema, proxies=False))  # type: ignore
            del model_schema["$defs"]

        parameters = ParametersSchema(
            type="object",
            properties=model_schema["properties"],
            required=model_schema.get("required", []),
            additionalProperties=model_schema.get("additionalProperties", False),
        )

        # If strict is enabled, the tool schema should list all properties as required.
        assert "required" in parameters
        if self._strict and set(parameters["required"]) != set(parameters["properties"].keys()):
            raise ValueError(
                "Strict mode is enabled, but not all input arguments are marked as required. Default arguments are not allowed in strict mode."
            )

        assert "additionalProperties" in parameters
        if self._strict and parameters["additionalProperties"]:
            raise ValueError(
                "Strict mode is enabled but additional argument is also enabled. This is not allowed in strict mode."
            )

        tool_schema = ToolSchema(
            name=self._name,
            description=self._description,
            parameters=parameters,
            strict=self._strict,
        )
        return tool_schema

    @override
    def args_type(self) -> Type[BaseModel]:
        return self._args_type

    @override
    def return_type(self) -> Type[Any]:
        return self._return_type

    @override
    def state_type(self) -> Type[BaseModel] | None:
        return None

    @override
    async def run(self, args: BaseModel) -> Any:
        if asyncio.iscoroutinefunction(self._func):
            result = await self._func(**args.model_dump())
        else:
            future = asyncio.get_event_loop().run_in_executor(None, functools.partial(self._func, **args.model_dump()))
            result = await future

        return result


def _args_base_model_from_signature(tool_name: str, sig: inspect.Signature) -> Type[BaseModel]:
    fields: dict[str, tuple[Type[Any], Any]] = {}
    for param_name, param in sig.parameters.items():
        if param.annotation is inspect.Parameter.empty:
            raise ValueError("No annotation")

        type = _normalize_annotated_type(param.annotation)
        description = _type2description(param_name, param.annotation)
        default_value = param.default if param.default is not inspect.Parameter.empty else PydanticUndefined

        fields[param_name] = (
            type,
            Field(default=default_value, description=description),
        )

    return typing.cast(BaseModel, pydantic.create_model(tool_name + "Args", **fields))  # type: ignore


def _normalize_annotated_type(type_hint: Type[Any]) -> Type[Any]:
    """Normalize typing.Annotated types to the inner type."""
    if typing.get_origin(type_hint) is Annotated:
        # Extract the inner type from Annotated
        return typing.get_args(type_hint)[0]  # type: ignore

    return type_hint


def _type2description(k: str, v: Annotated[Type[Any] | str, Type[Any]]) -> str:
    # handles Annotated
    if hasattr(v, "__metadata__"):
        retval = v.__metadata__[0]  # type: ignore
        if isinstance(retval, str):
            return retval
        else:
            raise ValueError(f"Invalid description {retval} for parameter {k}, should be a string.")
    else:
        return k
