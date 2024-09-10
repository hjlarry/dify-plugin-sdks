from collections.abc import Generator
from typing import Literal, overload
from dify_plugin.core.entities.invocation import InvokeType
from dify_plugin.core.runtime import BackwardsInvocation


class WorkflowAppInvocation(BackwardsInvocation[dict]):
    @overload
    def invoke(
        self,
        app_id: str,
        inputs: dict,
        response_mode: Literal["streaming"],
        files: list,
    ) -> Generator[dict, None, None]: ...

    @overload
    def invoke(
        self,
        app_id: str,
        inputs: dict,
        response_mode: Literal["blocking"],
        files: list,
    ) -> dict: ...

    def invoke(
        self,
        app_id: str,
        inputs: dict,
        response_mode: Literal["streaming", "blocking"],
        files: list,
    ) -> Generator[dict, None, None] | dict:
        """
        Invoke workflow app
        """
        response = self._backwards_invoke(
            InvokeType.App,
            dict,
            {
                "app_id": app_id,
                "inputs": inputs,
                "response_mode": response_mode,
                "files": files,
            },
        )

        if response_mode == "streaming":
            return response

        for data in response:
            return data

        raise Exception("No response from workflow")