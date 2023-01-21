## Wallchange
An automated tool to set your desktop background!

## Running
This project requires Python 3.8+ with pip installed. **No macOS support.**

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

When the auto wallpaper-set service started and successfully set your wallpaper, it will show messages:
![image](https://user-images.githubusercontent.com/77564176/213847343-3bdabed4-3704-4197-81f8-9df09a72ac02.png)


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

## Issue(s)
* If you use GNOME 42+, you may see that your wallpaper used in this program not used in your desktop when you change the system color. It occurred due to the new wallpaper system (WallChange based on that). Now I fixed it by setting another schema path for dark mode (/org/gnome/desktop/background/picture-uri-dark).

## Inspirations
* [Dynamic-wallpaper](https://github.com/dusansimic/dynamic-wallpaper)
* GNOME Shell's auto wallpaper change on system theme change
