from os import path, listdir
from importlib.util import spec_from_file_location, module_from_spec


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


def help():
    print("The Cyckei Plugin Suite aids in device plugin development.")
    print("\toverwrite [plugin]       \t Loads a plugin with default configuration.")
    print("\tload  [plugin]           \t Loads a plugin with existing configuration.")
    print("\tread  [plugin] [address] \t Reads value from loaded device.")
    print("\tlist                     \t Lisrs available plugins.")
    print("\thelp                     \t Displays this help dialog.")
    print("\texit                     \t Closes application.")


def load_plugin(path, overwrite=False):
    if path.isfile(path):
        spec = spec_from_file_location(f"plugin.{path}", path)
        plugin_module = module_from_spec(spec)
        spec.loader.exec_module(plugin_module)

    # Rewrite individual configuration and load sources into config for client
        config_file = f"{plugin_module.DEFAULT_CONFIG['name']}.json"
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


def command_loop(plugins):
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
                    print(f"Loading {path}, overwrite.")
            elif command[0] == "load":
                path = get_path(command[1], plugins)
                if path:
                    print(f"Loading {path}.")
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
