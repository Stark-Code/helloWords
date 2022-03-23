from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import requests


class Game_Mode_Interface:
    def __init__(self, parent, start_Game_Func):
        self.parent = parent
        self.start_Game = start_Game_Func
        self.single_Player_Btn = None
        self.multi_Player_Btn = None
        self.image = None
        self.room_Viewer_Tree = None
        self.name_List_Database_Viewer = []
        self.join_Btn = None
        self.selected_Room = None
        self.selected_Room_Item = None
        self.lobby = None
        self.refresh_Timer = None

    def populate_Room_Data(self):
        print('Populating Room Data')
        r = requests.get('http://127.0.0.1:5000/room_Registry', json={})

        if r.ok:
            for child in self.room_Viewer_Tree.get_children():
                self.room_Viewer_Tree.delete(child)

            # room_ID = self.room_Viewer_Tree.identify_row(self.selected_Room)
            # # self.room_Viewer_Tree.selection_set(room_ID)
            # self.room_Viewer_Tree.selection_set(room_ID)

        # if self.selected_Room_Item:
        #     self.room_Viewer_Tree.focus_set(0)

        # print(r)
        # print(r.json())
        # print(r.json()['Search Results:'])

        for room_Idx, room in enumerate(r.json()['Search Results:']):
            self.name_List_Database_Viewer.append(room['name'])  # Maybe move this?
            contact = (room["name"].capitalize(), room["population"], room["status"])
            self.room_Viewer_Tree.insert('', 'end', values=contact)

        if self.selected_Room is not None:
            child_id = self.room_Viewer_Tree.get_children()[self.selected_Room]
            self.room_Viewer_Tree.focus(child_id)
            self.room_Viewer_Tree.selection_set(child_id)

    def refresh_Room_Data(self):
        self.populate_Room_Data()
        self.refresh_Timer = self.parent.canvas.after(1000, self.refresh_Room_Data)
        # self.parent.after_cancel(self.time_Label_Timer_ID)

    def get_Room_Selection(self, event):
        self.selected_Room = event.widget.index(event.widget.focus())  # Index
        self.selected_Room_Item = event.widget.focus()
        self.join_Btn.config(state='normal')

    def join_Room(self):
        print(f'Selected Room Index: {self.selected_Room}')
        payload = self.name_List_Database_Viewer[self.selected_Room]  # List[index]
        print(f'join room payload {payload}')         # print(f'Join Room Response: {r.text}')
        r = requests.put('http://127.0.0.1:5000/room_Registry', json={'name': payload})
        print(f'Join Room Response: {r.text}')
        if r.json()['population'] > 1:  # Change Later
            self.parent.canvas.after_cancel(self.refresh_Timer)
            self.lobby.destroy()
            self.start_Game(self.parent, 'multi', r.json()['name'], player_ID='Unique ID for player loading game')
        else:
            self.populate_Room_Data()

    def init_Room_Select(self):
        self.lobby = Toplevel()
        self.lobby.geometry('500x275')
        window_Frame = LabelFrame(self.lobby, relief="groove")
        window_Frame.grid()
        columns = ('#1', '#2', '#3')
        self.room_Viewer_Tree = ttk.Treeview(window_Frame, columns=columns, show='headings')
        self.room_Viewer_Tree.name = 'database_Viewer'
        self.room_Viewer_Tree.grid(row=1, column=1, sticky=(N, S))
        self.room_Viewer_Tree.grid_configure(padx=5, pady=2)
        self.room_Viewer_Tree.bind('<<TreeviewSelect>>', self.get_Room_Selection)
        self.room_Viewer_Tree.heading('#1', text='Room')
        self.room_Viewer_Tree.column('#1', width=125, anchor='center')
        self.room_Viewer_Tree.heading('#2', text='Population')
        self.room_Viewer_Tree.column('#2', width=125, anchor='center')
        self.room_Viewer_Tree.heading('#3', text='Status')
        self.room_Viewer_Tree.column('#3', width=225, anchor='center')

        self.join_Btn = Button(window_Frame, text="Join", highlightthickness=0, command=self.join_Room)
        self.join_Btn.grid(row=2, column=1)
        self.join_Btn.grid_configure(padx=3, pady=3)
        self.join_Btn.config(state='disabled')

    def init_Game(self, mode):
        for widget in self.parent.canvas.winfo_children():
            widget.destroy()
        if mode == 'single':
            self.start_Game(self.parent, mode, 'None')
        else:
            self.init_Room_Select()
            self.refresh_Room_Data()

    def init_Buttons(self):
        self.image = ImageTk.PhotoImage(Image.open('images/tile_Yellow.png').resize((100, 100)))

        self.single_Player_Btn = Button(self.parent.canvas, activebackground='grey', font=self.parent.canvas.tile_Font,
                                        highlightthickness=0, bg='grey', anchor='center', borderwidth=0, image=self.image,
                                        compound='center', text="1", command=lambda: self.init_Game('single'))
        self.single_Player_Btn.x = 175
        self.single_Player_Btn.y = 100
        self.single_Player_Btn.place(x=self.single_Player_Btn.x, y=self.single_Player_Btn.y)

        self.multi_Player_Btn = Button(self.parent.canvas, activebackground='grey', font=self.parent.canvas.tile_Font,
                                       highlightthickness=0, bg='grey', borderwidth=0, image=self.image,
                                       compound='center', text="2", command=lambda: self.init_Game('multi'))
        self.multi_Player_Btn.x = 425
        self.multi_Player_Btn.y = 100
        self.multi_Player_Btn.place(x=self.multi_Player_Btn.x, y=self.multi_Player_Btn.y)

    def init_Labels(self):
        single_Player_Label = Label(self.parent.canvas, bg='grey', font=self.parent.canvas.tile_Font,
                                    anchor='center', text="Single Player")
        multi_Player_Label = Label(self.parent.canvas, bg='grey', font=self.parent.canvas.tile_Font, text="Multiplayer")
        single_Player_Label.place(x=self.single_Player_Btn.x - 50, y=self.single_Player_Btn.y + 125)
        multi_Player_Label.place(x=self.multi_Player_Btn.x - 25, y=self.multi_Player_Btn.y + 125)
