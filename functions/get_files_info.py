import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        contents_as_str = []
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)

            is_dir = os.path.isdir(file_path)
            size = os.path.getsize(file_path)

            contents_as_str.append(f"  - {file}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(contents_as_str)

    except Exception as e:
        return f"Error: {e}"