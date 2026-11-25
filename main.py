
import tkinter as tk
import threading
import time
import random

# ==================================
# 1. Main Configuration
# ==================================

BUFFER_SIZE = 5
buffer = []

# Real semaphores
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)
mutex = threading.Semaphore(1)

item_number = 0
running = False
after_id = None
process_index = 0

# ==================================
# 2. Main Window
# ==================================

root = tk.Tk()
root.title("Operating System II - Concurrency Visualizer")
root.geometry("1200x950")
root.state("zoomed")
root.configure(bg="#eaf0ff")

# ==================================
# 3. Process Names
# ==================================

producer_names = ["Producer 1", "Producer 2"]
consumer_names = ["Consumer 1", "Consumer 2"]

process_names = producer_names + consumer_names

status_labels = {}

# ==================================
# 4. Title
# ==================================

title = tk.Label(
    root,
    text="Producer - Consumer Simulation",
    font=("Arial", 23, "bold"),
    bg="#263f80",
    fg="white",
    pady=15
)
title.pack(fill="x", padx=10, pady=10)

# ==================================
# 5. Control Buttons
# ==================================

controls = tk.Frame(root, bg="#eaf0ff")
controls.pack(pady=10)

# ==================================
# Speed Control
# ==================================

speed_frame = tk.LabelFrame(
    root,
    text="Process Speed Control",
    font=("Arial", 14, "bold"),
    bg="#eaf0ff",
    padx=20,
    pady=10
)
speed_frame.pack(pady=10)

producer_speed = tk.Scale(
    speed_frame,
    from_=200,
    to=2000,
    orient="horizontal",
    label="Producer Speed (ms)",
    length=300,
    bg="#eaf0ff"
)
producer_speed.set(600)
producer_speed.grid(row=0, column=0, padx=20)

consumer_speed = tk.Scale(
    speed_frame,
    from_=200,
    to=2000,
    orient="horizontal",
    label="Consumer Speed (ms)",
    length=300,
    bg="#eaf0ff"
)
consumer_speed.set(600)
consumer_speed.grid(row=0, column=1, padx=20)

# ==================================
# 6. Process Status
# ==================================

status_frame = tk.LabelFrame(
    root,
    text="Process Status",
    font=("Arial", 14, "bold"),
    bg="#eaf0ff",
    padx=15,
    pady=10
)
status_frame.pack(fill="x", padx=20, pady=10)

for i, name in enumerate(process_names):
    label = tk.Label(
        status_frame,
        text=name + ": Waiting",
        font=("Arial", 12, "bold"),
        bg="#fff0bd",
        fg="#9a6500",
        width=22,
        pady=10
    )
    label.grid(row=0, column=i, padx=10, pady=5)
    status_labels[name] = label


# ==================================
# 7. Buffer Display
# ==================================

buffer_frame = tk.LabelFrame(
    root,
    text="Shared Buffer (Size = 5)",
    font=("Arial", 14, "bold"),
    bg="#eaf0ff",
    padx=15,
    pady=5,
)
buffer_frame.pack(fill="x", padx=20, pady=3)

slots = []

for i in range(BUFFER_SIZE):
    slot = tk.Label(
        buffer_frame,
        text="Empty",
        font=("Arial", 12, "bold"),
        bg="white",
        relief="solid",
        width=15,
        height=4
    )
    slot.grid(row=0, column=i, padx=10, pady=10)
    slots.append(slot)

info = tk.Label(
    buffer_frame,
    text="Empty: 5 | Full: 0",
    font=("Arial", 12, "bold"),
    bg="#eaf0ff"
)
info.grid(row=1, column=0, columnspan=5, pady=10)


# ==================================
# 8. Chatbot Interface
# ==================================

assistant_frame = tk.LabelFrame(
    root,
    text="Operating System Assistant",
    font=("Arial", 14, "bold"),
    bg="#eaf0ff",
    padx=10,
    pady=10
)
assistant_frame.pack(fill="both", expand=True, padx=20, pady=3)

