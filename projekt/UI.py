"""
- zapytanie wszystkich węzłów czy posiadają zasób
- odpowiadanie na zapytanie o posiadany zasób
- możliwość wprowadzania zasobu przez użytkownika
- pobieranie konkretnych nazwanych zasobów ze zdalnego węzła (jednego na raz)
- rozgłaszanie informacji o posiadanych lokalnie zasobach
- usuwanie lokalnego zasobu
- interfejs tekstowy obsługujący współbieżność transferu zasobów
- dodanie nowego węzła do sieci
"""
from P2PNode import P2PNode

class UI:
    def __init__(self):
        self.node = P2PNode()

    def display_local_resources(self):
        """Displays the resources that are currently stored locally"""
        pass

    def add_new_resource(self):
        """Prompts the user to add a new resource from their local file system"""
        pass

    def download_resource(self, filename: str):
        """Prompts the user to enter the name of a resource to download from a remote node"""
        self.node.get_file(filename)
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
                filename = input("Write filename: ")
                self.download_resource(filename)
            elif user_input == "4":
                self.broadcast_local_resources()
            elif user_input == "q":
                break
            else:
                print("Invalid input, please try again.")

if __name__ == "__main__":
    ui = UI()
    ui.run()