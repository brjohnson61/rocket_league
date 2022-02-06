from pynput.keyboard import Key, Controller, Events, KeyCode
import tkinter
from tkinter import ttk
import threading
import os
import time

window_title = "RL Chat Bot"

chat_entry_default_text = [
    "Custom chat one", # chat 0
    "Custom chat two", # chat 1
    "Custom chat three", # chat 2
    "Custom chat four", # chat 3
    "Custom chat five", # chat 4
    "Custom chat six", # chat 5
    "Custom chat seven", # chat 6
    "Custom chat eight", # chat 7
    "Custom chat nine", # chat 8
    "Custom chat ten", # chat 9
]

chat_labels = [
    "Quick chat on Number '0'", # label 0
    "Quick chat on Number '1'", # label 1
    "Quick chat on Number '2'", # label 2
    "Quick chat on Number '3'", # label 3
    "Quick chat on Number '4'", # label 4
    "Quick chat on Number '5'", # label 5
    "Quick chat on Number '6'", # label 6
    "Quick chat on Number '7'", # label 7
    "Quick chat on Number '8'", # label 8
    "Quick chat on Number '9'", # label 9
]

key_translation = {
    KeyCode(char='0'): 0,
    KeyCode(char='1'): 1,
    KeyCode(char='2'): 2,
    KeyCode(char='3'): 3,
    KeyCode(char='4'): 4,
    KeyCode(char='5'): 5,
    KeyCode(char='6'): 6,
    KeyCode(char='7'): 7,
    KeyCode(char='8'): 8,
    KeyCode(char='9'): 9,
}

chat_entry_text_vars = []

chat_entry_objects = []

buttons = {}

misc_labels = {}

misc_text_vars = {}

NUM_CHAT_ENTRIES = 10

service_is_running = False
program_is_running = True

service_thread = None

rocket_league_save_filename = "rl_chat_save_files/save_file.rlchat"


#
# 
# set_status_message(message)
# 
#
def set_status_message(message):
    misc_text_vars['status_display'].set(message)


#
# 
# callback_start_stop_toggle()
# 
#
def callback_start_stop_toggle():
    global service_is_running
    current_state = misc_text_vars['start_stop_toggle'].get()

    if current_state == "Start":
        set_status_message("Running Service")
        service_is_running = True
        misc_text_vars['start_stop_toggle'].set("Stop")
    elif current_state == "Stop":
        set_status_message("Stopping Service")
        service_is_running = False
        misc_text_vars['start_stop_toggle'].set("Start")


#
# 
# callback_save_button()
# 
#
def callback_save_button():
    set_status_message("Saving...")
    if not os.path.isdir("rl_chat_save_files"):
        os.mkdir("rl_chat_save_files")
    try:
        with open(rocket_league_save_filename, 'w+') as save_file:
            for line_num in range(NUM_CHAT_ENTRIES):
                line_to_output = chat_entry_text_vars[line_num].get()
                save_file.write(line_to_output)
                save_file.write('\n')
        set_status_message("Saved!")
    except IOError:
        set_status_message("Cannot save!")

#
# 
# callback_load_button()
# 
#
def callback_load_button():
    set_status_message("Loading...")
    try:
        with open(rocket_league_save_filename, 'r') as save_file:
            line_count = 0
            for line in save_file:
                if line_count < NUM_CHAT_ENTRIES:
                    chat_entry_text_vars[line_count].set(line.strip())
                    line_count += 1
        set_status_message("Loaded!")
    except IOError:
        set_status_message("Save not found!")


#
# 
# set_initial_window_properties()
# 
#
def set_initial_window_properties():
    window = tkinter.Tk(screenName="screenName",
                        baseName="baseName",
                        useTk=True)

    window.title(window_title)
    window.geometry("250x450")
    window.iconbitmap('rocketleague.ico')

    frame = ttk.Frame(window, padding=10)
    frame.grid()

    return window, frame

#
# 
# handle_key_event(key)
# 
#
def output_string_to_rocket_league_chat(chat_output, keyboard):
    keyboard.press(KeyCode(char='t'))
    keyboard.release(KeyCode(char='t'))

    time.sleep(0.015)
    for key_char in chat_output:
        send_shift = False
        if key_char.isupper():
            send_shift = True
            entry_char = key_char.lower()
        else:
            entry_char = key_char
        
        if send_shift:
            keyboard.press(Key.shift)
            

        keyboard.press(KeyCode(char=entry_char))
        keyboard.release(KeyCode(char=entry_char))

        if send_shift:
            keyboard.release(Key.shift)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

