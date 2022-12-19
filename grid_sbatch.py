from argparse import ArgumentParser
import itertools
import subprocess

import toml

from sbatch import config_to_sbatch_flags, config_to_launch_cmd


def search_to_flags(search_toml):
    search_dict = toml.load(search_toml)
    flag_strs = []
    print(search_dict)
    for vals in itertools.product(*search_dict.values()):
        flag_strs.append(" ".join([f"{key} {val}" for key, val in zip(search_dict.keys(), vals)]))
    return flag_strs


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("config_path")
    parser.add_argument("search_path")
    args = parser.parse_args()
    sbatch_flags = config_to_sbatch_flags(args.config_path)
    launch_cmd = config_to_launch_cmd(args.config_path)
    flag_strs = search_to_flags(args.search_path)
    for flag_str in flag_strs:
        cmd = f"sbatch {sbatch_flags} --wrap \"{launch_cmd} {flag_str}\""
        subprocess.run(f"{cmd} {flag_str}", shell=True)
