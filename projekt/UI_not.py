from P2PNot import P2PNot
import os
import socket

class UI:
    def __init__(self):
        self.node = P2PNot()

    def display_local_resources(self):
        """Displays the resources that are currently stored locally"""
        resources = self.node.res_handler.scan_local_folder()
        print("RESOURCES")
        for resource_name, resource_obj in resources.items():
            print(f"# Resource name: \"{resource_name}\" \tLocal path to resource: \"{resource_obj.get('path')}\"")

    def display_all_resources(self):
        """Displays all resources"""
        print("KNOWN RESOURCES:")
        for res in self.node.resources:
            print(res)
        print()

    def add_new_resource(self):
        """Prompts the user to add a new resource from their local file system"""
        while True:
            new_resource_path = input("Please provide resource name: ")
            if not os.path.exists(os.path.join(self.node.res_handler.local_folder, new_resource_path)) and os.path.exists(new_resource_path):
                self.node.res_handler.copy_file_to_local_folder(file_path=new_resource_path)
                self.node.resources.update(self.node.res_handler.scan_local_folder().keys())
                print("File successfully copied to local folder!")
                break
            elif not os.path.exists(new_resource_path):
                print(f"File with provided path {new_resource_path} does not exist")
            elif os.path.exists(os.path.join(self.node.res_handler.local_folder, new_resource_path)):
                print(f"File with provided path {new_resource_path} already exists in local folder")


    def download_resource(self, filename: str):
        """Prompts the user to enter the name of a resource to download from a remote node"""
        # raise socket.error            FOR TESTING
        return self.node.get_file(filename)

    def greet_user(self):
        message = "Welcome to P2P NOT UI"
        print("#" * len(message))
        print(message)
        print("#" * len(message))

    def print_options(self):
        print("| Operations |")
        options = self.get_options()
        for option, text in options.items():
            msg = f"{option} - {text}"
            print(msg)

    def get_options(self):
        options = {
            "1": "Display local resources",
            "2": "Add new resource",
            "3": "Delete resource",
            "4": "Download resource",
            "5": "Broadcast local resources",
            "6": "Display all resources",
            "q": "Exit"
        }
        return options


    def run(self):
        """Main method to run the UI and handle user input"""
        self.greet_user()
        while True:
            self.print_options()
            user_input = input("Choose option: ")
            if user_input == "1":
                self.display_local_resources()
            elif user_input == "2":
                self.add_new_resource()
            elif user_input == "3":
                resource_name = input("Please provide resource name to delete: ")
                is_deleted = self.node.res_handler.delete_resource(resource_name=resource_name)
                if is_deleted:
                    print(f"Deleted file {resource_name}")
                else:
                    print(f"No such file in local directory: {resource_name}")
            elif user_input == "4":
                filename = input("Write filename: ")
                print()
                returnCode = self.download_resource(filename)
                
                if returnCode == 0:
                    print("File successfully downloaded!")
                if returnCode == -1:
                    print("Unable to download file")
                if returnCode == 1:
                    print("The resource is no longer in network")
                    self.node.resources.remove(filename)
                print()
            elif user_input == "5":
                self.node.share_files()
            elif user_input == "6":
                self.display_all_resources()
            elif user_input == "q":
                self.node.stop_node()
                break
            else:
                print("Invalid input, please try again.")

if __name__ == "__main__":
    ui = UI()
    ui.run()