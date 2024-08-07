import os
import random
import warnings

import gym
import ma_gym  # noqa 401
import numpy as np
import torch
import wandb
from common.arguments import common_args, config_args
from dotenv import load_dotenv
from runner import Runner

warnings.filterwarnings("ignore", category=UserWarning)

N_EXPERIMENTS = 1


if __name__ == "__main__":
    load_dotenv()
    args = common_args()

    seed = random.randrange(0, 2**32 - 1)
    print("Using seed: ", seed)
    torch.random.manual_seed(seed)
    np.random.seed(seed)

    if args.env == "PredatorPrey":
        # avoid registering a new environment in the ma_gym package and instead change grid size here manually
        env = gym.make(
            "PredatorPrey7x7-v0",
            grid_shape=(7, 7),
            n_agents=4,
            n_preys=2,
            penalty=-0.75,
        )
        args.n_actions = env.action_space[0].n
        args.n_agents = env.n_agents
        args.state_shape = 28 * args.n_agents
        args.obs_shape = 28
        args.episode_limit = env._max_steps
        print("PP with penalty ", env._penalty)
    else:
        raise Exception("Invalid environment: environment not supported!")

    print(
        "Environment {} initialized, for {} time steps and evaluating every {} time steps".format(
            args.env, args.n_steps, args.evaluate_cycle
        )
    )

    # load args
    # this code is prepared for no parameter sharing methods; supporting only indepdnednt learning without sharing params and with and without communication
    if args.alg == "idql":
        args = config_args(args)
    else:
        raise Exception("No such algorithm!")

    print("CUDA set to", args.cuda)
    print("Communication set to", args.with_comm)
    print("With args:\n", args)

    wandb.login(key=os.getenv("WANDB_API_KEY"))
    wandb.init(
        project="independent-comm",
        config=args,
    )

    runner = Runner(env, args)

    # parameterize run according to the number of independent experiments to run, i.e., independent sets of n_epochs over the model; default is 1
    if args.learn:
        runner.run(N_EXPERIMENTS)
