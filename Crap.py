from tkinter import *
import random
win = Tk()
win.geometry('1050x600')
win.title('Craps')
win.option_add('*font','tahoma 10')
win.option_add('*Button*background','lightgray')

#Frame: top (แสดงรูปภาพ)
frame_top = Frame(win)
frame_top.pack()

canvas1 = Canvas(frame_top)
canvas1.pack(side=LEFT, padx=15, pady=10)

canvas2 = Canvas(frame_top)
canvas2.pack(side=LEFT, padx=15, pady=10)

#Frame: canter (แสดงผลรวมและปุ่ม)
frame_center = Frame(win)
frame_center.pack()

sum_var = StringVar()
label_sum = Label(frame_center,textvariable=sum_var)
label_sum.pack()
point_var = StringVar(value='')
label_point = Label(frame_center, fg='gray', textvariable=point_var)
label_point.pack()

button_roll = Button(frame_center, text='Roll', command=lambda: roll())
button_roll.pack(pady=20, ipadx=30)

button_new = Button(frame_center, text='New', state=DISABLED, command=lambda: new_game())
button_new.pack(ipadx=27)

#Frame: buttom (แสดงแถบสถานะ)
frame_bottom = Frame(win)
frame_bottom.pack(side=BOTTOM, anchor=S, fill=X, expand=YES, padx=5, pady=5)

status_var = StringVar(value=' ')
label_status = Label(frame_bottom, textvariable=status_var, relief=SUNKEN)
label_status.pack(side=LEFT, fill=X, expand=YES, ipady=2)

stat_var = StringVar()
label_stat = Label(frame_bottom, textvariable=stat_var, relief=SUNKEN)
label_stat.pack(side=LEFT, ipady=2)

#global variables
_wins = 0           #จำนวนครั้งที่ชนะ
_losses = 0         #จำนวนครั้งที่แพ้
_is_first = True    #สำหรับเก็บค่าสถานะว่าเป็นการทอยครั้งแรกของแต่ละเกมหรือไม่
_point = 0          #ผลรวมของการทอยครั้งแรก กรณีที่ต้องนำไปเทียบสำหรับการทอยครั้งต่อไป

#functions
#ฟังก์ชันสำหรับการทอยแต่ละครั้ง
def roll():
    global _is_first, _point, _wins, _losses
    #สร้างเลขสุ่มให้ได้ค่าระหว่าง 1-6 สำหรับแทนหน้าลูกเต๋าทั้งสองลูก
    r1 = random.randint(1, 6)
    r2 = random.randint(1, 6)
    #นำเลขที่ได้ไปเลือกรูปภาพ ซึ่งเราตั้งชื่อภาพเป็น d1, d2, ..., d6
    #ดังนั้น จึงนำเลขที่สุ่มได้ไปต่อท้ายตัว d ให้กลายเป็นชื่อภาพได้เลย
    dice1_img = PhotoImage(file=f'd{r1}.png')
    dice2_img = PhotoImage(file=f'd{r2}.png')
    set_image(canvas1, dice1_img)
    set_image(canvas2, dice2_img)
    sum = r1 + r2   #ผลรวมของการทอยแต่ละครั้ง
    sum_var.set(f'Sum = {sum}') #แสดงผลรวมของการทอยแต่ละครั้งใน Label

    if _is_first:               #ถ้าเป็นการทอยครั้งแรกของแต่ละเกม
        if sum in [7, 11]:      #ถ้าได้ 7 หรือ 11 ถือว่าชนะ
            _wins += 1          #เพิ่มสถิติจำนวนครั้งที่ชนะ
            game_end('ชนะ')     #และจบเกม

        elif sum in [2, 3, 12]: #ถ้าได้ 2 , 3 หรือ 12 ถือว่า แพ้
            _losses += 1        #เพิ่มสถิติจำนวนที่แพ้
            game_end('แพ้')      #และจบเกม

        else:                   #ถ้ายังไม่มีการแพ้ชนะเกิดขึ้น
            _is_first = False   #เปลี่ยนสถานะว่าไม่ใช่การเล่นครั้งแรกของเกม
            _point = sum        #นำผลรวมของการทอยครั้งแรกมาเป็นค่า point
                                #เพื่อรอการเปรียบเทียบในครั้งถัดไป

            update_status('คลิก Roll เพื่อเล่นต่อไป')   #แสดงข้อความที่แถบสถานะ

    else:       #ถ้าไม่ใช่การทอยครั้งแรก ให้เปรียบเทียบดังหลักการที่กล่าวมาแล้ว
        point_var.set(f'[{_point}]')
        if sum == 7:
            _losses += 1
            game_end('แพ้')
        elif sum == _point:
            _wins += 1
            game_end('ชนะ')

def game_end(result):
    update_status(f'คุณ {result} คลิก New เพื่อเริ่มใหม่')
    update_stat()
    button_roll.config(state=DISABLED)
    button_new.config(state=NORMAL)

def set_image(canvas, img):
    canvas.config(width=img.width()+5, height=img.height()+5)
    canvas.create_image(5, 5, anchor=NW, image=img)
    canvas.image = img

def update_status(text):
    stat_var.set(text)

def update_stat():
    stat_var.set((f'ชนะ: {_wins} แพ้: {_losses}'))

#ฟังก์ชันสำหรับรีเชตค่าต่างๆ เพื่อเข้าสู่ขั้นตอนการเริ่มเกมใหม่
def new_game():
    global _is_first, _point
    _point = 0
    _is_first = True
    sum_var.set('')
    point_var.set('')
    dice0_img = PhotoImage(file='d0.png')
    set_image(canvas1, dice0_img)
    set_image(canvas2, dice0_img)
    button_roll.config(state=NORMAL)
    button_new.config(state=DISABLED)
    status_var.set('คลิก Roll เพื่อเล่นตัอไป')

#เริ่มต้นครั้งแรก
new_game()
update_stat()

mainloop()