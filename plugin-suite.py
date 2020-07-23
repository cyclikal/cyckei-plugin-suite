from os import path, listdir


def main():
    print("Welcome to the Cyckei Plugin Suite!")
    print("Place plugins in the 'plugins' folder of the root directory.")
    list_plugins()


def list_plugins():
    plugin_path = path.join(path.dirname(path.abspath(__file__)), "plugins")
    print(f"Checking available plugins from {plugin_path}...")
    plugins = [[], []]
    for file in listdir(plugin_path):
        if path.isfile(path.join(plugin_path, file)):
            plugins[0].append(path.join(plugin_path, file))
            plugins[1].append(file.split('.')[0])
    print(f"Found these plugins: {plugins[1]}")


if __name__ == "__main__":
    main()
