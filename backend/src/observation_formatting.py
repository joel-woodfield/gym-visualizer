import numpy as np

FORMATS = {
    "ocatari/AirRaid": {
        "objects": [
            "Player",
            "Building-1",
            "Building-2",
            "Building-3",
            "Enemy25-1",
            "Enemy25-2",
            "Enemy25-3",
            "Enemy50-1",
            "Enemy50-2",
            "Enemy50-3",
            "Enemy75-1",
            "Enemy75-2",
            "Enemy75-3",
            "Enemy100-1",
            "Enemy100-2",
            "Enemy100-3",
            "Missile-1",
            "Missile-2",
        ],
        "type": "relative_indicator",
    },
    "ocatari/Asterix": {
        "objects": [
            "Player",
            "Reward-1",
            "Reward-2",
            "Reward-3",
            "Reward-4",
            "Reward-5",
            "Reward-6",
            "Reward-7",
            "Reward-8",
            "Enemy-1",
            "Enemy-2",
            "Enemy-3",
            "Enemy-4",
            "Enemy-5",
            "Enemy-6",
            "Enemy-7",
            "Enemy-8",
            "Consumable-1",
            "Consumable-2",
            "Consumable-3",
            "Consumable-4",
            "Consumable-5",
            "Consumable-6",
            "Consumable-7",
            "Consumable-8",
        ],
        "type": "relative_indicator",
    },
    "ocatari/Bowling": {
        "objects": [
            "Player",
            "Ball",
            "Pin-1",
            "Pin-2",
            "Pin-3",
            "Pin-4",
            "Pin-5",
            "Pin-6",
            "Pin-7",
            "Pin-8",
            "Pin-9",
            "Pin-10",
        ],
        "type": "relative_indicator",
    },
    "ocatari/Boxing": {
        "objects": [
            "Player",
            "Enemy",
        ],
        "type": "relative_indicator",
    },
    "CartPole-v1": {
        "objects": [
            "x",
            "v",
            "theta",
            "omega",
        ],
        "type": "regular",
    }
}


def format_obs(env_id: str, obs: np.ndarray) -> list[str]:
    new = []
    if env_id not in FORMATS:
        for val in obs:
            new.append(f"{val:.2f}")
    else:
        if FORMATS[env_id]["type"] == "relative_indicator":
            object_names = FORMATS[env_id]["objects"]
            num_objects = len(object_names)
            for i in range(num_objects):
                base_idx = i * 3
                x = obs[base_idx]
                y = obs[base_idx + 1]
                indicator = obs[base_idx + 2]
                new.append(f"{object_names[i]}-x: {x}")
                new.append(f"{object_names[i]}-y: {y}")
                new.append(f"{object_names[i]}-e: {indicator}")
        elif FORMATS[env_id]["type"] == "regular":
            object_names = FORMATS[env_id]["objects"]
            for i, name in enumerate(object_names):
                val = obs[i]
                new.append(f"{name}: {val:.2f}")
        else:
            raise NotImplementedError

    return new
        
