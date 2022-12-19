from argparse import ArgumentParser
import subprocess

import toml


def config_to_sbatch_flags(config_toml):
    config_dict = toml.load(config_toml)
    sbatch_flags = " ".join([f"{key} {val}" for key, val in config_dict["sbatch"].items()])
    return sbatch_flags


def config_to_launch_cmd(config_toml):
    config_dict = toml.load(config_toml)
    return config_dict["launch_cmd"]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("config_path")
    args = parser.parse_args()
    sbatch_flags = config_to_sbatch_flags(args.config_path)
    launch_cmd = config_to_launch_cmd(args.config_path)
    cmd = f"sbatch {sbatch_flags} --wrap \"{launch_cmd}\""
    subprocess.run(cmd, shell=True)
