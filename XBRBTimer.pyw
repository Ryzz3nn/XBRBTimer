import PySimpleGUI as sg
import json
import keyboard
import requests
import os
import time

# ----- Setting up the directory -----
home_dir = os.path.expanduser("~")
documents_path = os.path.join(home_dir, "Documents")
target_dir = os.path.join(documents_path, "Ryzz3nn", "BRBTimer")
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
# ---------------------------------------------------------------

CURRENT_VERSION = "v1.0"
GITHUB_REPO_API_URL = "https://api.github.com/repos/razzeking/BRBTimer/releases/latest"

sg.theme('DarkBrown4')

timer_running = False
start_time = None
duration = 0

def check_for_updates():
    try:
        response = requests.get(GITHUB_REPO_API_URL)
        response.raise_for_status()

        latest_release = response.json()
        latest_version = latest_release['tag_name']

        if latest_version > CURRENT_VERSION:
            return True, latest_version
        else:
            return False, None
    except requests.RequestException:
        return False, None

def format_time(seconds):
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

layout = [
    [sg.Text("BRB Timer", font=("bahnschrift Condensed", 24), justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Text("Timer", font=("bahnschrift Condensed", 20), justification='left')],
    [sg.Text("00:00", size=(5, 1), key='-TIMER-', font=("bahnschrift Condensed", 14))],
    [sg.Button("Start", key="-START-"), sg.Button("Reset", key="-RESET-")]
]

window = sg.Window("BRBTimer • {}".format(CURRENT_VERSION), layout, finalize=True, resizable=True)

while True:
    event, values = window.read(timeout=100)

    if timer_running:
        elapsed_time = time.time() - start_time
        window['-TIMER-'].update(format_time(int(elapsed_time)))

    if event == sg.WIN_CLOSED:
        break
    elif event == "-START-":
        if not timer_running:
            start_time = time.time()
            timer_running = True
            window["-START-"].update(text="Pause")
        else:
            timer_running = False
            duration += time.time() - start_time
            window["-START-"].update(text="Start")
    elif event == "-RESET-":
        timer_running = False
        start_time = None
        duration = 0
        window["-START-"].update(text="Start")
        window['-TIMER-'].update("00:00")

window.close()
