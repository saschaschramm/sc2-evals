import json
import os
from typing import Generator

from sc2_evals.agents.openai.agent import FunctionDescription, Response
from sc2_evals.agents.openai.agent import (
    MessageResponse,
    ToolCallResponse,
    ToolOutputResponse,
)

from sc2_evals.agents import markdown
from sc2_evals.agents.base_logger import BaseLogger
from sc2_evals.agents.models import ModelInfo

class Logger(BaseLogger):

    def __init__(self, base_dir: str, model_info: ModelInfo, game: str) -> None:
        super().__init__(base_dir, game, model_info)
        self.total_tokens: int = 0
        self.total_costs: float = 0.0

    def log_system(self, instructions: str, functions: list[FunctionDescription]) -> None:
        text: str = markdown.headline("Instructions")
        text += markdown.code("markdown", instructions)
        text += markdown.headline("Functions")
        for function in functions:
            json_str: str = json.dumps(function.to_dict(), indent=4)
            text += markdown.strong(f"Function: {function._name}")
            text += f"{markdown.code('json', json_str)}"
        self.write_file(os.path.join(self._dir, f"0-system.md"), text)

    def _usage(self, prompt_tokens: int, completion_token: int) -> str:
        tokens: int = prompt_tokens + completion_token
        self.total_tokens += tokens
        self.total_costs += self._model_info.cost(prompt_tokens, completion_token)
        text: str = markdown.strong(f"Tokens: {tokens}")
        text += markdown.strong(f"Total tokens: {self.total_tokens}")
        text += markdown.strong(f"Total costs: {self.total_costs:.4f}")
        return text

    def log_user(self, step: int, content: str):
        text: str = markdown.headline("User message")
        text += markdown.code("markdown", content)
        self.write_file(os.path.join(self._dir, f"step-{step}-1-user.md"), text)

    def log_assistant(self, step: int, response: Response):
        print("---")
        index: int = 0
        text: str = ""
        message = response.message
        if isinstance(response, MessageResponse):
            text += markdown.headline(f"{index} Message")
            text += self._usage(
                prompt_tokens=response.completion_usage.prompt_tokens,
                completion_token=response.completion_usage.completion_tokens,
            )
            text += markdown.code("markdown", message["content"])

            print(f"Step {step} - index {index}")
            print(f"Message: {message['content']}")
            index += 1
        elif isinstance(response, ToolCallResponse):
            text += markdown.headline(f"{index} Tool Call")
            text += self._usage(
                prompt_tokens=response.completion_usage.prompt_tokens,
                completion_token=response.completion_usage.completion_tokens,
            )
            text += markdown.strong("Tool call:")
            text += markdown.code("json", json.dumps(message["function"], indent=4))

            print(f"Step {step} - index {index}")
            print(f"Tool call: {message['function']}")
            index += 1
        elif isinstance(response, ToolOutputResponse):
            text += markdown.strong("Tool output:")
            text += markdown.code("markdown", f"{message['content']}")
            if response.metadata is not None:
                # metadata is None if the tool call failed
                reward = response.metadata["reward"]
                self.total_reward += reward
                text += markdown.strong(f"Total reward: {self.total_reward}")
                print(f"Total reward: {self.total_reward}")
        else:
            raise Exception("Unknown response type")

        self.write_file(
            os.path.join(self._dir, f"step-{step}-2-assistant.md"), text
        )