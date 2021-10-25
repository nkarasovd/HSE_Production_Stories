import numpy as np
import ray
import torch
from PIL import Image
from ray import tune
from ray.rllib.agents.ppo import ppo

import wandb
from modified_env import ModifiedDungeon
from utils import get_ppo_standard_config, ppo_run_parser, log_result


def train_ppo(max_iters: int = 250, reward_type: str = "basic"):
    ray.shutdown()
    ray.init(ignore_reinit_error=True)
    tune.register_env("ModifiedDungeon", lambda config: ModifiedDungeon(**config))

    directory_root = "tmp/ppo/modified_dungeon"

    ppo_config = get_ppo_standard_config()
    ppo_config["env_config"]["reward_type"] = reward_type

    ppo_agent = ppo.PPOTrainer(ppo_config)

    wandb.init(project='prod_stories_task_5', config=ppo_config)

    for n in range(max_iters):
        result = ppo_agent.train()
        file_name = ppo_agent.save(directory_root)
        if n % 50 == 0:
            wandb.save(file_name)

        log_result(result)

        print(f"Epoch {n:3d} | min reward {result['episode_reward_min']:8.2f} | "
              f"mean reward {result['episode_reward_mean']:8.2f} | "
              f"max reward {result['episode_reward_max']:8.2f} | "
              f"len {result['episode_len_mean']:8.2f}")

        # sample trajectory
        if (n + 1) % 10 == 0:
            env = ModifiedDungeon(20, 20, 3, min_room_xy=5, max_room_xy=10, vision_radius=5)
            obs = env.reset()
            Image.fromarray(env._map.render(env._agent)).convert('RGB').resize((500, 500), Image.NEAREST).save(
                'tmp.png')

            frames = []

            for _ in range(500):
                action = ppo_agent.compute_single_action(obs)

                frame = Image.fromarray(env._map.render(env._agent)).convert('RGB'). \
                    resize((500, 500), Image.NEAREST).quantize()
                frames.append(frame)

                obs, reward, done, info = env.step(action)
                if done:
                    break

            frames[0].save(f"out.gif", save_all=True, append_images=frames[1:], loop=0, duration=1000 / 60)
            wandb.log({"trajectory": wandb.Video(f"out.gif", fps=5, format="gif")})


if __name__ == '__main__':
    torch.manual_seed(12345)
    np.random.seed(12345)
    args = ppo_run_parser()
    train_ppo(max_iters=args.max_iters, reward_type=args.reward_type)
