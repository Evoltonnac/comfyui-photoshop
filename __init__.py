import importlib
import os
import folder_paths
import sys

# Define the path to the 'py' directory
py = os.path.join(
    folder_paths.get_folder_paths("custom_nodes")[0], "comfyui-photoshop", "py"
)

# List of modules
node_list = ["nodePlugin", "nodeRemoteConnection"]
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Import each module from the 'py' directory
for module_name in node_list:
    spec = importlib.util.spec_from_file_location(
        module_name, os.path.join(py, f"{module_name}.py")
    )
    imported_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imported_module)
    NODE_CLASS_MAPPINGS.update(imported_module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(imported_module.NODE_DISPLAY_NAME_MAPPINGS)

# Import 'Backend' module
try:
    # 创建包的命名空间
    package_name = "comfyui_photoshop"
    
    # 确保父包存在
    if package_name not in sys.modules:
        sys.modules[package_name] = type(sys)(package_name)
    
    # 导入 Backend 模块
    backend_spec = importlib.util.spec_from_file_location(
        f"{package_name}.Backend", 
        os.path.join(py, "Backend.py")
    )
    backend_module = importlib.util.module_from_spec(backend_spec)
    sys.modules[f"{package_name}.Backend"] = backend_module
    
    # 同样导入 decrypt 模块
    decrypt_spec = importlib.util.spec_from_file_location(
        f"{package_name}.decrypt", 
        os.path.join(py, "decrypt.py")
    )
    decrypt_module = importlib.util.module_from_spec(decrypt_spec)
    sys.modules[f"{package_name}.decrypt"] = decrypt_module
    
    # 先执行 decrypt 模块
    decrypt_spec.loader.exec_module(decrypt_module)
    # 再执行 Backend 模块
    backend_spec.loader.exec_module(backend_module)
    
except Exception as e:
    print(f"Backend import error: {str(e)}")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
WEB_DIRECTORY = "js"
