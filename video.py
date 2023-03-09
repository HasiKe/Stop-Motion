
import os
import moviepy.video.io.ImageSequenceClip


def get_settings():
    settings = open('settings.txt', 'r')
    for line in settings:
        if line[0] == '#':
            continue
        else:
            line = line.split('=')
            if line[0] =='Path':
                Path = line[1].strip()
    settings.close()
    fps = input("FPS: ")
    return Path, fps

image_files = [os.path.join(Path,img)
               for img in os.listdir(Path)
               if img.endswith(".jpg")]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
clip.write_videofile('video.mp4')

