import os
import subprocess


def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                 cwd=working_dir_abs, timeout=30)

        output_string = ""

        if process.returncode != 0:
            output_string += f"Process exited with code {process.returncode}\n"

        if not (process.stdout or process.stderr):
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {process.stdout.strip()}\n"
            output_string += f"STDERR: {process.stderr.strip()}"

        return output_string


    except Exception as e:
        return f"Error: {e}"
