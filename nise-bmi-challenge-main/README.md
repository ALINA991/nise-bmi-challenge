# NISE-game

<img
  src="/pictures/Network_Challenge.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 50px">

The [sEMG](https://www.dfrobot.com/product-1661.html) sensor is connected to an [ESP32](https://www.adafruit.com/product/3405) microcontroller, which is again connected through serial port to your laptop. At the moment, the keyboard buttons are the game's input, and via serial communication you can receive the RMS values from the sEMG. One of your task is to integrate the IMU to the communication network, e.g. for moving the player in the game. In the template [bmi_core.py](https://gitlab.lrz.de/student-projects/nise-bmi-challenge/-/blob/main/component_connection/bmi_core.py) you should write your own code to communicate with the game, that means to move the player up, down, left and right, set the shared memory variable `smd["move_direction"]` to 1, 2, 3 and 4, respectively. In contrast, EMG-based trigger intentions are detected which send a kick command to the game by setting the shared memory variable `smd["emg_trigger"]` to `True`. In addition, setting `smd["pull_ball"]` to `True` will trigger the pulling ball action.
The positions of player and ball in the game are transmitted via UDP communication to a second ESP32 microcontroller, which is again connected to four [vibro motors](https://www.adafruit.com/product/1201), providing the sensory feedback.

## Step 1: Clone
Clone this repo in your project directory:

```
cd your_folder
git clone https://gitlab.lrz.de/student-projects/nise-bmi-challenge.git 

```
## Step 2: ESP32 and Arduino
* Take two ESP32 and connect each to your laptop and leave both powered on.
* Upload `microcontroller_code/serial_emg_rms_esp32/serial_emg_rms_esp32.ino` to one ESP32 where the sEMG is connected to the analog input *A0*.
* Upload `microcontroller_code/udp_server_esp32_motors/udp_server_esp32_motors.ino` to the second ESP32 where four vibro motors are connected to the GPIOs *32*, *33*, *14* and *15*.


## Step 3: Communication and Game

We recommend using [VS Code](https://code.visualstudio.com/) as an editor and having [Python3.8](https://www.python.org/downloads/) or newer installed.

* Install [numpy](https://numpy.org/install/) with [pip](https://pypi.org/project/pip/):
```
pip install numpy
```

* Install [pyserial](https://pypi.org/project/pyserial/) with pip:
```
pip install pyserial
```

* Install [pygame](https://www.pygame.org/wiki/GettingStarted) with pip:
```
pip install pygame
```

* Install [Shared Memor Dict](https://pypi.org/project/shared-memory-dict/) with pip:
``` 
pip install shared-memory-dict 
``` 
* Connect your laptop in the network settings to the established WiFi network *ESP32_for_IMU* and log in with the password *ICSESP32IMU*:

<img
  src="/pictures/ESP32_for_IMU.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 50px">
  
* Open `component_connection/bmi_core.py` and replace COM**X** with the corresponding serial port that is connected with the ESP32 and the sEMG.
```python
port = serial.Serial('COM9', baudrate=512000) # Windows
# port = serial.Serial('/dev/ttyUSB0')  # Linux
```
* Open a terminal and run `component_connection/bmi_core.py` to establish the serial and UDP communication:
```
cd nise-bmi-challenge/component_connection
python bmi_core.py
```
If something like this appears, just run the script again:

<img
  src="/pictures/clear.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 50px">

* Run `game/main.py` in a second terminal to start the game:
```
cd nise-bmi-challenge/game
python main.py
```
---
## How to play:

<img
  src="/pictures/game_window.png"
  alt="Alt text"
  title="Optional title"
  style="display: inline-block; margin: 0 auto; max-width: 50px">


The objective is to bring the ball towards the goal. The soccer field has a size of 10 x 10 and the origin lies in the upper left corner. Remember that pygame counts positive when moving downwards along the y-direction. The blue triangle indicates the player which respawns in the first row after scoring a goal whereas the ball respawns in the forelast row.
* Certain `smd` values correspond to certain actions. For game testing, you can move the player, shoot and pull the ball with the following keyboard inputs:

|`shared memory smd[]`  | Key        | Action           | 
|-| ------------- |:-------------:|
|`smd["move_direction"]` = `1`| **w**      | Move player up      |
|`smd["move_direction"]` = `2`| **s**      | Move player down    |
|`smd["move_direction"]` = `3`| **a**      | Move player left   | 
|`smd["move_direction"]` = `4`| **d**      | Move player right    |
|`smd["emg_trigger"]` = `True`| **e**      | Shoot ball   |
|`smd["emg_trigger"]` = `True` `and` `smd["pull_ball"]` = `True`| **q** + **e**      | Pull ball| 

* In your final project, you will only have the IMU and the EMG for controlling the game and are **not** allowed to use the keyboard anymore. 
The ball can be shot only if the player is located next to the ball. Diagonal shooting is also possible by positioning the player diagonally next to the ball. Besides pressing the key **e**, setting the shared memory variable `smd["emg_trigger"]` to `True` based on the EMG activity would also trigger a shooting action.
At the moment, the pull action is activated with **q** so the ball can be pulled. Pressing **q** again deactivates the pull action. Instead of using they keyboard, setting `smd["pull_ball"]` to `True` will cause the player to pull the ball. 

* The vibro motors will vibrate depending on the array `intensity_array = []` that is sent through UDP, where the first value is sent to the input of the first motor, the second value to the input of the second motor etc. The value `0` would mean lowest vibration power and `9` most vibration power. In `udp_server_esp32_motors.ino`, the received motor array will then be mapped to the range between 0 and 255 for the `analogWrite()` function. 

| Vibro Motor        | Relation            | 
| ------------- |:-------------:|
| 1 (GPIO 32)             | x-position of the *ball* |
| 2 (GPIO 33)             | y-position of the *ball* |
| 3 (GPIO 14)             | x-position of the *player* |
| 4 (GPIO 15)             | y-position of the *player* |





