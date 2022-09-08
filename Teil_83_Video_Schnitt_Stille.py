# Based on a script by Donald Feury
# https://gitlab.com/dak425/scripts/-/blob/master/trim_silenceV2


import moviepy.editor as mvpe


def finde_sprache(audio, abschnitt, min_lautst):
  schnittliste, start = [], -1
  for i in range(int(audio.end/abschnitt)):
    s = audio.subclip(i * abschnitt, (i + 1) * abschnitt)
    if s.max_volume() >= min_lautst and start == -1:
      start = i*abschnitt
    elif s.max_volume() < min_lautst and start != -1:
      schnittliste.append([start, i*abschnitt])
      start = -1
  if start != -1:
    schnittliste.append([start, i*abschnitt])  
  return schnittliste


file_in = "y:\\Videos\\OBS Studio\\adventOfCode\\2022-09-05 18-49-31.mp4"
file_out = "y:\\Videos\\OBS Studio\\adventOfCode\\test.mp4"
video = mvpe.VideoFileClip(file_in)

schnittliste = finde_sprache(video.audio,0.1,0.03)
länge = sum(b-a for a,b in schnittliste)

print(f'Videolänge vor dem Schnitt : {video.end//60:.0f}:{video.end%60:.0f}')
print(f'Videolänge nach dem Schnitt: {länge//60:.0f}:{länge%60:.0f}')
print(f'Einträge in Schnittliste   : {len(schnittliste)}')

print(f'Start Zusammenstellung')
sprach_clips = [video.subclip(s, e) for s,e in schnittliste]
edited_video = mvpe.concatenate_videoclips(sprach_clips)
print(f'Start Ausgabe')
edited_video.write_videofile(file_out,
                            fps=30,
                            preset='ultrafast',
                            codec='libx264',
                            temp_audiofile='temp-audio.m4a',
                            remove_temp=True,
                            audio_codec="aac",
                            threads=8
                            )

video.close()