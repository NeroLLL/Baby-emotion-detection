#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

#os.system("python /home/pi/feedback.py")


class my_command(object):
    def __init__(self, marsiot):
        self.marsiot = marsiot

    #def __del__(self):

    def test(self, args):
        self.marsiot.send_message("message", args['cool'])

    def send_email(self,marsiot):
	os.system("python /home/pi/mail_main.py")
		
