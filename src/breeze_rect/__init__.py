
from tqdm import tqdm

import os
import glob
import subprocess
from breeze.utils.build_utils import can_compile
from breeze.errors import UnknownOutputType
from breeze.logger import *

from breeze.helpers import assert_dict

def find_default_compiler():
    # TODO: https://cmake.org/pipermail/cmake/2013-March/053819.html
    return "rgoc"

def create_rect_folder(build_config):
    def create_dir(dir: str):
        if not os.path.exists(dir):
            os.mkdir(dir)

    rect_folder = os.path.join(build_config["breeze_folder"], ".rect")
    create_dir(rect_folder)

    rect_folder = os.path.join(rect_folder, build_config["project_name"])
    create_dir(rect_folder)

    create_dir(os.path.join(rect_folder, "cache"))
    create_dir(os.path.join(rect_folder, "config"))
    create_dir(os.path.join(rect_folder, "files"))

def link_objects(config):

    command = []

    command.append(config["compiler"])
    command += config["flags"]
    command.append("-o")
    command.append(config['output'])
    command += config["source_files"]

    subprocess.run(command, check=True)
    logger.info(f"Compiled rect source code ({config['output']})")

def emit_library(config):

    command = []

    command.append(config["compiler"])
    command += config["flags"]
    command.append("-o")
    command.append(config['output'])
    command += config["source_files"]

    subprocess.run(command, check=True)
    logger.info(f"Compiled rect source code ({config['output']})")

def breeze_build(config):

    build_config = {
        "compiler": "",
        "flags": "",
        "project_name": "",
        "output": "",
        "output_type": "",
        "source_files": [],
        "compiled_objects": [],
        "breeze_folder": config[".folder"]
    }

    logger.verbose("Fetching necesary information")

    assert_dict(config, "config")
    assert_dict(config["config"], "rect-lang")

    rect_lang_config = config["config"]["rect-lang"]

    assert_dict(rect_lang_config, "sources", "config.rect-lang.sources")
    assert_dict(rect_lang_config, "type", "config.rect-lang.type")

    compiler = rect_lang_config.get("compiler", None)
    if compiler is None:
        compiler = find_default_compiler()

    output_type = rect_lang_config["type"]

    create_rect_folder(build_config)

    build_config["compiler"] = compiler
    build_config["output_type"] = output_type
    build_config["project_name"] = config["project"]["name"]

    build_config["flags"] = rect_lang_config.get("flags", "")

    logger.verbose("Retrieving source files")

    if isinstance(rect_lang_config["sources"], str):
        build_config["source_files"] += glob.glob(rect_lang_config["sources"], recursive=True)
    elif isinstance(rect_lang_config["sources"], list):
        for source in rect_lang_config["sources"]:
            build_config["source_files"] += glob.glob(source, recursive=True)
    else:
        pass # TODO: error?

    if len(build_config["source_files"]) == 0:
        logger.info("Skiping build because no sources found!")
        exit(0)

    logger.verbose("Rect sources: %s" % str(build_config["source_files"]))
    logger.verbose("Rect flags: %s" % build_config["flags"])
    if output_type == "exec":
        logger.verbose("Compiling executable...")
        build_config["output"] = rect_lang_config.get("output", "a.out")

        raise UnknownOutputType(f"Executables not yet supported!")
        link_objects(build_config)
    elif output_type == "lib":
        logger.verbose("Compiling library...")
        build_config["output"] = rect_lang_config.get("output", "a.so")
        emit_library(build_config)
    else:
        raise UnknownOutputType(f"Output type '{output_type}' is not supported")
