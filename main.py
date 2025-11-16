# main.py
# Kivy Tic Tac Toe with player name & avatar selection screen

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


class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = Label(text="Enter a number from 5 to 20", font_size=32)
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
            if not (5 <= n <= 20):
                self.label.text = "Number must be 5–20!"
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

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.status = Label(text="", font_size=32)
        self.main_layout.add_widget(self.status)

        self.grid = GridLayout(cols=5, spacing=10, size_hint=(1, 1))
        self.main_layout.add_widget(self.grid)

        self.add_widget(self.main_layout)

    def setup_game(self, n):
        self.n = n
        self.grid.cols = n  #Can change this for multiple rows
        self.grid.clear_widgets()

        # Generate shuffled list
        self.numbers = [i + 1 for i in range(n)]
        random.shuffle(self.numbers)

        self.status.text = "Arrange the numbers in order!"

        # Create buttons
        self.buttons = []
        for value in self.numbers:
            #btn = Button()
            btn = Button(text=str(value), font_size=32)
            #tower = TowerWidget(value)
            #btn.add_widget(tower)

            #btn.tower_height = value  # store the value for easy access

            btn.bind(on_release=self.on_select)
            
            self.buttons.append(btn)
            self.grid.add_widget(btn)

    def on_select(self, btn):
        self.selected.append(btn)
        btn.background_color = (0.5, 0.8, 1, 1)  # highlight

        # Once two are selected → swap their positions
        if len(self.selected) == 2:
            self.swap_buttons(self.selected[0], self.selected[1])

            # remove highlights
            for b in self.selected:
                b.background_color = (1, 1, 1, 1)

            self.selected = []

            # check if sorted
            if self.is_sorted():
                self.status.text = "WINNER WINNER CHICKEN DINNER!"

    def swap_buttons(self, btn1, btn2):
        i = self.buttons.index(btn1)
        j = self.buttons.index(btn2)

        # swap the data list
        self.numbers[i], self.numbers[j] = self.numbers[j], self.numbers[i]

        # swap button text
        btn1.text, btn2.text = btn2.text, btn1.text

    def is_sorted(self):
        return self.numbers == sorted(self.numbers)

class TowerWidget(Widget):
    def __init__(self, tower_height, **kwargs):
        super().__init__(**kwargs)
        self.tower_height = tower_height
        self.bind(size=self.redraw, pos=self.redraw)
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()

        th = self.tower_height

        if th <= 0:
            return

        block_h = self.height / th

        with self.canvas:
            for i in range(th):
                Color(0.2, 0.6, 1, 1)
                Rectangle(
                    pos=(self.x, self.y + i * block_h),
                    size=(self.width, block_h)
                )

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == "__main__":
    GameApp().run()
