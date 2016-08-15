#!/usr/bin/python           # This is client.py file
import paramiko
import socket               # Import socket module

username = "boven"
passwd = "10.087"

def ssh_addrule(ip,username,passwd,inport,outport):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        stdin, stdout, stderr = ssh.exec_command("ovs-ofctl add-flow br0 in_port=%d,actions=output:%d"%(inport,outport))
        stdin, stdout, stderr = ssh.exec_command("ovs-ofctl add-flow br0 in_port=%d,actions=output:%d"%(outport,inport))
        ssh.close()
        print "Added rules between Port %d and Port %d at Ip %s"%(inport,outport,ip)
    except :
        print '%s\tError\n'%(ip)

def ssh_delrule(ip,username,passwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,passwd,timeout=5)
        stdin, stdout, stderr = ssh.exec_command("ovs-ofctl del-flow br0")
        ssh.close()
        print "Deleted all rules at %s"%(ip)              
    except :
        print '%s\tError\n'%(ip)

def test_connection():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345                # Reserve a port for your service.
    if (s.connect((host, port)) == 0):
        print "Link Error"
        exit()
    print "Conncetion Correct"
    print s.recv(1024)
    s.close			# Close the socket when done

def s1_test():
    ip = "10.1.0.3"
    print "Switch 1 Test Begin"
    print "Testing Port 1 and Port 2"
    ssh_addrule(ip,username,passwd,1,2)
    test_connection()
    ssh_delrule(ip,username,passwd)
    print "Switch 1 Correct"

def s23_test():
    print "Switch 2 and Switch 3 Test Begin"
    for i in range(1,4):
        ip = "10.1.0.3"
        ssh_addrule(ip,username,passwd,1,16+i)
        ssh_addrule(ip,username,passwd,2,22+i)
        ip = "10.1.0.5"
        ssh_addrule(ip,username,passwd,12+i,18+i) 
        ip = "10.1.0.6"
        ssh_addrule(ip,username,passwd,16+i,22+i)
        test_connection()
        ssh_delrule(ip,username,passwd)
    print "Switch 2 and 3 Correct"

if __name__=='__main__':
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    print "Test Begin"
    s1_test()
    s23_test()