#
# 
# handle_key_event(key)
# 
#
def handle_key_event(key, keyboard):
    if key in key_translation:
        key_index = key_translation[key]
        chat_output = chat_entry_text_vars[key_index].get()
        output_string_to_rocket_league_chat(chat_output, keyboard)
        

    
#
# 
# start_service_process()
# 
#
def start_service_process():
    global service_thread

    service_thread = threading.Thread(target=service, args=())
    service_thread.start()

#
# 
# kill_service_process()
# 
#
def kill_service_process():
    global service_thread
    global program_is_running
    global service_is_running

    service_is_running = False
    program_is_running = False
    
    service_thread.join()


#
# 
# create_chat_labels(frame)
# 
#
def create_chat_labels(frame):
    for chat_position in range(NUM_CHAT_ENTRIES):
        # Create chat entry labels (Quick chat on Number '0', etc.)
        label = ttk.Label(frame, text=chat_labels[chat_position])
        label.grid(column=0, row=(2*chat_position))


#
# 
# create_chat_entries(frame)
# 
#
def create_chat_entries(frame):
    for chat_position in range(NUM_CHAT_ENTRIES):
        # Create and set new persistent text variable
        chat_entry_text_vars.append(tkinter.StringVar())
        chat_entry_text_vars[chat_position].set(chat_entry_default_text[chat_position])

        # Create Entry and save reference to widget containing custom chat text
        entry = ttk.Entry(frame,
                          textvariable=chat_entry_text_vars[chat_position])
        entry.grid(column=0, row=((2*chat_position)+1))
        chat_entry_objects.append(entry)


#
# 
# create_chat_labels_and_entries(frame)
# 
#
def create_chat_labels_and_entries(frame):
    create_chat_labels(frame)
    create_chat_entries(frame)


#
# 
# create_status_message_display(frame)
# 
#
def create_status_message_display(frame):
    # Create status display text value and save reference to it in 'misc' dictionary
    misc_text_vars['status_display'] = tkinter.StringVar()
    misc_text_vars['status_display'].set("")

    # Create display label
    misc_labels['status_display'] = ttk.Label(frame,
                                              textvariable=misc_text_vars['status_display'])
    misc_labels['status_display'].grid(column=1, row=20)

    # Create 'Status: ' text label to the left of the display area
    misc_labels['status_label'] = ttk.Label(frame, text="Status:")
    misc_labels['status_label'].grid(column=0, row=20)


#
# 
# create_save_file_button(frame)
# 
#
def create_save_file_button(frame):
    # Create Save button and save reference in dictionary
    buttons['save_button'] = ttk.Button(frame,
                                        text="Save Chats",
                                        command=callback_save_button)
    buttons['save_button'].grid(column=1, row=2)


#
# 
# create_load_file_button(frame)
# 
#
def create_load_file_button(frame):
    # Create and save reference to Load button
    buttons['load_button'] = ttk.Button(frame,
                                        text="Load Chats",
                                        command=callback_load_button)
    buttons['load_button'].grid(column=1, row=4)

#
# 
# create_start_stop_toggle_button(frame)
# 
#
def create_start_stop_toggle_button(frame):
    # Create persistent string variable for Start/Stop text
    misc_text_vars['start_stop_toggle'] = tkinter.StringVar()
    misc_text_vars['start_stop_toggle'].set("Start")

    # Create persistent reference to Button and Button itself for Start/Stop
    buttons['start_stop_toggle'] = ttk.Button(frame, 
                                              textvariable=misc_text_vars['start_stop_toggle'],
                                              command=callback_start_stop_toggle)
    buttons['start_stop_toggle'].grid(column=1, row=6)

#
# 
# service(is_running)
# 
#
def service():
    keyboard = Controller()

    while(program_is_running):
        while (service_is_running):
            with Events() as events:
                # Block at most .1 second between getting events
                event = events.get(0.1)

                if event is not None and event.__class__.__name__ == "Press":
                    handle_key_event(event.key, keyboard)


def main():
    # Create top level widgets
    window, frame = set_initial_window_properties()

    # Create chat labels and text entries
    create_chat_labels_and_entries(frame)

    # Create save file button
    create_save_file_button(frame)

    # Create load file button
    create_load_file_button(frame)

    # Create start stop toggle button
    create_start_stop_toggle_button(frame)

    # Create 'Status' display
    create_status_message_display(frame)

    # Start 'service thread' that listens for keypress events
    start_service_process()
 
    # Start application main loop
    window.mainloop()

    # Kill service thread listening to keypresses
    kill_service_process()
    

if __name__ == "__main__":
    main()
