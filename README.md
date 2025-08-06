# Getting ARX arm to comply

How to set up your Ubuntu (no NixOS @Max!!) laptop/computer to work with CAN and control the R5 arm, even over network! This guide assumes one arm only.

## 1. Building the project

1. **Install pybind in root of this repo**
```bash
git clone https://github.com/pybind/pybind11.git && cd pybind11 && mkdir build && cd build
```

> Quick aside, pybind is the bridge between Python and C++ code, allowing python to use functions like the kinematic solver created in C++.

Before continuing to step #3, check if CMAKE is installed in the correct location:

```bash
which cmake
cmake --system-information | grep CMAKE_ROOT
```

<details>
<summary>Click here for troubleshooting steps if <code>which cmake</code> returns <code>/usr/local/bin</code> and if <code>cmake --system-information | grep CMAKE_ROOT</code> returns an error like <code>CMAKE_ROOT not found!!!</code></summary>

1. **Remove the problematic CMake + cache:**
   ```bash
   sudo apt remove --purge cmake cmake-data
   sudo rm -rf /usr/local/bin/cmake
   sudo rm -rf /usr/local/share/cmake*
   sudo rm -rf /usr/local/doc/cmake*
   sudo apt autoremove
   sudo apt autoclean
   ```

2. **Install CMake from apt:**
   ```bash
   sudo apt update
   sudo apt install cmake
   ```

3. **Verify the installation:**
   ```bash
   which cmake
   ```
   You should now see something like `/usr/bin/cmake`.
   ```bash
   cmake --system-information | grep CMAKE_ROOT
   ```
   You should see a path to CMAKE_ROOT. If it says `Cannot find CMAKE_ROOT!!!`, ask GPT or email [alessio@vassarrobotics.com](mailto:alessio@vassarrobotics.com). Likely you will need to install the tar.gz from CMAKE's website and get it in the right location. Also, make sure that you are doing this all from the system terminal and not VSCode. Sometimes paths are not cached or there are issues with bash.rc.
</details>


<br>
Once CMAKE is configued correctly, while still in the `build` folder in `pybind11`, run this next step:

2. **Build pybind's CMAKE packages (this could take a minute)**
```bash
cmake .. && make && sudo make install
```

3. **Build the actual project's CMAKE packages**
```bash
cd ../../py/ARX_R5_python
./build.sh
```

## 2. CAN Configuration

This step is important to make sure you can connect *reliably* over USB to the robot's CAN.

1. **Install CAN libraries**
```bash
sudo apt install can-utils
sudo apt install net-tools
```

Then, plug in your USB cable for the CAN device before this next step:

2. **Find CAN device serial number**
```bash
sh search.sh
```
This will open up a new terminal and print a serial number. If the device is unknown, then you should un-plug and plug it back in. It can get iffy at times. If it works, example output looks like this: `ATTRS{serial}=="209738784D4D"`

3. **Replace serial number in `arx_can.rules`**
Open `arx_can.rules` in the root of the `ARX_can` folder, and replace the serial number for `arxcan1` with the detected one. For example:

```text
ATTRS{serial}=="209738784D4D", SYMLINK+="arxcan1"
```

4. **Run `set.sh`**
```bash
./set.sh
```
No errors should appear if you did everything correctly.

5. **Moment of truth test for CAN!**
```bash
./arx_can1.sh
```
You should hopefully see a stream of text resembling `CAN 接口 can1 正常工作`.

## 3. Running the arm

In every new terminal, make sure you run:
```bash
source ./setup.sh
```

Here's a simple, single-arm test:
```bash
python3 test_keyboard.py
```
You can press the arrow keys and observe the magic of inverse kinematics!