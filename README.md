[![Build Wheels](https://github.com/lebao3105/wallchange/actions/workflows/wheels.yml/badge.svg)](https://github.com/lebao3105/wallchange/actions/workflows/wheels.yml)
## Wallchange
An automated tool to set your desktop background!

## Running
This project requires Python 3.8+ with pip installed. Tested on **Windows** and **Linux**.

Install dependencies first:
```bash
$ pip install attrdict3
$ pip install -r requirements.txt
```

Use meson to install:
```bash
$ meson setup build # Add --prefix=~/.local for local installation
$ ninja -C build install
$ me.lebao3105.wallchange [filepath] # Run
```

Or install using generated wheels on (https://github.com/lebao3105/wallchange/actions/workflows/wheels.yml):
```bash
$ pip install <downloaded .whl file> --force-reinstall
```

Or:
```bash
$ pip install build wheel
$ pip install . --force-reinstall
```

Run without installing:
```bash
$ python3 -m wallchange [filepath] # Run
```

## Usage
Open the app, and you will see 2 sections called "Light background" and "Dark background".

Choose your preferred image for each sections, click "Save" if you want to save it for later use. If you do, you will see a prompt which asks you to start the theming service. Accept it, and you're ready to go!

You can close the app window, since the app is still accessable via the icon in the system tray.

When the auto wallpaper-set service started and successfully set your wallpaper, it will show messages:
![image](https://user-images.githubusercontent.com/77564176/213847343-3bdabed4-3704-4197-81f8-9df09a72ac02.png)

Wallpaper-set demostration:
![link here](https://user-images.githubusercontent.com/77564176/213848497-3af86855-2e8a-4729-9728-2359acb27a12.webm)

The configuration is saved in a XML file. Here's the content on my file:
```xml
<? xml version="1.0" encoding="UTF-8"?>
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
* It is recommended to set this app to run automatically on log-in.

## Inspirations
* [Dynamic-wallpaper](https://github.com/dusansimic/dynamic-wallpaper)
* GNOME Shell's auto wallpaper change on system theme change
