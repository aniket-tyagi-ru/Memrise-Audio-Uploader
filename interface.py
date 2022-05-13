from tkinter import *
import uploader

def run_uploader(inputs):
    #print("Button is working")
    for a in range(len(inputs)):
        inputs[a] = inputs[a].get()
    uploader.main(inputs)

def launch_app():
    def assign_item_rows(items):
        row = 0
        for item in items:
            # item.grid_forget()
            item.grid(row = row, column = 0)
            if str(type(item)) == "<class 'tkinter.Label'>":
                item.grid(sticky = W)
            elif str(type(item)) == "<class 'tkinter.Button'>":
                item.grid(pady = (12, 2))
            row += 1

    def items_to_inputs(items):
        list = []
        for item in items:
            if str(type(item)) == "<class 'tkinter.Entry'>":
                list.append(item)
        return list

    main = Tk()
    main.title("Memrise Audio Uploader")
    # main.geometry("515x640")
    main.resizable(width = False, height = False)

    header = Frame(main)
    header.pack(side = TOP)
    img = PhotoImage(file = "mem_header.gif")
    mem_header = Canvas(header, width = 512, height = 288, bd = 0, relief='ridge')
    mem_header.create_image(0,0,anchor = "nw", image = img)
    mem_header.grid(row=0, columnspan = 3)

    footer = Frame(main, height = 20)
    footer.pack(side = BOTTOM)
    l_frame = Frame(main, width = 160)
    l_frame.pack(side = LEFT)
    m_frame = Frame(main,)
    m_frame.pack(side = LEFT)
    r_frame = Frame(main, width = 158)
    r_frame.pack(side = RIGHT)

    items = []
    el_user = Label(m_frame, text = "Cookie")
    ef_user = Entry(m_frame)
    items.append(el_user), items.append(ef_user)
    el_url = Label(m_frame, text = "Database URL")
    ef_url = Entry(m_frame)
    items.append(el_url), items.append(ef_url)
    el_lang = Label(m_frame, text = "Language Column Name")
    ef_lang = Entry(m_frame)
    items.append(el_lang), items.append(ef_lang)
    el_aud = Label(m_frame, text = "Audio Column Name")
    ef_aud = Entry(m_frame)
    items.append(el_aud), items.append(ef_aud)
    btn = Button(m_frame, text = "Start", width = '12', height = '2',
                    command = lambda: [main.withdraw(), run_uploader(inputs)])
    items.append(btn)
    assign_item_rows(items)
    inputs = items_to_inputs(items)

    main.mainloop()

launch_app()
