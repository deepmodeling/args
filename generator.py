import json
from pathlib import Path

import deepmd
import dpgen
import dpdispatcher
from deepmd.utils.argcheck import model_args, learning_rate_args, loss_args, training_args
from dpgen.generator.arginfo import run_mdata_arginfo
from dpdispatcher import Resources, Task, Machine
from dargs import ArgumentEncoder, Argument

args_path = Path(__file__).parent / "args"
args_path.mkdir(exist_ok=True)

args = {}

def jsdelivr_url(repo, version, file):
    return "https://cdn.jsdelivr.net/gh/{}@{}/{}".format(repo, version, file)


def add_parameter(key : str, name: str, argument: Argument, version: str,
                  repo: str, examples: list = None) -> dict:
    fn = key + ".json"
    with open(args_path / fn, 'w') as f:
        json.dump(argument, f, cls=ArgumentEncoder)
    arg = {}
    arg["name"] = "{} v{}".format(name, version)
    arg["fn"] = fn
    if examples is not None:
        arg_examples = []
        for example in examples:
            arg_examples.append(
                {
                    "name": example["name"],
                    "url": jsdelivr_url(repo, version, example["file"])
                }
            )
        arg['examples']= arg_examples
    args[key] = arg


# deepmd-kit
add_parameter(
    "deepmd-kit",
    "DeePMD-kit",
    (
        model_args(),
        learning_rate_args(),
        loss_args(),
        training_args(),
    ),
    deepmd.__version__,
    "deepmodeling/deepmd-kit",
    [
        {
            "name": "Water se_e2_a",
            "file": "examples/water/se_e2_a/input.json"
        },
        {
            "name": "Water se_e2_r",
            "file": "examples/water/se_e2_r/input.json"
        },
        {
            "name": "Water se_e2_a_tebd",
            "file": "examples/water/se_e2_a_tebd/input.json"
        },
        {
            "name": "Water se_e3",
            "file": "examples/water/se_e3/input.json"
        },
        {
            "name": "Water hybrid",
            "file": "examples/water/hybrid/input.json"
        },
        {
            "name": "Water tensor polar",
            "file": "examples/water_tensor/polar/polar_input.json"
        },
        {
            "name": "Water tensor dipole",
            "file": "examples/water_tensor/dipole/dipole_input.json"
        },
        {
            "name": "Frame parameter",
            "file": "examples/fparam/train/input.json"
        },
        {
            "name": "Atomic parameter",
            "file": "examples/fparam/train/input_aparam.json"
        }
    ],
)

# dpgen
add_parameter(
    "dpgen",
    "DP-GEN Machine",
    run_mdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)

# dpdispatcher
add_parameter(
    "dpdispatcher-machine",
    "DPDispatcher Machine",
    Machine.arginfo(),
    dpdispatcher.__version__,
    "deepmodeling/dpdispatcher",
)

add_parameter(
    "dpdispatcher-resources",
    "DPDispatcher Resources",
    Resources.arginfo(),
    dpdispatcher.__version__,
    "deepmodeling/dpdispatcher",
)

add_parameter(
    "dpdispatcher-task",
    "DPDispatcher Task",
    Task.arginfo(),
    dpdispatcher.__version__,
    "deepmodeling/dpdispatcher",
)

# args.json
with open(args_path / "args.json", 'w') as f:
    json.dump(args, f)

# list generated files
print(*args_path.iterdir())
