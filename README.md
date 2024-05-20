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
* The agent starts with 9 marines and must defeat 4 roaches. Every time
it defeats all of the roaches it gets 5 more marines as reinforcements and 4 new roaches
spawn. The reward is +10 per roach killed and −1 per marine killed. The more marines it
can keep alive, the more roaches it can defeat.
* Ends: After 120 seconds or no marine is left
* Deepmind human player: 41 [StarCraft II: A New Challenge for Reinforcement Learning](https://www.davidsilver.uk/wp-content/uploads/2020/03/starcraft_compressed.pdf)


| Model name | Total reward | Date | Result | Comment |
| - | - | - | - | - |
| gpt4_4o_2024_05_13 | 36 | 2024-05-20 | [results/defeatroaches/2024-05-20/gpt4_4o_2024_05_13](results/defeatroaches/2024-05-20/gpt4_4o_2024_05_13) | Chat Completion API |
| gpt4_turbo_2024_04_09 | 1 | 2024-05-20 | [results/defeatroaches/2024-05-20/gpt4_turbo_2024_04_09](results/defeatroaches/2024-05-20/gpt4_turbo_2024_04_09) | Chat Completion API |
| gpt_35_turbo_0125 | 1 | 2024-05-20 | [results/defeatroaches/2024-05-20/gpt_35_turbo_0125](results/defeatroaches/2024-05-20/gpt_35_turbo_0125) | Chat Completion API |

### CollectMineralShards
A map with 12 SCVs, 1 Command Center, 16 Mineral Fields and 4 Vespene Geysers.
Rewards are based on the total amount of Minerals and Vespene Gas collected.
Spending Minerals and Vespene Gas to train new units does not decrease your
reward tally. Optimal collection will require expanding your capacity to gather
Minerals and Vespene Gas by constructing additional SCVs and an additional
Command Center.
* End: After 300 seconds
* Deepmind human player: 6880

| Model name | Total reward | Date | Result | Comment |
| - | - | - | - | - |
| gpt_35_turbo_0125 | 2234 | 2024-05-20 | [results/collectmineralsandgas/2024-05-20/gpt_35_turbo_0125](results/collectmineralsandgas/2024-05-20/gpt_35_turbo_0125) | Chat Completion API |