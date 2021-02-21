import os

os.system("apt install ipmitool")

def createfanpwrscripts(val):
    command = "ipmitool -U root -P calvin raw 0x30 0x30 0x02 0xff "
    command = command + hex(val)
    cmd = "mkdir -pv idrac-files && cd idrac-files && echo '" + command + "' > idrac-fanpwr" + str(val)
    os.system(cmd)

for i in range(6):
    createfanpwrscripts(i*5)

setmanual = "mkdir -pv idrac-files && cd idrac-files && echo 'ipmitool -U root -P calvin raw 0x30 0x30 0x01 0x00' > idrac-setmanual"
setauto = "mkdir -pv idrac-files && cd idrac-files && echo 'ipmitool -U root -P calvin raw 0x30 0x30 0x01 0x01' > idrac-setauto"
createresetidrac = "mkdir -pv idrac-files && cd idrac-files && echo 'ipmitool user list 1 \\nipmitool user set password 2' > idrac-resetpw"
showtemp = "mkdir -pv idrac-files && cd idrac-files && echo 'ipmitool sdr elist all | grep -i 0Eh' > idrac-showtemp"

os.system(setmanual)
os.system(setauto)
os.system(createresetidrac)
os.system(showtemp)
os.system("cd idrac-files && chmod +x * && mv * /bin/ && cd .. && rm -rf idrac-files")

print("All files created and moved to /bin.")
print("Commands: \nidrac-fanpwr(0-25)\nidrac-setmanual\nidrac-setauto\nidrac-showtemp\nidrac-resetpw")

os.system("(crontab -l; echo '@reboot /bin/idrac-setmanual \\n@reboot /bin/idrac-fanpwr10';) | crontab -")
print("Added settings to cron: \n - Set fans to manual mode at boot\n - Set fans to 10% of their power at boot\n !!! ALL COMMANDS MUST BE RUN AS ROOT !!!")



