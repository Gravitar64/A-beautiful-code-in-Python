import moviepy.editor as mvpe
import itertools as it
from time import perf_counter as pfc


def lade_video(datei):
  name, ext = datei.split('.')
  return mvpe.VideoFileClip(datei), name+'_kurz.'+ext


def gen_clips(video, ab, stille):
  audio = video.audio
  a = [audio.subclip(i*ab, (i+1)*ab).max_volume() >= stille for i in range(int(audio.end/ab))]
  b = [(k,len(list(g))*ab) for k,g in it.groupby(a)]
  clips, start = [], 0
  for sprache, länge in b:
    if sprache: 
      clips.append(video.subclip(start,start+länge))
    start += länge   
  return clips       


start = pfc()
video1, ausgabedatei = lade_video('Teil_83_Beispiel.mp4')
video2 = mvpe.concatenate_videoclips(gen_clips(video1,0.05,0.03))
video2.write_videofile(ausgabedatei, fps=30, preset='ultrafast', codec='libx264',
                   temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac', threads=4)

print(f'Länge vorher/nacher = {video1.end:.2f} Sek. / {video2.end:.2f} Sek.')
print(pfc()-start)
