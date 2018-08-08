#!/usr/bin/python 

# -*- coding: utf-8 -*-
import socket
import os, os.path, sys
import select
import subprocess
import threading 
import subprocess
import argparse
import time
from subprocess import check_output
class ServerThread(threading.Thread): 
    def __init__(self, sock_file): 
        threading.Thread.__init__(self) 
        self.sock_file = sock_file

    def run(self):
       sock_file = self.sock_file
       if os.path.exists( sock_file ):
          os.remove( sock_file )
       server = socket.socket( socket.AF_UNIX, socket.SOCK_DGRAM )
       server.bind(sock_file)
       while True:
       # blocking ...less CPU consumption
         (inputready,outputready,exceptready) = select.select([server],[],[])
         # if we are here there has been input and blocking is released
         datagram_socket = inputready[0]
         datagram = datagram_socket.recv( 128 )
         #print datagram
         if not datagram:
           break
         else:
           #print datagram
           if (datagram == "DONE"):
	       #print "Server exited!!!!"
               break
         # to learn more about color codes goto    
           elif(datagram.find("whiteblue_") is not -1):
               cmd = datagram.split("_")[1]
               os.system("echo -e '\E[37;44m'\"\033[1m" + cmd + "\033[0m\"")
           elif(datagram.find("whitered_") is not -1):
               cmd = datagram.split("_")[1]
               os.system("echo -e '\E[37;41m'\"\033[1m" + cmd + "\033[0m\"")
           elif(datagram.find("whitegreen_") is not -1):
               cmd = datagram.split("_")[1]
               os.system("echo -e '\E[37;42m'\"\033[1m" + cmd + "\033[0m\"")
           # reset colors
           #os.system("echo -ne \E[0m")
       server.close()
       os.remove( sock_file )


class SocketClient:
    def __init__(self, sock_file): 
        self.sock_file = sock_file
	# add some interval between server and client ... possible creation and connecting to the socket 
	time.sleep(0.1)
    def sendMsg(self, msg):
      try:
       s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
       s.connect(self.sock_file)
       s.send(msg)
       #data = s.recv(128)
       s.close()
      except:
       print "cannot connect, socket not existent @ " + self.sock_file
       #print('Received ' + repr(data))
    

def my_argparse():
    parser = argparse.ArgumentParser(description='colored echo socket server/client')
   # subcommands are server and client
    subparsers = parser.add_subparsers(dest="subcommand", title="subcommands")
# The "server" command.

    parser_server = subparsers.add_parser("server")
    parser_server.add_argument("socketfile")
# the client subcommand
    parser_client = subparsers.add_parser("client")
    parser_client.add_argument("socketfile")
    parser_client.add_argument("--message", default="",
                        help="the message to send to colorize echo on server")

# Parse the actual arguments and do some addition sanity-checking.
    args = parser.parse_args(sys.argv[1:])
    if not args.subcommand:
      parser.error("too few arguments")

    socket_file=args.socketfile
    subcommand = args.subcommand
    if(subcommand == "server"):
      ss = ServerThread(socket_file)
      ss.start()
    elif(subcommand == "client"):
      sc = SocketClient(socket_file)
      print "client sends following message: " + args.message
      sc.sendMsg(args.message)


my_argparse()
