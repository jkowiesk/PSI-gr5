import os
import shutil
from pathlib import Path

class ResourceHandler:
    def __init__(self, local_folder: str) -> None:
        self.local_folder = local_folder
        self.scan_local_folder()

    def scan_local_folder(self):
        try:
            files = {}
            for file_name in os.listdir(self.local_folder):
                if self.check_resource(file_name):
                    file_path = os.path.join(self.local_folder, file_name)
                    files[file_name] = {"path": file_path}
            return files
        except Exception:
            raise ValueError("Unable to scan local folder")

    def copy_file_to_local_folder(self, file_path: str) -> None:
        file_name = Path(file_path).name
        try:
            shutil.copy(file_path, os.path.join(self.local_folder, file_name))
        except Exception:
            raise ValueError(f"Unable to copy file from this path: {file_path} to local folder")


    def check_resource(self, resource_name: str) -> bool:
        try:
            with open(os.path.join(self.local_folder, resource_name), 'rb') as resource_file:
                return True
        except:
            return False

    def divide_into_batches(self, lst, batch_size: int):
        for i in range(0, len(lst), batch_size):
            yield lst[i:i+batch_size]

    def process_resource(self, resource_name: str, chunk_size: int = 1024) -> bytes:
        if not self.check_resource(resource_name):
            return None

        processed_file = b''
        with open(os.path.join(self.local_folder, resource_name), 'rb') as resource_file:
            chunk = resource_file.read(chunk_size)
            while chunk:
                processed_file += chunk
                chunk = resource_file.read(chunk_size)

        return processed_file

    def unprocess_resource(self, processed_resource: bytes, file_name: str) -> None:
        try:
            with open(file_name, 'w') as file_handler:
                decoded_file = processed_resource.decode("utf-8")
                file_handler.write(decoded_file)
        except Exception:
            raise ValueError("File cannot be saved or unprocessed")


if __name__ == "__main__":
    local_folder_path = os.path.join(os.getcwd(), 'projekt/psi_projekt_download')
    resource_handler = ResourceHandler(local_folder=local_folder_path)

    resource_name = "projekt/mark2"
    resource_handler.copy_file_to_local_folder(file_path=resource_name)
    local_files = resource_handler.scan_local_folder()
    print(local_files)

    assert resource_handler.check_resource(resource_name="mark2")

    processed_file = resource_handler.process_resource(resource_name="mark2")
    print(processed_file)