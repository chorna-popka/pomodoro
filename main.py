from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Verdana"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

cycle = [ ]
cur_step = 0
tracker_offset = 0
timer = None

headers = {
    WORK_MIN: [ "Work!", GREEN ],
    LONG_BREAK_MIN: [ "Rest!", RED ],
    SHORT_BREAK_MIN: [ "Rest!", PINK ],
}

for i in range(3):
    cycle.append(WORK_MIN)
    cycle.append(SHORT_BREAK_MIN)

cycle.append(WORK_MIN)
cycle.append(LONG_BREAK_MIN)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global cur_step, timer, tracker_offset
    cur_step = 0
    timer = window.after_cancel(timer)
    lbl_header.config(text="Ready?", fg=GREEN)
    canvas.itemconfig(lbl_timer, text="00:00")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global tracker_offset
    lbl_header.config(text=headers[ cycle[ cur_step ] ][ 0 ], fg=headers[ cycle[ cur_step ] ][ 1 ])
    if cur_step % 2 == 1:
        # add pomodoro img
        tracker_canvas.create_image(22, 22, image=pmd)
        tracker_offset += 50
    elif cur_step == 0:
        # remove pomodoro img
        tracker_canvas.delete("all")
        tracker_offset = 0

    count_down(cycle[ cur_step ] * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global cur_step, timer
    timer_text = "{:02d}".format(int(count / 60)) + ":" + "{:02d}".format(count % 60)
    canvas.itemconfig(lbl_timer, text=timer_text)
    if count >= 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        if cur_step < len(cycle) - 1:
            cur_step += 1
        else:
            cur_step = 0

        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=20, bg=YELLOW)

lbl_header = Label(text="Ready?", font=(FONT_NAME, 35), fg=GREEN, bg=YELLOW)
lbl_header.grid(column=1, row=0)

bg_img = PhotoImage(file="tomato.png")
canvas = Canvas(width=230, height=254, bg=YELLOW, highlightthickness=0)
canvas.create_image(116, 117, image=bg_img)
lbl_timer = canvas.create_text(116, 132, text="00:00", fill="white", font=(FONT_NAME, 30))
canvas.grid(column=1, row=1)

pmd = PhotoImage(file="mini_tomato.png")
tracker_canvas = Canvas(width=46, height=200, bg=YELLOW, highlightthickness=0)

tracker_canvas.grid(column=0, row=1)

btn_start = Button(text="Start", command=start_timer, width=10, highlightthickness=0)
btn_start.grid(column=0, row=2)
btn_reset = Button(text="Reset", command=reset_timer, width=10, highlightthickness=0)
btn_reset.grid(column=2, row=2)

window.mainloop()
