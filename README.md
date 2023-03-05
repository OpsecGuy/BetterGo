# CS-GO-python
External CS:GO cheat written in Python(3.11).

## Functions:
- Aimbot
- GlowESP
- Recoil Control System
- TriggerBot
- Auto Pistol
- BunnyHop
- Chat Spam
- Pattern Scan
- OpenGL Overlay
- Many more... :)

## In game
![This is an image](https://i.imgur.com/VlAsuOp.png)

## Instruction
- Please read video description

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/bwnokvZOPxo/0.jpg)](https://www.youtube.com/watch?v=bwnokvZOPxo)

## Contributors
- [boris768](https://github.com/boris768/)
- [AlexanderQueen](https://github.com/AlexanderQueen) - Tester

## UC Thread:
##### https://www.unknowncheats.me/forum/cs-go-releases/482499-python-external-multihack-exe-source.html

## F.A.Q:
#### Overlay is crashing/ not working
1. Check what python versions are installed on your PC and make sure you using at least python 3.8+ (3.11 is recommended)
2. Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl
[FOR PYTHON 3.11]
3. Download PyOpenGL_accelerate‑3.1.6‑cp311‑cp311‑win_amd64.whl and PyOpenGL‑3.1.6‑cp311‑cp311‑win_amd64.whl
4. Go to CMD and run this commands:
pip install PyOpenGL-3.1.6-cp311-cp311-win_amd64.whl --force-reinstall
pip install PyOpenGL_accelerate‑3.1.6‑cp311‑cp311‑win_amd64.whl
5. Once you finish everything should be working fine. Go to the game and run cheat
#### I can not see overlay in game
Run game in 'Fullscreen Windowed' mode in video settings in order to use Overlay functions.
#### In case of glfw.dll error
Place glfw.dll in the same folder where cheat is located.
#### How do I compile it [WINDOWS]?
1. Install [pyinstaller](https://github.com/pyinstaller/pyinstaller) for that.
2. Open CMD and type this commands:
3. cd PATH_TO_FOLDER_WITH_CHEAT
4. pyinstaller --onefile app.py --clean
5. Once it finish compresing files, go to new created 'dist' folder and run app.exe
