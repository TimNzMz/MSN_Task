$ sudo apt update
$ sudo apt upgrade -y
$ sudo apt install --no-install-recommends git cmake ninja-build gperf \
  ccache dfu-util device-tree-compiler wget python3-dev python3-venv python3-tk \
  xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1 docker.io
  
$ git clone https://github.com/openthread/ot-br-posix
# cd ot-br-posix
$ git checkout fbde28a
$ ./script/bootstrap
// check the internet interface name with the following. it can be a nime like eth0, wlan0, wlp2s0
$ ifconfig -a
// use the name you got in the following
$ INFRA_IF_NAME=<interface> ./script/setup
$ ./script/server
// modify the file /etc/default/otbr-agent
$ sudo nano /etc/default/otbr-agent
// change it so it says spinel+hdlc+uart:///dev/ttyACM0?uart-baudrate=1000000
//verify if the service is activate
$ sudo service otbr-agent status
  
$ python3 -m venv ~/zephyrproject/.python3-venv
$ echo "alias zephyr-env='source ~/zephyrproject/.python3-venv/bin/activate'" >> ~/.bashrc
$ source ~/.bashrc
$ zephyr-env
$ pip install west
$ west init ~/zephyrproject
$ cd ~/zephyrproject
$ west update
$ west zephyr-export
$ west packages pip --install
$ cd ~/zephyrproject/zephyr
$ west sdk install
$ deactivate

// To form a thread network you'll need to start it
https://openthread.io/guides/border-router/form-network

NOW IN (base) timnz@DESKTOP-U9BO5EO:~/zephyrproject/zephyr$

// nrfutil is needed to upload to the devices. make it executable and move it to the correct directory (from where you unpacked the zip)
$ chmod +x nrfutil
$ sudo mv nrfutil /usr/local/bin/
$ nrfutil install completion device device nrf5sdk-tools toolchain-manager trace

// compiling for the nrf dongles (using the blinky example). Do this in the correct environment (zephyr-env). The dongle needs to be in dfu mode, press the small sideways button (red led should blink)
#Zephyr code -> comiled -> packaged -> sent via DFU -> flashed
$ cd ~/zephyrproject/zephyr/samples/basic/blinky
### west build -> zephyr's build system, nrf -> target board=nrf52840 USB dongle; build the current project blinky; creates build/zephyr/zephyr.hex => so we compile the code and create the build/zephyr/zephyr.hex file
$ west build -p always -b nrf52840dongle/nrf52840 ./
###create DFU package; app_dfu_package.zip -> output file; output is a zip file containing: firmware, metadata, checksums (what the bootloader understands) => Wraps the .hex into a DFU package (.zip)
$ nrfutil pkg generate --hw-version 52 --sd-req 0x00 --application build/zephyr/zephyr.hex --aplication_version 1 app_dfu_package.zip 
###Upload via DFU over USB; dfu usb-serial -> use USB serial DFU protocol, the DFU package we created, -p /dev/ttyACM1 -> USB port of my dongle => Sends the package to the device
$ nrfutil dfu usb-serial -pkg app_dfu_package.zip -p /dev/ttyACM0

