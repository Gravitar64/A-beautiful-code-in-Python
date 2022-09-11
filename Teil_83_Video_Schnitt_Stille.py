import moviepy.editor as mvpe
import itertools as it


def lade_video(datei):
  name, ext = datei.split('.')
  return mvpe.VideoFileClip(datei), name+'_kurz.'+ext


def gen_video(video, ab, stille):
  audio = video.audio
  a = [audio.subclip(i*ab, (i+1)*ab).max_volume() >= stille for i in range(int(audio.end/ab))]
  s,l = zip(*[(k,len(list(g))*ab) for k,g in it.groupby(a)])
  c = [(sum(l[:i]), sum(l[:i+1])) for i in range(len(l)) if s[i]]
  return mvpe.concatenate_videoclips([video.subclip(s,e) for s,e in c])    


video1, ausgabedatei = lade_video('Teil_83_Beispiel.mp4')
video2 = gen_video(video1, 0.05, 0.03)
video2.write_videofile(ausgabedatei, fps=30, preset='ultrafast', codec='libx264',
                   temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac', threads=4)

print(f'Länge vorher/nacher = {video1.end:.2f} Sek. / {video2.end:.2f} Sek.')