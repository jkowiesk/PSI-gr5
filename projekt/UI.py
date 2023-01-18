class UI:
    def __init__(self):
        pass

    def display_local_resources(self):
        """Displays the resources that are currently stored locally"""
        pass

    def add_new_resource(self):
        """Prompts the user to add a new resource from their local file system"""
        pass

    def download_resource(self):
        """Prompts the user to enter the name of a resource to download from a remote node"""
        pass

    def broadcast_local_resources(self):
        """Sends information about locally stored resources to other nodes in the network"""
        pass

    def handle_network_errors(self):
        """Handles any network errors that occur during resource transfer"""
        pass

    def greet_user(self):
        message = "Welcome to P2P network UI"
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
            "3": "Download resource",
            "4": "Broadcast local resources",
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
                self.download_resource()
            elif user_input == "4":
                self.broadcast_local_resources()
            elif user_input == "q":
                break
            else:
                print("Invalid input, please try again.")

if __name__ == "__main__":
    ui = UI()
    ui.run()