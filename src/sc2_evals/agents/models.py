import enum


class Model(enum.Enum):
    DEPRECATED_GPT_35_TURBO_1106 = "gpt-3.5-turbo-1106"
    DEPRECATED_GPT4_0125_PREVIEW = "gpt-4-0125-preview"
    GPT_35_TURBO_0125 = "gpt-3.5-turbo-0125"
    GPT4_TURBO_2024_04_09 = "gpt-4-turbo-2024-04-09"
    GPT4_4O_2024_05_13 = "gpt-4o-2024-05-13"



class Price:

    def __init__(self, input: float, output: float) -> None:
        self.input: float = input
        self.output: float = output


class ModelInfo:

    def __init__(self, model: Model) -> None:
        self.model: Model = model
        self.price: Price = self._price(model)

    def _price(self, model: Model) -> Price:
        if model == Model.DEPRECATED_GPT_35_TURBO_1106:  # 2023
            return Price(0.001, 0.002)
        elif model == Model.GPT_35_TURBO_0125:  # 2024
            return Price(0.0005, 0.0015)
        elif model == Model.DEPRECATED_GPT4_0125_PREVIEW:  # 2024
            return Price(0.01, 0.03)
        elif model == Model.GPT4_TURBO_2024_04_09:
            return Price(0.01, 0.03)
        elif model == Model.GPT4_4O_2024_05_13:
            return Price(0.005, 0.015)

        else:
            raise ValueError(f"Unknown model: {model}")

    def cost(self, prompt_tokens: int, completion_token: int) -> float:
        return (prompt_tokens * self.price.input + completion_token * self.price.output) / 1000
