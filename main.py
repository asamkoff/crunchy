# main.py
# Kivy Tic Tac Toe with player name & avatar selection screen

#TODO add a back/reset button

import os
from kivy.config import Config

#Keep before remaining kivy imports for window sizes to apply correctly
# Simulate a 1080x2340 Android phone (portrait mode)
Config.set('graphics', 'width', '780')
Config.set('graphics', 'height', '360')
Config.set('graphics', 'resizable', False)

# Optional: lock orientation (portrait)
Config.set('graphics', 'orientation', 'landscape')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
#from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.config import Config

import random

MIN_BARS = 5
MAX_BARS = 30
HARD_MODE = True #For future: when true, only neighboring bars can be swapped.
#TODO add colors for bars
#Ideas: towers of hanoi, 2048- need sequence of 11 fun images

class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = Label(text=f"Enter a number from {MIN_BARS} to {MAX_BARS}", font_size=32)
        layout.add_widget(self.label)

        self.input_box = TextInput(multiline=False, font_size=32, input_filter='int')
        layout.add_widget(self.input_box)

        start_btn = Button(text="Start Game", font_size=32, size_hint=(1, 0.3))
        start_btn.bind(on_release=self.start_game)
        layout.add_widget(start_btn)

        self.add_widget(layout)

    def start_game(self, instance):
        try:
            n = int(self.input_box.text)
            
            if not (MIN_BARS <= n <= MAX_BARS):
                self.label.text = f"Number must be between {MIN_BARS} and {MAX_BARS}!"
                return
        except:
            self.label.text = "Invalid number!"
            return

        self.manager.get_screen('game').setup_game(n)
        self.manager.current = 'game'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected = []   # holds selected buttons
        self.numbers = []    # current order

        self.main_layout = GridLayout(cols=1)

        self.top_grid = GridLayout(
            #cols=3
            # spacing=10, 
            # size_hint=(1, 1), 
            # row_force_default=True,
             height=40,
             size_hint_y=None
            )
        self.top_grid.cols = 3
        back_btn = Button(text='Back')
        back_btn.bind(on_release=self.go_back)
        self.top_grid.add_widget(back_btn)

        self.move_counter = 0
        self.moves = Label(text=f'Moves: {self.move_counter}', font_size=32)
        self.top_grid.add_widget(self.moves)

        self.main_layout.add_widget(self.top_grid)
        
        self.status = Label(text="", font_size=32)

        self.main_layout.add_widget(self.status)

        self.grid = GridLayout(
            cols=5, 
            spacing=10, 
            size_hint=(1, 1), 
            row_force_default=True,
            row_default_height=150
            )
        self.main_layout.add_widget(self.grid)

        
        

        self.add_widget(self.main_layout)

    def setup_game(self, n):
        self.move_counter = 0
        self.moves.text = f'Moves: {self.move_counter}'
        self.n = n
        self.grid.cols = n  #Can change this for multiple rows
        self.grid.clear_widgets()

        # Generate shuffled list
        self.numbers = list(range(1,n+1))
        random.shuffle(self.numbers)

        self.status.text = "Arrange the towers in order!"

        # Create buttons
        self.buttons = []
        for value in self.numbers:
            #btn = TowerButton(value)
            btn = Button(text=str(value))
            btn.size_hint_y=None
            btn.height=180*value/(n+1)
            #btn.add_widget(tower)
            #r, g, b = random.random(), random.random(), random.random()
            #btn.background_color = (r, g, b, 1)
            

            btn.bind(on_release=self.on_select)
            
            self.buttons.append(btn)
            self.grid.add_widget(btn)

    def on_select(self, btn):
        self.selected.append(btn)
        #second paragraph doesn't work? try this instead?
        # if btn in self.selected:
        #     if hasattr(btn, 'saved_bg'):
        #         btn.background_color = btn.saved_bg
        #         del btn.saved_bg


        # if len(self.selected) == 2:
        #     saved_background1 = self.selected[0].background_color
        #     saved_background2 = self.selected[1].background_color
        # elif len(self.selected) == 1:
        #      saved_background = btn.background_color

        btn.background_color = (0, 0.8, 1, 1)  # highlight

        # Once two are selected → swap their positions
        if len(self.selected) == 2:
            i = self.buttons.index(self.selected[0])
            j = self.buttons.index(self.selected[1])
            if (HARD_MODE and abs(i-j) == 1) or (not HARD_MODE):
                self.swap_buttons(self.selected[0], self.selected[1])
                self.move_counter += 1
                self.moves.text = f'Moves: {self.move_counter}'

            # remove highlights
            self.selected[0].background_color = (1,1,1,1)
            self.selected[1].background_color = (1,1,1,1)

            self.selected = []

            # check if sorted
            if self.is_sorted():
                self.status.text = "WINNER WINNER CHICKEN DINNER"

    def swap_buttons(self, btn1, btn2):
        i = self.buttons.index(btn1)
        j = self.buttons.index(btn2)

        # swap the data list
        self.numbers[i], self.numbers[j] = self.numbers[j], self.numbers[i]

        # swap button text
        btn1.text, btn2.text = btn2.text, btn1.text
        btn1.size_hint_y = None
        btn2.size_hint_y = None
        btn1.height, btn2.height = btn2.height, btn1.height

    def is_sorted(self):
        return self.numbers == sorted(self.numbers)
    
    def go_back(self, instance):
        self.manager.current = 'setup'

class TowerButton(Button):
    def __init__(self, tower_height, **kwargs):
        super().__init__(**kwargs)

        # Make background transparent so rectangles show
        #self.background_normal = ''
        #self.background_down = ''
        #self.background_color = (1, 1, 1, 1)
        
        self.tower_height = tower_height
        self.bind(size=self.redraw, pos=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.before.clear()

        block_count = self.tower_height
        if block_count <= 0:
            return

        block_h = self.height / block_count

        with self.canvas.before:
            Color(0,0.2,1,0.5)
            Rectangle(
                pos=(self.x, self.y),
                size=(0.8*self.width,0.8*self.height)
            )
        
            #DEBUG: make only one tower
            # for i in range(block_count):
            #     Color(0, 0.2, 1, 1)
            #     Rectangle(
            #         pos=(self.x, self.y + i * block_h),
            #         size=(0.8*self.width, block_h)
            #     )

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == "__main__":
    GameApp().run()
