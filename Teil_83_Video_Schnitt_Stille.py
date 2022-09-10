import moviepy.editor as mvpe


def lade_video(datei):
  name, ext = datei.split('.')
  return mvpe.VideoFileClip(datei), name+'_kurz.'+ext


ab, stille = 0.05, 0.03

v1, ausgabedatei = lade_video('Teil_83_Beispiel.mp4')
clips = [v1.subclip(i*ab, (i+1)*ab) for i in range(int(v1.end/ab))
         if v1.subclip(i*ab, (i+1)*ab).audio.max_volume() >= stille]
v2 = mvpe.concatenate_videoclips(clips)
v2.write_videofile(ausgabedatei, fps=30, preset='ultrafast', codec='libx264',
                   temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac', threads=4)

print(f'Länge vorher/nacher = {v1.end:.2f} Sek. / {v2.end:.2f} Sek.')
