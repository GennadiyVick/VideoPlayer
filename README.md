# VideoPlayer. 
VideoPlayer based on libvlc for python and pyqt5 for gui. 
The program was written for using on a laptop with a connected projector.

![screenshot](https://github.com/GennadiyVick/VideoPlayer/blob/master/image.jpg)
During playback, the video window hotkeys work.
Spacebar - pause/play, F key to switch to full screen mode and back.
Escape key to stop playback.
Left and right keys for 15 sec. backward and forward skipping, up and down keys for 1 min. backward and forward skipping, Page Up and Page Down keys for 5 min. skipping.
Keys / and * to decrease and increase the volume respectively.

## Required:
To run the program, you need python itself and the installed PyQt5 and libvlc modules.

## Installing python and PyQt5 and libvlc modules.  

### MS Windows:
You can download the distribution from [python.org](https://www.python.org/downloads/) and double-click the installation  
after installation, you need to install the `PyQt5` and `libvlc` modules, to do this in the console enter 
```console
python -m pip install pyqt5
python -m pip install python-vlc
```
the program will download and install the module.
To run this program, you must enter in the console
```console
python program_path\VideoPlayer.py
```
You can also create a launch shortcut on the desktop.
To run from a shortcut, use `pythonw` instead of `python`
```console
pythonw program_path\VideoPlayer.py
```

### Linux:
For the program to work in Linux, you need to use python version 3 or higher.
Most distributions have python preinstalled and you don't need to download and install it, 
you just need to install the `PyQt5` and `libvlc` modules.
If you do not have python3 installed, you can install it using your package manager, 
for example, in distributions based on Debian, it is installed like this:
```console
sudo apt-get install python3
```
To install the module in the console, enter
```console
sudo apt-get install python3-pyqt5
pip3 install python3-vlc
```
modules will be automatically downloaded and installed.
The program starts like this:
```console
python3 program_path/VideoPlayer.py
```
You can also add permission to run the script and double-click to run it, as well as create a desktop shortcut.

Author: Roganov G.V. roganovg@mail.ru


