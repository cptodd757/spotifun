import numpy as np 
import matplotlib.pyplot as plt 
import json

pitch_names = ["C","C#/Db","D","D#/Eb","E","F","F#/Gb","G","G#/Ab","A","A#/Bb","B"]

def visualize_segments(segments):
    times = np.array([])
    pitches = np.array([])
    pitch_strengths = np.array([])
    #segments = json.loads(response)["segments"]
    for segment in segments:
        #print(segment)
        #n = 3
        #idea: only show pitches above a certain threshold
        #top_pitches = np.flip(np.argsort(segment["pitches"]))[:3]
        #top_pitches_strengths = [segment["pitches"][i] for i in top_pitches]
        threshold = .4
        p = np.array(segment["pitches"])
        top_pitches = np.argwhere(p > threshold).flatten()
        top_pitches_strengths = p[top_pitches]
        print(p,top_pitches,top_pitches_strengths)
        #break

        n = len(top_pitches)
        time = segment["start"]

        lower = 60
        upper = 80
        if time < lower:
            continue
        if time > upper:
            break

        pitches = np.append(pitches,top_pitches)
        pitch_strengths = np.append(pitch_strengths,top_pitches_strengths)
        for i in range(n):
            times = np.append(times,time)

    print(len(times),len(pitches))

    plt.scatter(times,pitches,marker="s",s=100,c=pitch_strengths, cmap='Purples')
    plt.yticks(range(12), pitch_names)
    plt.show()

name = 'wagner'
with open('data/{}.json'.format(name)) as f:
  obladi = json.load(f)
print(obladi["track"]["duration"])
visualize_segments(obladi["segments"])
