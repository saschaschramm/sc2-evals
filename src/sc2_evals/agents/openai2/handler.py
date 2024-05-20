from typing import Any

from typing_extensions import override
from openai import AssistantEventHandler

from sc2_evals.agents.function_description import FunctionDescription
from sc2_evals.agents.openai2.logger import Logger
from openai.types.beta.assistant_stream_event import ThreadRunRequiresAction, ThreadMessageCompleted, ThreadCreated, ThreadRunStepFailed, ThreadRunFailed, ThreadRunStepCompleted

class EventHandler(AssistantEventHandler):

    def __init__(self, client, functions: list[FunctionDescription], logger: Logger):
        super().__init__()
        self.client = client
        self._functions = functions
        self._logger = logger
        self._tool_outputs = []

    @override
    def on_event(self, event):
        if isinstance(event, ThreadRunRequiresAction):
            print("=== tool")
            tool_calls = event.data.required_action.submit_tool_outputs.tool_calls
            tool_outputs: list[dict[str, Any]] = []
            for tool_call in tool_calls:
                functions: list[FunctionDescription] = [
                    function for function in self._functions if function._name == tool_call.function.name
                ]
                if len(functions) == 0:
                    # TODO Return valid tools
                    raise NotImplementedError(f"Unknown tool {tool_call.function.name}. Valid tools are .")
                else:
                    output: dict[str, Any] = functions[0](tool_call.function.arguments)
                    self._logger.log_tool(tool_call, output)
                    tool_outputs.append({"tool_call_id": tool_call.id, "output": output["content"]})

            with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(self.client, functions=self._functions, logger=self._logger),
            ) as stream:
                stream.until_done()
        elif isinstance(event, ThreadMessageCompleted):
            print("=== message")
            print(event.data.content[0].text.value)
            self._logger.log_assistant_message(event.data)

        elif isinstance(event, ThreadCreated):
            raise Exception("Thread created", event)
        elif isinstance(event, ThreadRunStepFailed):
            raise Exception("Thread run step failed", event)
        elif isinstance(event, ThreadRunFailed):
            raise Exception("Thread run failed", event)
        elif isinstance(event, ThreadRunStepCompleted):
            #print("=== thread.run.step.completed")
            assert event.data.usage is not None

            print(event.data.usage.prompt_tokens)
            self._logger.log_costs(event.data.usage.prompt_tokens, 
                                   event.data.usage.completion_tokens)