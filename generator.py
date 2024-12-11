import json
from pathlib import Path

import deepmd
import dpgen
import dpgen2
import dpdispatcher
from deepmd.utils.argcheck import (
    gen_args as deepmd_arginfo,
    gen_args_multi_task as deepmd_multi_task_arginfo,
)
from dpgen.generator.arginfo import run_jdata_arginfo, run_mdata_arginfo
from dpgen.simplify.arginfo import simplify_jdata_arginfo, simplify_mdata_arginfo
from dpgen.data.arginfo import (
    init_bulk_jdata_arginfo,
    init_bulk_mdata_arginfo,
    init_surf_jdata_arginfo,
    init_surf_mdata_arginfo,
    init_reaction_jdata_arginfo,
    init_reaction_mdata_arginfo,
)
from dpdispatcher import Resources, Task, Machine
from dpgen2.entrypoint.args import submit_args
from dargs import ArgumentEncoder, Argument

args_path = Path(__file__).parent / "args"
args_path.mkdir(exist_ok=True)

args = {}

def jsdelivr_url(repo, version, file):
    return "https://fastly.jsdelivr.net/gh/{}@{}/{}".format(repo, version, file)


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
    "deepmd-kit-2.0",
    "DeePMD-kit",
    deepmd_arginfo(),
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
add_parameter(
    "deepmd-kit-multi-task",
    "DeePMD-kit",
    deepmd_multi_task_arginfo(),
    deepmd.__version__,
    "deepmodeling/deepmd-kit",
)

# dpgen
add_parameter(
    "dpgen-run",
    "DP-GEN Run",
    run_jdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-machine",
    "DP-GEN Run Machine",
    run_mdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-simplify",
    "DP-GEN Simplify",
    simplify_jdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-simplify-machine",
    "DP-GEN Simplify Machine",
    simplify_mdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-init-bulk",
    "DP-GEN init_bulk",
    init_bulk_jdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-init-bulk-machine",
    "DP-GEN init_bulk Machine",
    init_bulk_mdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-init-surf",
    "DP-GEN init_surf",
    init_surf_jdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-init-surf-machine",
    "DP-GEN init_surf",
    init_surf_mdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-init-reaction",
    "DP-GEN init_reaction",
    init_reaction_jdata_arginfo(),
    dpgen.__version__,
    "deepmodeling/dpgen",
)
add_parameter(
    "dpgen-init-reaction-machine",
    "DP-GEN init_reaction Machine",
    init_reaction_mdata_arginfo(),
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

# DPGEN2
add_parameter(
    "dpgen2-submit",
    "DP-GEN2 Submit",
    submit_args(),
    dpgen2.__version__,
    "deepmodeling/dpgen2",
)

# args.json
with open(args_path / "args.json", 'w') as f:
    json.dump(args, f)

# list generated files
print(*args_path.iterdir())
