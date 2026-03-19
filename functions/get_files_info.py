import os
def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    if os.path.commonpath([working_dir_abs,target_dir]) != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    items = os.listdir(target_dir)
    items.sort()
    outputlines = []
    for item in items:
        item_path = os.path.join(target_dir,item)
        file_size = os.path.isdir(item_path)

        line = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
        output_lines.append(line)
    return "\n".join(output_lines)        
except Exception as e:
    return f"Error: {e}"