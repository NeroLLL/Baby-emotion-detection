#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform
import json
import os

if platform.uname()[1] == 'raspberrypi':
    import RPi.GPIO as GPIO

#这里是MarsIoT缺省命令的处理，用户自己的命令尽量不要定义在这个文件里
class default_command(object):

    def __init__(self, marsiot):
        self.marsiot = marsiot

        if platform.uname()[1] == 'raspberrypi':
            self.gpioSetup()

    def __del__(self):
        if platform.uname()[1] == 'raspberrypi':
            self.gpioClean()

    def gpioSetup(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        bcm_gpios = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
        for pin in bcm_gpios:
            #配置为上拉电阻输入方式
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            #当检测到上升沿(RISING)/下降沿(FALLING)/上升和下降(BOTH)时触发事件响应
            #bouncetime为防抖处理
            GPIO.add_event_detect(pin, GPIO.BOTH, callback = self.gpioEventHandler, bouncetime=500) 
    
    def gpioClean(self):
        GPIO.cleanup()

    def gpioEventHandler(self, pin):
        print("事件 gpio" + str(pin) + "变化为" + str(GPIO.input(pin)))
        self.marsiot.send_message("message", "gpio" + str(pin) + ":" + str(GPIO.input(pin)))

    def helloWorld(self, args):
        greeting = args['greeting'] + " World!"
        if args['loud'] == 'true':
            greeting = greeting.upper()
        self.marsiot.send_message("message", "hello world!")

    def getGpioStatus(self, args):
        if platform.uname()[1] != 'raspberrypi':
            return

        if args.has_key('gpios'):
            gpios = args['gpios'].split(',')
            my_message = {}

            for gpio in gpios:
                try:
                    pin = int(gpio)
                except Exception as e:
                    print("错误！gpio编号为空或者不是数字")
                    return

                try:
                    my_message['gpio' + bytes(pin)] = GPIO.input(pin) 
                except Exception as e:
                    print("错误！gpio"+str(pin)+"不可用")
                    print("参考文档https://www.marsiot.com/wiki/doku.php?id=pi-gpio-naming")

            my_message_string = json.dumps(my_message)    
            print("返回 " + my_message_string)
            self.marsiot.send_message("message", my_message_string)
        else:
            print("错误！gpio列表为空")

    def setGpio(self, args):
        if platform.uname()[1] != 'raspberrypi':
            return

        try:
            pin = int(args['gpio'])
        except Exception as e:
            print("错误！gpio编号为空或者不是数字")
            return

        try:
            GPIO.setup(pin, GPIO.OUT)
            if args['high'] == 'true':
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)
        except Exception as e:
            print("错误！gpio"+str(pin)+"不可用")
            print("参考文档https://www.marsiot.com/wiki/doku.php?id=pi-gpio-naming")

    def getInfoFromSystem(self, args):
        if platform.uname()[1] == 'raspberrypi':
            model = os.popen('cat /proc/device-tree/model')

            my_message = {}
            my_message['model'] = model.read()
            my_message_string = json.dumps(my_message)    
            print("返回 " + my_message_string)
            self.marsiot.send_message("message", my_message_string)

        else:
            model = os.popen('cat /etc/issue').read()

            my_message = {}
            my_message['model'] = model.strip()
            my_message_string = json.dumps(my_message)    
            print("返回 " + my_message_string)
            self.marsiot.send_message("message", my_message_string)