chat_display = tk.Text(
    assistant_frame,
    height=4,
    font=("Arial", 11),
    wrap="word",
    state="disabled"
)
chat_display.pack(fill="both", expand=True, padx=5, pady=5)

chat_input_frame = tk.Frame(
    assistant_frame,
    bg="#eaf0ff"
)
chat_input_frame.pack(fill="x", pady=5)

chat_entry = tk.Entry(
    chat_input_frame,
    font=("Arial", 12),
    state="normal",
    bg="white",
    fg="black",
    insertbackground="black"
)
chat_entry.pack(side="left", fill="x", expand=True, padx=5)


# ==================================
# 9. Chatbot Functions
# ==================================

def add_chat_message(sender, message):

    chat_display.config(state="normal")

    chat_display.insert(
        tk.END,
        sender + ": " + message + "\n\n"
    )

    chat_display.see(tk.END)
    chat_display.config(state="disabled")


def assistant_response(message):

    global producer_speed, consumer_speed

    text = message.lower()

    if "producer" in text and ("faster" in text or "speed up" in text):
        producer_speed.set(max(200, producer_speed.get() - 200))
        return "Producer speed increased."

    if "producer" in text and ("slower" in text or "slow" in text):
        producer_speed.set(min(2000, producer_speed.get() + 200))
        return "Producer speed decreased."

    if "consumer" in text and ("faster" in text or "speed up" in text):
        consumer_speed.set(max(200, consumer_speed.get() - 200))
        return "Consumer speed increased."

    if "consumer" in text and ("slower" in text or "slow" in text):
        consumer_speed.set(min(2000, consumer_speed.get() + 200))
        return "Consumer speed decreased."

    if "semaphore" in text:
        return "A semaphore is a synchronization tool used to control access to shared resources."

    if "mutex" in text:
        return "Mutex allows only one process or thread to access a critical section at a time."

    if "buffer" in text:
        return "The buffer is a shared memory area where produced items are stored before consumption."

    if "producer" in text:
        return "The Producer creates items and puts them into the shared buffer."

    if "consumer" in text:
        return "The Consumer removes items from the shared buffer."

    if "critical section" in text:
        return "The critical section is the part of the program that accesses shared data."

    if "synchronization" in text:
        return "Synchronization coordinates processes to prevent conflicts when sharing resources."

    return "I can explain Producer, Consumer, Buffer, Semaphore, Mutex and Synchronization."



# ==================================
# 10. Send Chatbot Message
# ==================================

def send_message():

    message = chat_entry.get().strip()

    if not message:
        return

    add_chat_message("You", message)

    chat_entry.delete(0, tk.END)

    response = assistant_response(message)

    add_chat_message("Assistant", response)


send_button = tk.Button(
    chat_input_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    bg="#263f80",
    fg="white",
    command=send_message
)
send_button.pack(side="right", padx=5)

chat_entry.bind("<Return>", lambda event: send_message())


# ==================================
# 11. Update Buffer Display
# ==================================

def update_buffer_display():

    for i in range(BUFFER_SIZE):

        if i < len(buffer):
            slots[i].config(
                text=str(buffer[i]),
                bg="#b9e7c4",
                fg="#155724"
            )

        else:
            slots[i].config(
                text="Empty",
                bg="white",
                fg="black"
            )

    info.config(
        text="Empty: " + str(BUFFER_SIZE - len(buffer)) +
             " | Full: " + str(len(buffer))
    )


# ==================================
# 12. Update Process Status
# ==================================

def update_status(name, status):

    if status == "Running":
        status_labels[name].config(
            text=name + ": Running",
            bg="#b9e7c4",
            fg="#155724"
        )

    elif status == "Waiting":
        status_labels[name].config(
            text=name + ": Waiting",
            bg="#fff0bd",
            fg="#9a6500"
        )

    elif status == "Blocked":
        status_labels[name].config(
            text=name + ": Blocked",
            bg="#f5b7b1",
            fg="#922b21"
        )


# ==================================
# 13. Simulation Log
# ==================================

log_frame = tk.LabelFrame(
    root,
    text="Simulation Log",
    font=("Arial", 14, "bold"),
    bg="#eaf0ff",
    padx=10,
    pady=10
)
log_frame.pack(fill="both", expand=True, padx=20, pady=10)

