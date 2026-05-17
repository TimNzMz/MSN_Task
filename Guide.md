#Zephyr Openthread

##Guide usecase
###Zephyr Openthread
This guide provides the steps needed for analysing the pakcages sent between a Border Router and a CoAP server node.
1. Stick the border router and the coap server inside of the computer
2. (Powershell administrator): usbipd list/ usbipd attach bind --force --busid / usbipd attach --wsl --busid
    These command are to link the usb ports with wsl.
3. Check the usb connection: ls /dev/ttyACM*
4. sudo ot-ctl state (if it doesn't say leader, continue, otherwise, move to step 6)
5. Run these commands step by step: sudo ot-ctl(thread stop, ifconfig down, dataset init new, dataset commit active, ifconfig up, thread start, state). https://openthread.io/guides/border-router/external-commissioning/prepare
    It should display "leader"
6. Insert the sniffer and open wireshark
7. Look in the list of interfaces and click on the parameters of the interface called "nRF Sniffer for 802.15.4: COM18"
8. In wsl, type ot-ctl channel to get the channel on which the network is sending packages and fill this channel number inside of the parameters of the interface.
9. You should now see packages that are being picked up by the sniffer.

Look at the official documentation NORDIC regarding the setup for the sniffer.
STARTING

Source: f80::28b1:812c:93b5:c3f0 and Destination ff02::1 with the the protocol MLE (Mesh Link Establishment) and info, Advertisement. Than This means that our computer, who it initiating the network and is extended by the fysical border router is sending a message to all devices to form a network.
Iconfig up, will bring up the ipv6 interface. By just writing ifconfig, you can see if the ipv6 interface is up or down. If the ipv6 interface is up, you start the thread by doing "sudo ot-ctl thread start", (sometimes doing sudo ot-ctl dataset active works better) and the router will now send a "Link Request" and a "Parent Request". You can check the state of your router by doing "sudo ot-ctl state" and your border router should be put to "leader".

Next you can connect your coap server wich in this case would be your nrf-dongle.
When you plug in the dongle you will see that the dongle with adres "fe80" send a "Child Update Request" to the BTR. The BTR sends an Ack to the dongle to tell him that it received the package. The BTR will than respond with "Child Update Response". 
Dongle will send a "Parent Request". BTR will send a "Parent Response" and after some time the Dongle will send a "Child ID Request" and at the end the BTR will respond with a "Child ID response".
