import os
import subprocess, sys
import re

HOST = "Zabbix_hostname"
ZabS = "Zabix_server_ip"

def zabbix_sender(item, value):
        if os.path.isfile('/usr/bin/zabbix_sender') == True:
                path = os.path.join(r'/usr/bin/', 'zabbix_sender')
                command = '{0} -z {1} -s {2} -k {3} -o "{4}"'.format(path,ZabS,host,item,value)
                pipe = os.popen(command)
        elif os.path.isfile('C:\\zabbix\\bin\\win32\\zabbix_sender.exe') == True:
                path = os.path.join(r'C:\zabbix\bin\win32', 'zabbix_sender.exe')
                command = '{0} -z {1} -s {2} -k {3} -o "{4}"'.format(path,ZabS,HOST,item,value)
                pipe = os.popen(command)
        elif os.path.isfile('C:\\zabbix\\zabbix_sender.exe') == True:
                path = os.path.join(r'C:\zabbix', 'zabbix_sender.exe')
                command = '{0} -z {1} -s {2} -k {3} -o "{4}"'.format(path,ZabS,HOST,item,value)
                pipe = os.popen(command)

#System 1
if os.path.isfile('/etc/netact-release') == True:
        command = 'cat /etc/netact-release | grep -v "CDA" | grep "SP" | tail -1 | awk -F\'-\' \'{print$1,"-",$3}\''
        pipe = os.popen(command)
        output = pipe.read()
        item = "NMS.version"
        zabbix_sender(item, output)

        command = 'hostnamectl | grep "Operating System" | awk -F\':\' \'{print$2}\''
        pipe = os.popen(command)
        output = pipe.read()
        item = "OS.version"
        zabbix_sender(item, output)

#System 2
elif os.path.isfile('/opt/oracle/ocsm/etc/iptego/display_version') == True:
        command = 'cat /opt/oracle/ocsm/etc/iptego/display_version'
        pipe = os.popen(command)
        output = pipe.read()
        item = "NMS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)

        command = 'hostnamectl | grep "Operating System" | awk -F\':\' \'{print$2}\''
        pipe = os.popen(command)
        output = pipe.read()
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)

#System 3
elif os.path.isfile('/etc/iskratel_installed_products.properties') == True:
        command = 'cat /etc/iskratel_installed_products.properties | sed -n 1p'
        pipe = os.popen(command)
        output = pipe.read()
        item = "NMS.version"
        datastring = output.split('=')
        data = datastring[1]
        datastring = data.split(';')
        output = datastring[len(datastring)-1]
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        output = output.split(',')
        output = output[1] + "," + output[2]
        zabbix_sender(item, output)

        command = 'cat /etc/centos-release'
        pipe = os.popen(command)
        output = pipe.read()
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)

#System 4
elif os.path.isfile('C:\\Program Files\\Nokia Solutions and Networks\\Traffica\\TrafRTTServer\\traffica.exe') == True:
        path = os.path.join(r'C:\Program Files\Nokia Solutions and Networks\Traffica\TrafRTTServer', 'traffica.exe')
        command = 'powershell.exe Get-ChildItem "{0}"'.format(path)

        process = subprocess.Popen(["powershell","Get-Childitem \"C:\\Program Files\\Nokia Solutions and Networks\\Traffica\\TrafRTTServer\\traffica.exe\" | Get-ItemProperty | Select VersionInfo | Format-List *"],stdout=subprocess.PIPE);
        result = process.communicate()[0]
        result = str(result, 'utf-8')
        result = list(result.split('\n'))
        datastring = result[9]
        datastring = datastring.split(':')
        data = datastring[1]
        data = re.sub("^\s+|\n|\r|\s+$", '', data)
        item = "NMS.version"
        zabbix_sender(item, data)

        process = subprocess.Popen(["powershell","Get-WmiObject -Class Win32_OperatingSystem | ForEach-Object -MemberName Caption"],stdout=subprocess.PIPE);
        result = process.communicate()[0]
        result = str(result, 'utf-8')
        result = re.sub("^\s+|\n|\r|\s+$", '', result)
        item = "OS.version"
        zabbix_sender(item, result)

#System 5
elif os.path.isfile('/etc/SuSE-release') == True:
        command = 'cat /etc/SuSE-release | sed -n 1p'
        pipe = os.popen(command)
        output = pipe.read()
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)

        command = 'export PATH=$PATH:/opt/webserver/programs/proton/db/bin; source /home/webserverpt/.bashrc; su - webserverpt -c "psql -d pt -U webserver -c \'select * from portal.tbl_productinfo;\' | sed -n 3p"'
        pipe = os.popen(command)
        output = pipe.read()
        item = "NMS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        output = output.split('|')
        output = output[3]
        zabbix_sender(item, output)

#System 6
else:
        command = 'wmic os get Caption, CSDVersion'
        pipe = os.popen(command)
        output = pipe.read()
        result = list(output.split('\n'))
        item = "OS.version"
        output = result[1]
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)
