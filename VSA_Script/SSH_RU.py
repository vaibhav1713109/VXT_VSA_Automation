import paramiko

def take_SSH(host,user,pswrd,CMD):
    host = host
    port = 22
    username = user
    password = pswrd

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    for command in CMD:
        stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()




