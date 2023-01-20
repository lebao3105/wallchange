## Wallchange
An automated tool to set your desktop background!

## Running
This project requires Python 3.8+ with pip installed.

Use Poetry:
```bash
$ poetry install
$ poetry run python3 -m wallchange [filepath] # Run
```

Or:
```bash
$ pip install -r requirements.txt
$ python3 -m wallchange
```

> Tip: You can set the app not to show the window (access the app from the system tray):
```bash
$ RUN_SLIENT=True python3 -m wallchange [filepath]
```

(Windows)
```cmd
> set RUN_SLIENT=True & py -m wallchange [filepath]
```

## Usage
Open the app, and you will see 2 sections called "Light background" and "Dark background".

Choose your preferred image for each sections, click "Save" if you want to save it for later use. If you do, you will see a prompt which asks you to start the theming service. Accept it, and you're ready to go!

You can close the app window, since the app is still accessable via the icon in the system tray.

The configuration is saved in a XML file. Here's the content on my file:
```xml
<data>
    <light>
        <image>C:\Users\Dell\Pictures\vanilla-day.png</image>
    </light>
    <dark>
        <image>C:\Users\Dell\Pictures\vanilla-night.png</image>
    </dark>
</data>
```

You can change the path in the ```image``` tag under both ```dark``` and ```light``` tags - open it by pass your full path to the file to the app.

## Inspirations
* [Dynamic-wallpaper](https://github.com/dusansimic/dynamic-wallpaper)
* GNOME Shell's auto wallpaper change on system theme change