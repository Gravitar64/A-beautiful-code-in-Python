# Basiert auf folgendem Source-Code von Donald Feury
# https://gitlab.com/dak425/scripts/-/blob/master/trim_silenceV2
import moviepy.editor as mvpe
import numpy as np


def finde_sprache(audio, abschnitt, min_lautst):
  schnittliste, sprache = [], False
   
  for ts in np.arange(0, video.end, abschnitt):
    lautst = audio.subclip(ts, ts+abschnitt).max_volume()
    if lautst >= min_lautst and not sprache:
      start = ts
      sprache = True
    elif lautst < min_lautst and sprache :
      schnittliste.append([start, ts])
      sprache = False
  
  if sprache:
    schnittliste.append([start, ts])
  
  return schnittliste


def lade_datei(datei):
  name, ext = datei.split('.')
  return mvpe.VideoFileClip(datei), name+'_stille.'+ext


video, ausgabe = lade_datei(
    'y:\\Videos\\OBS Studio\\adventOfCode\\2022-09-05 18-49-31.mp4')
schnittliste = finde_sprache(video.audio, 0.05, 0.03)
länge = sum(b-a for a, b in schnittliste)

print(f'  Videolänge vor dem Schnitt  : {video.end//60:.0f}:{video.end%60:.0f}')
print(f'- Videolänge nach dem Schnitt : {länge//60:.0f}:{länge%60:.0f}')
print(f'= Einsparung in %             : {(1-länge/video.end)*100:.2f}%')
print(f'  Anz. Schnitte               : {len(schnittliste)}')

clips = [video.subclip(s, e) for s, e in schnittliste]
video = mvpe.concatenate_videoclips(clips)
video.write_videofile(ausgabe, fps=30, preset='ultrafast', codec='libx264',
                      temp_audiofile='temp-audio.m4a', remove_temp=True,
                      audio_codec="aac", threads=4)

video.close()