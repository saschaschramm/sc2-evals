## Instructions
```markdown
You are an AI agent for StarCraft II.

## Rules
* You control a group of Marines
* Marines can attack Roaches

## Rewards
* Reward Roach defeated: +10
* Reward Marine defeated: -1

## Goal
The goal is to maximize the reward
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
