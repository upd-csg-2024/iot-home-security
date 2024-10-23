# cs199csg-ip-camera-study

## Structure

### Root directory
Contains the LaTeX source code of our final paper (.zip file) as well as the PDF.

### `packet_captures` directory
Contains the Wireshark packet capture files that were analyzed in the study. Separated per camera.

### `scripts` directory
Contains any scripts that were used during the course of the study. Separated per camera.

#### `v380/decrypt.py`
Script used to extract the v380 camera's username and decrypt password contained in a packet sent by the app to the camera.

#### `c200/rtsp-url-brute.nse`
Script used to bruteforce for valid RTSP endpoints in the C200. This was fetched from https://nmap.org/nsedoc/scripts/rtsp-url-brute.html.

#### `c200/rtsp_authentication.py`
Modified python sript used to simulate RTSP handshake with the C200 using basic authentication. The original can be found here: https://gist.github.com/crayfishapps/a13e2026ba872ec192695a95b851f4a0

### `packet_captures` directory
Contains wireshark files that were used during the course of the study. Separated per camera.

#### `c200/vlc_rtsp.pcapng`
The packet capture file for when RTSP via the VLC was done for the C200. Use display filters `rtsp` and `rtp` for relevant packets.

#### `c200/python_script_rtsp.pcapng`
The packet capture file for when Basic Authentication was attempted using the python script for the C200. Use display filters `rtsp` and `rtp` for relevant packets.

#### `v380/cap_normal_connection.pcapng`
The packet capture file for the MITM attack collecting the communciations between the camera/phone and the Wi-Fi router. Use the `tcp.stream eq {n}` filter for n in (0, 2, 4, 21) to find the packets highlighted in the paper.

#### `v380/cap_direct.pcapng`
The packet capture file for the MITM attack collecting the communciations between the camera and the phone. Use the `udp.stream eq {n}` filter for n in (0, 2) and the `tcp.stream eq 0` filter to find the packets highlighted in the paper.
