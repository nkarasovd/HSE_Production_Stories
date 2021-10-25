import argparse
from typing import Any, Dict

import torch.cuda
from ray.rllib.agents.ppo import ppo

import wandb


def get_ppo_standard_config() -> Dict[str, Any]:
    ppo_config = ppo.DEFAULT_CONFIG.copy()
    if torch.cuda.is_available():
        ppo_config["num_gpus"] = 1
    else:
        ppo_config["num_gpus"] = 0
        ppo_config["num_gpus_per_worker"] = 0
    ppo_config["log_level"] = "INFO"
    ppo_config["framework"] = "torch"
    ppo_config["env"] = "ModifiedDungeon"
    ppo_config["env_config"] = {
        "width": 20,
        "height": 20,
        "max_rooms": 3,
        "min_room_xy": 5,
        "max_room_xy": 10,
        "observation_size": 11,
        "vision_radius": 5,
        "reward_type": "basic"
    }

    ppo_config["model"] = {
        "conv_filters": [
            [16, (3, 3), 2],
            [32, (3, 3), 2],
            [32, (3, 3), 1],
        ],
        "post_fcnet_hiddens": [32],
        "post_fcnet_activation": "relu",
        "vf_share_layers": False,
    }

    ppo_config["rollout_fragment_length"] = 100
    ppo_config["entropy_coeff"] = 0.1
    ppo_config["lambda"] = 0.95
    ppo_config["vf_loss_coeff"] = 1.0

    return ppo_config


def ppo_run_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PPO Run")
    parser.add_argument("--max_iters", type=int, default=500,
                        help="Number of iterations")
    parser.add_argument("--reward_type", type=str, default="reward_new_cell",
                        choices=["basic", "reward_new_cell", "reward_new_explored"],
                        help="Agent reward type")

    return parser.parse_args()


def log_result(result: Dict[str, Any]):
    wandb.log({'episode_reward_mean': result["episode_reward_mean"]})
    wandb.log({'episode_reward_min': result["episode_reward_min"]})
    wandb.log({'episode_reward_max': result["episode_reward_max"]})
    wandb.log({'episode_len_mean': result["episode_len_mean"]})
    wandb.log({"entropy": result["info"]["learner"]["default_policy"]["learner_stats"]["entropy"]})
    wandb.log({"vf_loss": result["info"]["learner"]["default_policy"]["learner_stats"]["vf_loss"]})
    wandb.log({"policy_loss": result["info"]["learner"]["default_policy"]["learner_stats"]["policy_loss"]})
    wandb.log({"total_loss": result["info"]["learner"]["default_policy"]["learner_stats"]["total_loss"]})
