import os
import ast
from glob import glob
import hashlib
import shutil


SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
REMOVABLE_MEDIA_LOCATION = f"/media/{os.getenv('USER')}/"
DRIVE_IDENTIFIED_STRING = "VEX"
VEX_BUILTIN_MODULES = ["micropython", "uasyncio.event", "urandom", "_thread", "motorgroup", "uasyncio.funcs", "ure",
                       "_uasyncio", "python_vm_init", "uasyncio.lock", "uselect", "builtins", "smartdrive",
                       "uasyncio.stream", "ustruct", "cmath", "sys", "ubinascii", "utime", "drivetrain", "uarray",
                       "ucollections", "utimeq", "gc", "uasyncio", "uio", "vex", "math", "uasyncio.core", "ujson",
                       "vexdev"]

MAIN_PROGRAM = os.path.join(SRC_DIR, "main.py")
OTHER_DEPENDENCIES = os.path.join(SRC_DIR, "resources")


def get_vex_disk():
    mount_points = os.listdir(REMOVABLE_MEDIA_LOCATION)
    for mount_point in mount_points:
        drive_name = os.path.basename(mount_point)
        drive_path = os.path.join(REMOVABLE_MEDIA_LOCATION, drive_name)
        if DRIVE_IDENTIFIED_STRING in drive_name:
            return drive_path
    raise FileNotFoundError("Could not find sd card mountpoint")


def get_available_modules(library_directory):
    available_modules = {}
    for file in glob(os.path.join(library_directory, "*.py")):
        available_modules[(file.split('/')[-1].split('.')[0])] = file
    return available_modules


def detect_dependencies(file_path, visited=None):
    if visited is None:
        visited = set()

    with open(file_path, 'r') as file:
        content = file.read()

    tree = ast.parse(content)
    imported_modules = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name not in visited and name.name not in VEX_BUILTIN_MODULES:
                    visited.add(name.name)
                    imported_modules.append(name.name)
                    imported_modules.extend(detect_dependencies(os.path.join(SRC_DIR, name.name + ".py"), visited))
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            if module_name not in visited and module_name not in VEX_BUILTIN_MODULES:
                visited.add(module_name)
                imported_modules.append(module_name)
                imported_modules.extend(detect_dependencies(os.path.join(SRC_DIR, module_name + ".py"), visited))

    return imported_modules


def get_checksum(file_path):
    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()


def copy_libraries(libraries, directory):
    for file in libraries:
        file_to_copy_checksum = get_checksum(file)
        file_to_overwrite = os.path.join(directory, (file.split('/')[-1]))
        file_to_overwrite_checksum = None
        if os.path.isfile(file_to_overwrite):
            file_to_overwrite_checksum = get_checksum(file_to_overwrite)
            print(f"{file_to_overwrite} exists with checksum: {file_to_overwrite_checksum}")
        elif os.path.isdir(file_to_overwrite):
            print(f"{file_to_overwrite} exists as folder, removing it")
            os.rmdir(file_to_overwrite)
        if file_to_copy_checksum != file_to_overwrite_checksum:
            if file_to_overwrite_checksum:
                print(f"{file_to_overwrite} exists but has invalid checksum: {file_to_overwrite_checksum}")
                os.remove(file_to_overwrite)
            else:
                print(f"{file_to_overwrite} does not exist")
            shutil.copy(file, directory)
        else:
            print(f"{file_to_overwrite} checksum matches original")


def main():
    vex_disk = get_vex_disk()
    available_libraries = get_available_modules(SRC_DIR)
    required_libraries = [module for module in detect_dependencies(MAIN_PROGRAM) if module not in VEX_BUILTIN_MODULES]

    print(required_libraries)

    libraries_to_copy = {}

    for library in required_libraries:
        if library in available_libraries:
            print(f"Found library {library} at {available_libraries[library]}")
            libraries_to_copy[library] = available_libraries[library]
        else:
            raise ModuleNotFoundError(f"Couldn't find library \"{library}\"")

    other_dependencies = []

    for dependency in glob(OTHER_DEPENDENCIES + "/**", recursive=True):
        print(dependency)
        if os.path.isfile(dependency):
            other_dependencies.append(os.path.join(OTHER_DEPENDENCIES, dependency))

    copy_libraries(list((*libraries_to_copy.values(), *other_dependencies)), vex_disk)
    if not os.path.isdir(os.path.join(vex_disk, "Logs")):
        os.mkdir(os.path.join(vex_disk, "Logs"))

    os.system(f"umount {vex_disk}")


if __name__ == "__main__":
    main()
