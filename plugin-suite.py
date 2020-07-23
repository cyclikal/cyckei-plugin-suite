from os import path, listdir


def main():
    print("Welcome to the Cyckei Plugin Suite!")
    print("Place plugins in the 'plugins' folder of the root directory.")
    plugins = parse_plugins()
    return command_loop(plugins)


def parse_plugins():
    plugin_path = path.join(path.dirname(path.abspath(__file__)), "plugins")
    print(f"Checking available plugins from {plugin_path}...")

    plugins = [[], []]
    for file in listdir(plugin_path):
        if path.isfile(path.join(plugin_path, file)):
            plugins[0].append(path.join(plugin_path, file))
            plugins[1].append(file.split('.')[0])
    print(f"Found these plugins: {plugins[1]}")

    return plugins


def help_dialog(plugins):
    print("The Cyckei Plugin Suite aids in device plugin development.")
    print("\tbuild [plugin]\t Loads a plugin with default configuration.")
    print("\tload  [plugin]\t Loads a plugin with exist configuration.")
    print("\tread  [plugin]\t Reads value from loaded device.")
    print("\tlist          \t Lisrs available plugins.")
    print("\thelp          \t Displays this help dialog.")
    print("\texit          \t Closes application.")


def command_loop(plugins):
    while True:
        command = input("?> ").split()

        try:
            if command[0] == "build":
                if command[1] in plugins:
                    print(f"Creating configuration for {command[1]} plugin...")
                else:
                    print(f"Cannot find plugin {command[1]}")

            elif command[0] == "load":
                if command[1] in plugins:
                    print(f"Loading {command[1]} plugin...")
                else:
                    print(f"Cannot find plugin {command[1]}")

            elif command[0] == "read":
                if command[1] in plugins:
                    print(f"Reading value from {command[1]}...")
                else:
                    print(f"Cannot find plugin {command[1]}")

            elif command[0] == "list":
                print(f"Found these plugins: {plugins[1]}")
            elif command[0] == "exit":
                return 0
            else:
                raise ValueError
        except (IndexError, ValueError):
            help_dialog(plugins)


if __name__ == "__main__":
    main()
