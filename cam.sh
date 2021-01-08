for i in $(seq 3600);do
    sudo fswebcam -d /dev/video0 320*240 /home/pi/image.jpg
    sleep 40
done;
