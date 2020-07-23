from os import path, listdir
from importlib.util import spec_from_file_location, module_from_spec


def main():
    print("Welcome to the Cyckei Plugin Suite!")
    print("Place plugins in the 'plugins' folder of the root directory.")
    plugins, folder = parse_plugins()
    return command_loop(plugins, folder)


def parse_plugins():
    folder = path.join(path.dirname(path.abspath(__file__)), "plugins")
    print(f"Checking available plugins from {folder}...")

    plugins = [[], []]
    for file in listdir(folder):
        if path.isfile(path.join(folder, file)):
            plugins[0].append(path.join(folder, file))
            plugins[1].append(file.split('.')[0])
    print(f"Found these plugins: {plugins[1]}")

    return plugins, folder


def help():
    print("The Cyckei Plugin Suite aids in device plugin development.")
    print("\toverwrite [plugin]       \t Loads plugin with default config.")
    print("\tload  [plugin]           \t Loads plugin with existing config.")
    print("\tread  [plugin] [address] \t Reads value from loaded device.")
    print("\tlist                     \t Lisrs available plugins.")
    print("\thelp                     \t Displays this help dialog.")
    print("\texit                     \t Closes application.")


def load(path, name, folder, overwrite=False):
    if overwrite:
        print(f"Loading {name} plugin with new configuration.")
    else:
        print(f"Loading {name} plugin.")

    if path.isfile(path):
        spec = spec_from_file_location(f"plugin.{path}", path)
        plugin_module = module_from_spec(spec)
        spec.loader.exec_module(plugin_module)

    # Rewrite individual configuration and load sources into config for client
    config_file = path.join(folder,
                            f"{plugin_module.DEFAULT_CONFIG['name']}.json")
    if not exists(config_file) or overwrite:
        with open(config_file, "w") as file:
            json.dump(plugin.DEFAULT_CONFIG, file)

    with open(config_file) as file:
        plugin_config = json.load(file)
    config["plugin_sources"].append({
        "name": plugin_config["name"],
        "description": plugin_config["description"],
        "sources": []
    })
    for source in plugin_config["sources"]:
        config["plugin_sources"][-1]["sources"].append(source["readable"])

    # Cycle each plugin module up into its own object
    if launch == "server":
        for i, module in enumerate(plugins):
            plugins[i] = module.DataController(path)

    return config, plugins


def get_path(name, plugins):
    try:
        index = plugins[1].index(name)
        return plugins[0][index]
    except ValueError:
        print(f"Plugin {name} not found.")
        return None


def command_loop(plugins, folder):
    while True:
        command = input("?> ").split()

        if len(command) == 3:
            if command[0] == "read":
                if command[1] in plugins[1]:
                    print("read")
                else:
                    print(f"Plugin {command[1]} not loaded.")
            else:
                help()
        elif len(command) == 2:
            if command[0] == "overwrite":
                path = get_path(command[1], plugins)
                if path:
                    load(path, command[1], folder, True)
            elif command[0] == "load":
                path = get_path(command[1], plugins)
                if path:
                    load(path, command[1], folder)
            else:
                help()
        elif len(command) == 1:
            if command[0] == "list":
                print(f"Found these plugins: {plugins[1]}")
            elif command[0] == "exit":
                return 0
            else:
                help()
        else:
            help()


if __name__ == "__main__":
    main()
