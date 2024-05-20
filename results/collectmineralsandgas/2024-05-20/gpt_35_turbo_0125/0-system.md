## Instructions
```markdown
You are an AI agent for StarCraft II.

### Map
A map with 12 SCVs, 1 Command Center, 16 Mineral Fields and 4 Vespene Geysers. 

### Rewards
Rewards are based on the total amount of Minerals and Vespene Gas collected. 
Spending Minerals and Vespene Gas to train new units does not decrease your reward tally. 
Optimal collection will require expanding your capacity to gather Minerals and Vespene 
Gas by constructing additional SCVs and an additional Command Center.

### Goal
Maximize the reward.
```
## Functions
**Function: act_screen**  
```json
{
    "name": "act_screen",
    "description": "",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "Harvest_Gather_screen",
                        "select_rect",
                        "select_point",
                        "Build_Refinery_screen",
                        "Build_CommandCenter_screen",
                        "Attack_screen"
                    ],
                    "description": "Action name"
                }
            },
            "x1": {
                "type": "integer",
                "description": "Screen position x",
                "minimum": 0,
                "maximum": 31
            },
            "y1": {
                "type": "integer",
                "description": "Screen position y",
                "minimum": 0,
                "maximum": 31
            },
            "x2": {
                "type": "integer",
                "description": "Screen position x",
                "minimum": 0,
                "maximum": 31
            },
            "y2": {
                "type": "integer",
                "description": "Screen position y",
                "minimum": 0,
                "maximum": 31
            }
        }
    }
}
```
**Function: act**  
```json
{
    "name": "act",
    "description": "",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "select_idle_worker",
                        "Train_SCV_quick",
                        "select_army",
                        "Stop_quick",
                        "HoldPosition_quick"
                    ],
                    "description": "Action name"
                }
            }
        }
    }
}
```
