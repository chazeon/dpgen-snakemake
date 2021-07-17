from utils.taskset import iter_value_set
from copy import deepcopy
import yaml, sys, json

def build_taskset(params: dict):
    for _conf in params["confs"].items():
        for _vars in iter_value_set(params["vars"]):
            _params = deepcopy(params["fixes"])
            _params.update(_vars)
            yield _conf, _params

# def get_task_name(params: dict):
#     if params["fix"] == "nvt":
#         return "T{temp}".format_map(params)
#     elif params["fix"] == "npt":
#         return "P{pres}.T{temp}".format_map(params)
#     else:
#         raise RuntimeError()


import click

@click.command()
@click.argument("fin")
def main(fin):
    with open(fin) as fp:
        tparams = yaml.safe_load(fp)

    tasks = {}

    for key, params in tparams.items():
        for conf, param in build_taskset(params):
            # name = get_task_name(param)
            task = {
                "conf_name": conf[0],
                "conf": conf[1],
                "param": param,
            }
            path = params["path"].format_map(task)
            task["path"] = path
            tasks[path] = task
            # print(task)

    sys.stdout.write(json.dumps(tasks, indent=2) + "\n")

if __name__ == "__main__":
    main()