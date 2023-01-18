class ResourceHandler:
    def __init__(self, local_folder: str) -> None:
        self.local_folder = local_folder

    def check_resource(self, resource_name: str) -> bool:
        try:
            with open(resource_name, 'rb') as resource_file:
                return True
        except:
            return False

    def process_resource(self, resource_name: str, chunk_size: int =1024) -> tuple[bytes, int]:
        if not self.check_resource(resource_name):
            return None, None

        processed_file = b''
        packets_amount = 0
        with open(resource_name, 'rb') as resource_file:
            chunk = resource_file.read(chunk_size)
            while chunk:
                processed_file += chunk
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
    resource_name = './projekt/example.json'
    resource_handler = ResourceHandler(local_folder="")
    processed_resource, packets_amount = resource_handler.process_resource(resource_name=resource_name, chunk_size=2)
    print(packets_amount)
    resource_handler.unprocess_resource(processed_resource=processed_resource, file_name="./projekt/super_duper_exmaple.json")
