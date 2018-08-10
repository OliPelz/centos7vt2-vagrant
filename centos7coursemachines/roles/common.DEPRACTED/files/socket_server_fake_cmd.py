#!/usr/bin/python
# taken and modified from https://www.thomaschristlieb.de/ein-python-script-mit-systemd-als-daemon-systemd-tut-garnicht-weh/
import socket
import os

# send messages from client like "myfakeprog|helloworld"
# which creates bash function with name myfakeprog() {printf "helloworld"}


def write_func(cmd_out):
      cmd_out = cmd_out.rstrip()
      (cmd, output) = cmd_out.split("|")
      # if ~/.myfunc does not exist create it (touch it)
      home_dir = os.environ["HOME"] 
      myfunc = home_dir + "/.myfunc"
      os.system("rm -f " + myfunc)
      os.system("touch " + myfunc)

      # escape output string so we can put it into echo
      output_esc = output
      # add function to .myfunctions file (append, never overwrite)
      out_var = "%s() \n{\n printf '%s\\n' \n}\n" % (cmd, output)
      # append to the end of the file
      with open(myfunc, "a") as f:
          f.write(out_var)
      out_var


# start
TCP_IP = '127.0.0.1'
TCP_PORT = 5006
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
cmd_out = ""
while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
       
    conn, addr = s.accept()
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        cmd_out += data
    conn.close()
    write_func(cmd_out)
    cmd_out = ""
