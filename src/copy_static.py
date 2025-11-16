import os
import shutil

def static_to_public(path):
    static_path = os.path.join(os.path.abspath(os.getcwd()),"static", path)
    public_path = os.path.join(os.path.abspath(os.getcwd()),"public", path)
    contents = os.listdir(static_path)

    for content in contents:
        content_path = os.path.join(static_path, content)
        if os.path.isfile(content_path):
            shutil.copy(os.path.join(static_path, content), os.path.join(public_path, content))
        else:
            directory_path = os.path.join(public_path, content)
            os.mkdir(directory_path)
            static_to_public(os.path.join(path, content))
            
    
    
