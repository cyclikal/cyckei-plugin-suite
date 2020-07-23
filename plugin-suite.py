import json

from os import path, listdir
from importlib.util import spec_from_file_location, module_from_spec


def main():
    print("Welcome to the Cyckei Plugin Suite!")
    plugins, folder = parse_plugins()
    return command_loop(plugins, folder)


def parse_plugins():
    base_path = path.dirname(path.abspath(__file__))
    plugin_path = path.join(base_path, "plugins")
    print(f"Checking available plugins from {plugin_path}...")

    plugins = [[], []]
    for file in listdir(plugin_path):
        full_path = path.join(plugin_path, file)
        if path.isfile(full_path) and full_path.endswith(".py"):
            plugins[0].append(path.join(plugin_path, file))
            plugins[1].append(file.split('.')[0])

    return plugins, base_path


def help():
    print("The Cyckei Plugin Suite aids in device plugin development.")
    print("Place plugins in the 'plugins' folder of the root directory.")
    print("\toverwrite [plugin]       \t Loads plugin with default config.")
    print("\tload  [plugin]           \t Loads plugin with existing config.")
    print("\tread  [plugin] [address] \t Reads value from loaded device.")
    print("\tlist                     \t Lisrs available plugins.")
    print("\thelp                     \t Displays this help dialog.")
    print("\texit                     \t Closes application.")


def load(plugin_path, name, folder, overwrite=False):
    if overwrite:
        print(f"Loading {name} plugin with new configuration...", end="")
    else:
        print(f"Loading {name} plugin...", end="")

    if path.isfile(plugin_path):
        spec = spec_from_file_location(f"plugin.{plugin_path}", plugin_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

    # Rewrite individual configuration and load sources into config for client
    config_file = path.join(folder, "plugins",
                            f"{module.DEFAULT_CONFIG['name']}.json")
    if not path.exists(config_file) or overwrite:
        with open(config_file, "w") as file:
            json.dump(module.DEFAULT_CONFIG, file)

    # Cycle each plugin module up into its own object
    plugin = module.DataController(folder)

    print("Done!")
    return plugin


def get_path(name, plugins):
    try:
        index = plugins[1].index(name)
        return plugins[0][index]
    except ValueError:
        print(f"Plugin {name} not found.")
        return None


def command_loop(p_available, folder):
    p_loaded = []

    while True:
        command = input("?> ").split()

        if len(command) == 3:
            if command[0] == "read":
                for plugin in p_loaded:
                    if plugin.name == command[1]:
                        print(f"Reading {plugin.name} on port {command[2]}.")
                        value = plugin.read(command[2])
                        print(f"Current value: {value}.")
                        break
                else:
                    print(f"Plugin {command[1]} not loaded.")
            else:
                help()
        elif len(command) == 2:
            if command[0] == "overwrite":
                plugin_path = get_path(command[1], p_available)
                if plugin_path:
                    p_loaded.append(load(plugin_path, command[1], folder,
                                         True))
            elif command[0] == "load":
                plugin_path = get_path(command[1], p_available)
                if plugin_path:
                    p_loaded.append(load(plugin_path, command[1], folder))
            else:
                help()
        elif len(command) == 1:
            if command[0] == "list":
                print(f"Available plugins: {p_available[1]}")
                print(f"Loaded plugins:", end="")
                for plugin in p_loaded:
                    print(f" {plugin.name},", end="")
                print("")

            elif command[0] == "exit":
                return 0
            else:
                help()
        else:
            help()


if __name__ == "__main__":
    main()
