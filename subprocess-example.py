import subprocess
p = subprocess.Popen(["/sbin/ifconfig","wlan0"], stdout=subprocess.PIPE)
arg1 = subprocess.Popen(["/bin/grep","-v","inet6"],stdin=p.stdout,stdout=subprocess.PIPE)
arg2 = subprocess.Popen(["/bin/grep","inet"],stdin=arg1.stdout,stdout=subprocess.PIPE)
arg3 = subprocess.Popen(["/bin/awk","{print $2}"],stdin=arg2.stdout,stdout=subprocess.PIPE)
arg4 = subprocess.Popen(["/bin/awk","-F:","{print $2}"],stdin=arg3.stdout,stdout=subprocess.PIPE)
ipAddr = arg4.stdout.read()
print ipAddr