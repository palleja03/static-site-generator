import os
import shutil

def copy_files_recursive(src, dst):
    if src == dst:
        return
    if not os.path.exists(dst):
        os.mkdir(dst)
    for node in os.listdir(src):
        node_path = os.path.join(src, node)
        node_dst = os.path.join(dst, node)
        print(f" * {node_path} -> {node_dst}")
        if os.path.isfile(node_path):
            shutil.copy(node_path, node_dst)
        elif os.path.isdir(node_path):
            copy_files_recursive(node_path, node_dst)
        else:
            print(f"Cannot copy '{node_path}'. It's not a file nor directory")