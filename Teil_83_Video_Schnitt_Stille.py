import moviepy.editor as mvpe
import itertools as it


def lade_video(datei):
  name, ext = datei.split('.')
  return mvpe.VideoFileClip(datei), name+'_kurz.'+ext


def gen_video(video, ab, stille):
  audio = video.audio
  a = [audio.subclip(i*ab, (i+1)*ab).max_volume() >=
       stille for i in range(int(audio.end/ab))]
  b, l = zip(*[(k, len(list(v))*ab) for k, v in it.groupby(a)])
  schnitte = [(sum(l[:i]), sum(l[:i])+l[i]) for i in range(len(l)) if b[i]]
  return mvpe.concatenate_videoclips([video.subclip(s, e) for s, e in schnitte])


video, ausgabedatei = lade_video("Teil_83_Beispiel.mp4")
video2 = gen_video(video, 0.05, 0.03)
video2.write_videofile(ausgabedatei, fps=30, preset='ultrafast', codec='libx264', threads=4,
                       audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True, )
print(f'Länge vorher/nachher = {video.end:.2f} Sek. / {video2.end:.2f} Sek.')
