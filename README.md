# sc2 evals
This repository evaluates policy models like GPT-4 on StarCraft II.

## Install
**Python 3.10 required**

Clone this repository and install the dependencies with the following commands:

```bash
pip install -r requirements.txt
python -m pip install --editable .
```

Download the [mini games](https://github.com/deepmind/pysc2/releases/download/v1.2/mini_games.zip) and extract them to the following directory:
```bash
/StarCraft II/Maps/mini_games
```

## Helpful commands
Run an agent to test the environment.
```bash
python -m pysc2.bin.agent --map DefeatRoaches
```

## Results
### Defeat Roaches
| Model name | Total reward | Date | Result | Comment |
| - | - | - | - | - |
| gpt-4-turbo-2024-04-09 | 47 | 2024-04-28 | [results/defeatroaches/2024-04-28/gpt4_turbo_2024_04_09](results/defeatroaches/2024-04-28/gpt4_turbo_2024_04_09) | Chat completion API
| gpt-3.5-turbo-0125 | 72 | 2024-04-28 | [results/defeatroaches/2024-04-28/gpt_35_turbo_0125](results/defeatroaches/2024-04-28/gpt_35_turbo_0125) | Chat completion API
