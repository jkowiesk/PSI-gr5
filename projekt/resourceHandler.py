import os

class ResourceHandler:
    def __init__(self, local_folder: str) -> None:
        self.local_folder = local_folder
        self.files = {}
        self.scan_local_folder()

    def scan_local_folder(self):
        try:
            for file_name in os.listdir(self.local_folder):
                if self.check_resource(file_name):
                    file_path = os.path.join(self.local_folder, file_name)
                    self.files[file_name] = {"path": file_path}
        except Exception:
            raise ValueError("Unable to scan local folder")


    def check_resource(self, resource_name: str) -> bool:
        try:
            with open(os.path.join(self.local_folder, resource_name), 'rb') as resource_file:
                return True
        except:
            return False

    def process_resource(self, resource_name: str, chunk_size: int = 1024) -> tuple[bytes, int]:
        if not self.check_resource(resource_name):
            return None, None

        processed_file = []
        packets_amount = 0
        with open(os.path.join(self.local_folder, resource_name), 'rb') as resource_file:
            chunk = resource_file.read(chunk_size)
            while chunk:
                processed_file.append(chunk)
                chunk = resource_file.read(chunk_size)
                packets_amount += 1

        return processed_file, packets_amount

    def unprocess_resource(self, processed_resource: bytes, file_name: str) -> None:
        try:
            with open(file_name, 'w') as file_handler:
                decoded_file = processed_resource.decode("utf-8")
                file_handler.write(decoded_file)
        except Exception:
            raise ValueError("File cannot be saved or unprocessed")


if __name__ == "__main__":
    resource_handler = ResourceHandler("./psi_projekt_download")
    print(resource_handler.files)
