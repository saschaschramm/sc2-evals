from datetime import datetime
import os
import shutil

from sc2_evals.agents.models import ModelInfo


class BaseLogger:

    def __init__(self, base_dir: str, game: str, model_info: ModelInfo) -> None:
        self.total_reward: int = 0
        self._timestamp: str = datetime.now().strftime("%Y-%m-%d")
        self._model_info: ModelInfo = model_info
        self._dir: str = self._init_dir(base_dir, game, model_info.model.name.lower())

    def write_file(self, file_path: str, string: str) -> None:
        with open(file=file_path, mode="a", encoding="utf-8") as file:
            file.write(string)

    def _init_dir(self, base_dir: str, game: str, model_name: str) -> str:
        dir: str = os.path.join(base_dir, game, f"{self._timestamp}", f"{model_name}")
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(name=dir, exist_ok=False)
        return dir

    def log_stats(self) -> None:
        model_name = self._model_info.model.name.lower()
        headers = ["Model name", "Total reward", "Date", "Result", "Comment"]
        rows = []
        row: str = " | ".join(headers)
        row = f"| {row} |"
        rows.append(row)

        row = " | ".join(["-"] * len(headers))
        row = f"| {row} |"
        rows.append(row)

        row = " | ".join(
            [
                model_name,
                str(self.total_reward),
                self._timestamp,
                f"[{self._dir}]({self._dir})",
                "Chat Completion API",
            ]
        )
        row = f"| {row} |"
        rows.append(row)
        text = "\n".join(rows)
        with open(
            file=os.path.join(self._dir, "stats.md"), mode="w", encoding="utf-8"
        ) as file:
            file.write(text)
