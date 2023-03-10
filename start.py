import subprocess
from datetime import datetime
import time
import os
import zipfile

FNULL = open(os.devnull, 'w')

zip_name = "Backup.zip"

Path = '/home/kevin/Bilder'
Backup_Path = '/home/kevin/backup'

# Set the camera settings
def get_settings():
    settings = open('settings.txt', 'r')
    for line in settings:
        if line[0] == '#':
            continue
        else:
            line = line.split('=')
            if line[0] == 'resolution':
                res = line[1].split('x')
                resolution = line[1].strip()
            elif line[0] == 'interval':
                interval = int(line[1].strip())
            elif line[0] == 'start_time':
                start_time = datetime.strptime(line[1].strip(), '%H:%M:%S').time()
            elif line[0] == 'end_time':
                end_time = datetime.strptime(line[1].strip(), '%H:%M:%S').time()
            elif line[0] == 'days':
                days = line[1].split(',')
                for i in range(len(days)):
                    days[i] = int(days[i])
    settings.close()
    return resolution, start_time, end_time, days, interval

#get last file
def get_file():
    num = 0
    num2 = 0
    for file in os.listdir(Path):
        file = file.split('_')
        num = int(file[0])
        num2 = len(os.listdir(Path))
        if num2 > num:
            num = num2
        num = num2
    return num


def backup():
    datei_liste = os.listdir(Path)
    zip_name = str(len(os.listdir(Path)))
    with zipfile.ZipFile(os.path.join(Backup_Path, zip_name), "w") as zip:
        for datei in datei_liste:
            rel_pfad = os.path.relpath(datei)
            zip.write(datei, rel_pfad)

#start camera
def start_camera():
    resolution, start_time, end_time, days, interval = get_settings()
    while True:
        now = datetime.now().time()
        

        if start_time <= now <= end_time and datetime.today().weekday() in days:
            num = get_file()
            num += 1
            resolution, start_time, end_time, days, interval = get_settings()
            filename = '{}/{}_{}.jpg'.format(Path, "{:05d}".format(int(num)),datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            subprocess.call(['ffmpeg', '-f', 'video4linux2', '-i', '/dev/video0', '-vframes', '1', '-video_size', resolution, filename], stdout=FNULL, stderr=subprocess.STDOUT)
            time.sleep(interval)

        elif "01:00:00" <= now <= "04:01:00":
            for back in os.listdir(Backup_Path):
                back = back.split('.')
                if(back[0] != str(len(os.listdir(Path)))):
                    backup()

start_camera()