log_display = tk.Text(
    log_frame,
    height=7,
    font=("Consolas", 10),
    state="disabled"
)
log_display.pack(fill="both", expand=True)


def add_log(message):

    log_display.config(state="normal")

    log_display.insert(
        tk.END,
        message + "\n"
    )

    log_display.see(tk.END)
    log_display.config(state="disabled")



# ==================================
# 14. Producer Function
# ==================================

def produce_item(name):

    global item_number

    if len(buffer) >= BUFFER_SIZE:
        update_status(name, "Blocked")
        add_log(name + " is waiting: Buffer is full.")
        return

    update_status(name, "Running")

    item_number += 1
    item = item_number

    buffer.append(item)

    update_buffer_display()

    add_log(name + " produced item " + str(item))

    update_status(name, "Waiting")


# ==================================
# 15. Consumer Function
# ==================================

def consume_item(name):

    if len(buffer) == 0:
        update_status(name, "Blocked")
        add_log(name + " is waiting: Buffer is empty.")
        return

    update_status(name, "Running")

    item = buffer.pop(0)

    update_buffer_display()

    add_log(name + " consumed item " + str(item))

    update_status(name, "Waiting")


# ==================================
# 16. Execute Process
# ==================================

def execute_process(name):

    if name in producer_names:
        produce_item(name)

    elif name in consumer_names:
        consume_item(name)


# ==================================
# 17. Step Forward
# ==================================

def step_forward():

    global process_index

    name = process_names[process_index]

    execute_process(name)

    process_index = (process_index + 1) % len(process_names)



# ==================================
# 18. Run Simulation
# ==================================

def run_simulation():

    global after_id

    if not running:
        return

    name = process_names[process_index]

    step_forward()

    if name in producer_names:
        delay = producer_speed.get()
    else:
        delay = consumer_speed.get()

    after_id = root.after(delay, run_simulation)


# ==================================
# 19. Play
# ==================================

def play():

    global running

    if running:
        return

    running = True

    add_log("Simulation started.")

    run_simulation()


# ==================================
# 20. Pause
# ==================================

def pause():

    global running, after_id

    running = False

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    add_log("Simulation paused.")


# ==================================
# 21. Control Buttons
# ==================================

play_button = tk.Button(
    controls,
    text="▶ Play",
    font=("Arial", 12, "bold"),
    bg="#28a745",
    fg="white",
    width=15,
    command=play
)
play_button.grid(row=0, column=0, padx=10)

pause_button = tk.Button(
    controls,
    text="⏸ Pause",
    font=("Arial", 12, "bold"),
    bg="#dc3545",
    fg="white",
    width=15,
    command=pause
)
pause_button.grid(row=0, column=1, padx=10)

step_button = tk.Button(
    controls,
    text="⏭ Step Forward",
    font=("Arial", 12, "bold"),
    bg="#007bff",
    fg="white",
    width=15,
    command=step_forward
)
step_button.grid(row=0, column=2, padx=10)



# ==================================
# 22. Reset Simulation
# ==================================

def reset_simulation():

    global running, after_id, process_index, item_number

    pause()

    buffer.clear()

    item_number = 0
    process_index = 0

    update_buffer_display()

    for name in process_names:
        update_status(name, "Waiting")

    add_log("Simulation has been reset.")


# ==================================
# 23. Reset Button
# ==================================

reset_button = tk.Button(
    controls,
    text="↻ Reset",
    font=("Arial", 12, "bold"),
    bg="#6c757d",
    fg="white",
    width=15,
    command=reset_simulation
)
reset_button.grid(row=0, column=3, padx=10)


# ==================================
# 24. Initial Setup
# ==================================

update_buffer_display()

add_chat_message(
    "Assistant",
    "Hello! I am your Operating System Assistant. Ask me about Producer, Consumer, Buffer, Semaphore or Mutex."
)

add_log("Simulation is ready.")


# ==================================
# 25. Start Application
# ==================================

root.mainloop()
