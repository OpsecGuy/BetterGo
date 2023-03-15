# CS-GO-python
External CS:GO cheat written in Python3-(11.2).  
Supported OS: Windows

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

## Contributors
- [boris768](https://github.com/boris768/)
- [AlexanderQueen](https://github.com/AlexanderQueen) - Tester

## UC Thread:
##### https://www.unknowncheats.me/forum/cs-go-releases/482499-python-external-multihack-exe-source.html

## F.A.Q:
<details close>
<summary>How do I use this?</summary>
1. Please read video description.<br>
2. Follow all the steps from that <a href="https://youtu.be/bwnokvZOPxo">VIDEO</a>.
</details>
<details close>
<summary>Application crashed/ not working</summary>
1. Check what python versions are installed on your PC and make sure you using at least python 3.8+ (3.11 is recommended).<br>
2. Go to <a href="https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl">WEBSITE</a>.<br>
3. Download PyOpenGL_accelerate‑3.1.6‑cp311‑cp311‑win_amd64.whl and PyOpenGL‑3.1.6‑cp311‑cp311‑win_amd64.whl<br>
4. Go to CMD and run this commands:<br>
pip install PyOpenGL-3.1.6-cp311-cp311-win_amd64.whl --force-reinstall<br>
pip install PyOpenGL_accelerate‑3.1.6‑cp311‑cp311‑win_amd64.whl<br>
5. Once you finish everything should be working fine. Go to the game and run cheat.
</details>
<details close>
<summary>I can not see overlay in game</summary>
Run game in 'Fullscreen Windowed' mode in video settings in order to use Overlay functions.
</details>
<details close>
<summary>I'm getting glfw.dll error</summary>
Make sure you have glfw.dll in the same folder where cheat is located.
</details>
<details close>
<summary>How do I compile* it?</summary>
1. Install <a href="https://github.com/pyinstaller/pyinstaller">PYINSTALLER</a>.<br>
2. Open CMD and type this commands:<br>
cd PATH_TO_FOLDER_WITH_SOFTWARE<br>
pyinstaller --onefile app.py --clean --windowed<br>
3. Once it finish compresing files, go to newly created 'dist' folder and run app.exe.
</details>
<details close>
<summary>Why would I like to compile it?</summary>
By compressing Python code you make application run more efficient. It can be clearly observed while using overlay features.
</details>
