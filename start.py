import subprocess
from datetime import datetime
import time
import os

FNULL = open(os.devnull, 'w')

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
    for file in os.listdir('/home/kevin/Bilder'):
        file = file.split('_')
        num = int(file[0])
        num2 = len(os.listdir('/home/kevin/Bilder'))
        if num2 > num:
            num = num2
        num = num2
    return num


#start camera
def start_camera():
    resolution, start_time, end_time, days, interval = get_settings()
    while True:
        now = datetime.now().time()
        if start_time <= now <= end_time and datetime.today().weekday() in days:
            num = get_file()
            num += 1
            resolution, start_time, end_time, days, interval = get_settings()
            filename = '/home/kevin/Bilder/{}_{}.jpg'.format("{:05d}".format(int(num)),datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            subprocess.call(['ffmpeg', '-f', 'video4linux2', '-i', '/dev/video0', '-vframes', '1', '-video_size', resolution, filename], stdout=FNULL, stderr=subprocess.STDOUT)
            time.sleep(interval)

start_camera()
