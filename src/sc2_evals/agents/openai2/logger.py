from datetime import datetime
import json
import os
import shutil
from typing import Any

from openai.types.beta.threads import Message
from sc2_evals.agents.models import Model, ModelInfo
from sc2_evals.agents.openai2 import markdown
from sc2_evals.agents.function_description import FunctionDescription


def write_file(file_path: str, string: str) -> None:
    with open(file=file_path, mode="a", encoding="utf-8") as file:
        file.write(string)


STEP_FILENAME = "step-{step}.md"

class Logger:


    def _usage(self, prompt_tokens: int, completion_token: int) -> str:
        tokens: int = prompt_tokens + completion_token
        self.total_tokens += tokens
        self.total_costs += self._model_info.cost(prompt_tokens, completion_token)

        """
        prompt 1: hello, prompt_tokens=1
        prompt 2: hello, prompt_tokens=2
        prompt 3: hello, prompt_tokens=3
        total_prompt_tokens = 6"""

        text: str = "\n"
        text += f"| Tokens | Total tokens | Total costs |\n"
        text += f"| --- | --- | --- |\n"
        text += f"| {tokens} | {self.total_tokens} | {self.total_costs:.4f} |\n"
        return text

    def _init_dir(self, base_dir: str, game: str, model_name: str) -> str:
        timestamp: str = datetime.now().strftime("%Y-%m-%d")
        dir = os.path.join(base_dir, game, f"{timestamp}", f"{model_name}")
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.mkdir(base_dir)
        os.mkdir(os.path.join(base_dir, game))
        os.mkdir(os.path.join(base_dir, game, f"{timestamp}"))
        os.mkdir(dir)
        return dir

    def __init__(self, dir: str, model_info: ModelInfo, game: str) -> None:
        self.total_reward: int = 0
        self._dir: str = self._init_dir(dir, game, model_info.model.name.lower())
        self.total_tokens: int = 0
        self.total_costs: float = 0    
        self._model_info: ModelInfo = model_info
        #self._game = game
        self._step: int = 0
        self._total_reward: int = 0

    def log_user_message(self, role: str, content: str) -> None:

        text: str = markdown.headline(level=3, text=f"{role}")
            #text += f"{message.id}\n"
        text += markdown.code("markdown", content)
        write_file(
                os.path.join(self._dir, STEP_FILENAME.format(step=self._step)), text
        )

    def log_system_message(self, instructions: str, functions: list[FunctionDescription]) -> None:
        text: str = markdown.headline(level=3, text="Instructions")
        text += markdown.code("markdown", instructions)
        text += markdown.headline(level=3, text="Functions")
        for function in functions:
            json_str: str = json.dumps(function.to_dict(), indent=4)
            text += markdown.strong(f"Function: {function._name}")
            text += f"{markdown.code('json', json_str)}"
        write_file(
            os.path.join(self._dir, f"system.md"), text
        )


    def log_assistant_message(self, message: Message) -> None:
        if len(message.content) != 1:
            raise ValueError("Unknown message content")
        else:
            text: str = markdown.headline(level=3, text=f"{message.role}")
            #text += f"{message.id}\n"
            text += markdown.code("markdown", message.content[0].text.value)
        write_file(
                os.path.join(self._dir, STEP_FILENAME.format(step=self._step)), text
        )

    def log_tool(self, tool_call, output: dict[str, Any]) -> None:
        text: str = markdown.headline(level=3, text=f"tool")
        text += markdown.code("python", f"{tool_call.function}")
        text += markdown.code("markdown", f"{output['content']}")
        if output["metadata"] is not None:
            # metadata is None if the tool call failed
            reward: int = output["metadata"]["reward"]
            self._total_reward += reward
            text += markdown.strong(f"Total reward: {self._total_reward}")
        write_file(
                os.path.join(self._dir, STEP_FILENAME.format(step=self._step)), text
        )

    def log_costs(self, prompt_tokens: int, completion_tokens: int) -> None:
        text: str = self._usage(
            prompt_tokens=prompt_tokens,
            completion_token=completion_tokens,
        )
        write_file(
                os.path.join(self._dir, STEP_FILENAME.format(step=self._step)), text
        )