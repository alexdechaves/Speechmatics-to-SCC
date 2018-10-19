import json
import datetime
import subprocess
import os
import time
import shutil
import threading


python_path = "C:\\Users\\alex.dechaves\\AppData\\Local\\Continuum\\anaconda3\\python.exe"


def transcribe(audio_file):
    subprocess.call(python_path + ' speechmatics.py -a ' + audio_file +
                    ' -l en-US -i 24361 -k YmU3NjQwMmYtZDFkMC00MzI5LWI3Y2UtMTU1ZjQwOWMzMDVk -o ' + audio_file[:-4]
                    + 'json')


def seconds_to_timecode(number):
    return str(datetime.timedelta(seconds=int(float(number))))


def json_to_srt(transcript):
    try:
        with open(transcript, encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            json_captions = []
            json_time = []
            try:
                for word in json_data["words"]:
                    if word not in json_captions:
                        json_captions.append(word["name"])
                        json_time.append(word["time"])
            except ValueError:
                print("Error! Bad data from JSON!")
    except OSError:
        print("Error opening transcript...")
    lst2 = []
    n = 0
    try:
        for i in range(0, len(json_captions) - len(json_captions) % 5, 5):
            n += 1
            lst2.append(str(n) + "\n0" + seconds_to_timecode(json_time[i]) + ",000 --> 0"
                        + seconds_to_timecode(float(json_time[i+4])) + ",000\n"
                        + json_captions[i] + " " + json_captions[i+1] + " " + json_captions[i+2] + " "
                        + json_captions[i+3] + " " + json_captions[i+4] + '\n')
    except ValueError:
        print("Error computing captions from transcript...")
    try:
        n = int((len(json_captions) - len(json_captions) % 5)/5)
        for a in range(len(json_captions) - len(json_captions) % 5, len(json_captions)):
            n += 1
            lst2.append(str(n) + "\n0" + seconds_to_timecode(json_time[a]) + ",000 --> 0"
                        + seconds_to_timecode(float(json_time[a])) + ",000\n"
                        + json_captions[a] + "\n")
    except ValueError:
        print("Error computing captions from transcript...")

    with open(transcript[:-4] + 'srt', "w") as srt_file:
        srt_file.write("\n".join(lst2))


def srt_to_scc(transcript):
    subprocess.call('SubtitleEdit /convert "' + transcript + '" "Scenarist Closed Captions"')


def main(file, complete):
    file = file.replace('"', '')
    transcribe('"' + file + '"')
    json_to_srt(file[:-4] + '.json')
    srt_to_scc(file[:-4] + '.srt')
    os.remove(file[:-4] + '.json')
    os.remove(file[:-4] + '.srt')
    shutil.move(file, complete)
    shutil.move(file[:-4] + '.scc', complete + '.scc')


def main_thread(file, complete):
    t1 = threading.Thread(target=lambda: main(file, complete))
    t1.start()


def config_folder(folder):  # function to create watch folder structure if one is not present
    if os.path.exists(folder):  # if folders exists, then do nothing
        if os.path.exists(folder + "\\INPUT\\"):
            if os.path.exists(folder + "\\INPUT\\COMPLETE\\"):
                return folder
            else:
                os.makedirs(folder + "\\INPUT\\COMPLETE\\")
                os.makedirs(folder + "\\OUTPUT\\")
        else:
            os.makedirs(folder + "\\INPUT\\")
            os.makedirs(folder + "\\INPUT\\COMPLETE\\")
    else:  # create folders when they're not present
        try:
            os.makedirs(folder)
            os.makedirs(folder + "\\INPUT\\")
            os.makedirs(folder + "\\INPUT\\COMPLETE\\")
        except IndexError:
            print("Error creating folders")


def main_watch(watch_root):
    config_folder(watch_root)
    path_to_watch = watch_root + "\\INPUT\\"
    before = dict([(f, None) for f in os.listdir(path_to_watch)])
    while True:  # Main watch loop
        time.sleep(5)  # checking interval
        print("Folder checked at " + str(
            os.listdir(path_to_watch)))  # Prints the action of checking the folder
        after = dict([(f, None) for f in os.listdir(path_to_watch)])  # List generation for watch folder core
        added = [f for f in after if f not in before]
        removed = [f for f in before if f not in after]
        if added:
            print("Added: ", ", ".join(added))
            for i in added:
                if ".mov" in i or ".mp4" in i:
                    main_thread(path_to_watch + i, watch_root + '\\INPUT\\COMPLETE\\' + i)
        if removed:
            print("Removed: ", ", ".join(removed))
        before = after

