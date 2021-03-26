import os
import subprocess, sys
import re

HOST = "Zabbix_hostname"
ZabS = "Zabix_server_ip"

def zabbix_sender(item, value):
        for path in ['C:\\zabbix\\bin\\win32\\zabbix_sender.exe', 'C:\\zabbix\\zabbix_sender.exe', '/usr/bin/zabbix_sender']:
                if os.path.isfile(path) == True: pipe = os.popen('{0} -z {1} -s {2} -k {3} -o "{4}"'.format(path,ZabS,host,item,value))

#System 1
if os.path.isfile('/etc/netact-release') == True:
        output = os.popen('cat /etc/netact-release | grep -v "CDA" | grep "SP" | tail -1 | awk -F\'-\' \'{print$1,"-",$3}\'').read()
        item = "NMS.version"
        zabbix_sender(item, output)

        output = os.popen('hostnamectl | grep "Operating System" | awk -F\':\' \'{print$2}\'').read()
        item = "OS.version"
        zabbix_sender(item, output)

#System 2
elif os.path.isfile('/opt/oracle/ocsm/etc/iptego/display_version') == True:
        output = os.popen('cat /opt/oracle/ocsm/etc/iptego/display_version').read()
        item = "NMS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)

        output = os.popen('hostnamectl | grep "Operating System" | awk -F\':\' \'{print$2}\'').read()
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output)

#System 3
elif os.path.isfile('/etc/iskratel_installed_products.properties') == True:
        output = os.popen('cat /etc/iskratel_installed_products.properties | sed -n 1p').read()
        item = "NMS.version"
        datastring = output.split('=')[1].split(';')
        output = re.sub("^\s+|\n|\r|\s+$", '', datastring[len(datastring)-1])
        output = output.split(',')
        output = output[1] + "," + output[2]
        zabbix_sender(item, output, HOST)

        output = os.popen('cat /etc/centos-release').read()
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output, HOST)

#System 4
elif os.path.isfile('C:\\Program Files\\Nokia Solutions and Networks\\Traffica\\TrafRTTServer\\traffica.exe') == True:
        path = os.path.join(r'C:\Program Files\Nokia Solutions and Networks\Traffica\TrafRTTServer', 'traffica.exe')
        command = 'powershell.exe Get-ChildItem "{0}"'.format(path)

        process=subprocess.Popen(["powershell","Get-Childitem \"C:\\Program Files\\Nokia Solutions and Networks\\Traffica\\TrafRTTServer\\traffica.exe\" | Get-ItemProperty | Select VersionInfo | Format-List *"],stdout=subprocess.PIPE);
        result=process.communicate()[0]
        result = list(str(result, 'utf-8').split('\n'))
        datastring = result[9].split(':')
        data = re.sub("^\s+|\n|\r|\s+$", '', datastring[1])
        item = "NMS.version"
        zabbix_sender(item, data, HOST)
        
        process=subprocess.Popen(["powershell","Get-WmiObject -Class Win32_OperatingSystem | ForEach-Object -MemberName Caption"],stdout=subprocess.PIPE);
        result=process.communicate()[0]
        result = re.sub("^\s+|\n|\r|\s+$", '', str(result, 'utf-8'))
        item = "OS.version"
        zabbix_sender(item, result, HOST)

#System 5
elif os.path.isfile('/etc/SuSE-release') == True:
        command = 'cat /etc/SuSE-release | sed -n 1p'
        output = os.popen('cat /etc/SuSE-release | sed -n 1p').read()
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        zabbix_sender(item, output, HOST)

        command = 'export PATH=$PATH:/opt/webserver/programs/proton/db/bin; source /home/webserverpt/.bashrc; su - webserverpt -c "psql -d pt -U webserver -c \'select * from portal.tbl_productinfo;\' | sed -n 3p"'
        pipe = os.popen(command)
        output = pipe.read()
        item = "NMS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', output)
        output = output.split('|')[3]
        for host in [HOST_CSProbe, HOST]:
                zabbix_sender(item, output, host)

#System 6
else:
        output = os.popen('wmic os get Caption, CSDVersion').read()
        result = list(output.split('\n'))
        item = "OS.version"
        output = re.sub("^\s+|\n|\r|\s+$", '', result[1])
        zabbix_sender(item, output)
