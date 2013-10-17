from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from random import sample, randint, random

kv = '''
<Magnet>:
    on_pos: self.attract()
    on_size: self.attract()
'''


class Magnet(Widget):
    transition = StringProperty('out_quad')
    duration = NumericProperty(1)
    anim = ObjectProperty(None, allownone=True)

    def on_children(self, *args):
        if len(self.children) > 1:
            raise ValueError('Magnet can have only one children')
        else:
            self.attract()

    def attract(self, *args):
        if self.anim:
            self.anim.stop(self.children[0])
            self.anim = None

        self.anim = Animation(pos=self.pos, size=self.size,
                              t=self.transition, d=self.duration)

        self.anim.start(self.children[0])


Builder.load_string(kv)

# after that it's for the demo
kvdemo = '''
GridLayout:
    cols: 3
'''

transitions = (
    'out_sine', 'out_quint', 'out_quart', 'out_quad', 'out_expo',
    'out_cubic', 'out_circ', 'out_bounce', 'out_back', 'linear',
    'in_sine', 'in_quint', 'in_quart', 'in_quad', 'in_out_sine',
    'in_out_quint', 'in_out_quart', 'in_out_quad', 'in_out_expo',
    'in_out_cubic', 'in_out_circ', 'in_out_bounce', 'in_out_back',
    'in_expo', 'in_cubic', 'in_circ', 'in_bounce', 'in_back',
    )


class MagnetDemo(App):
    def build(self):
        self.root = Builder.load_string(kvdemo)
        Clock.schedule_interval(self.add_child, 1)
        Clock.schedule_interval(self.add_col, 5)
        Clock.schedule_interval(self.scramble, 10)
        return self.root

    def add_child(self, dt, *args):
        magnet = Magnet(transition=sample(transitions, 1)[0],
                        duration=random())
        magnet.add_widget(Button(text='test %s' % dt))
        self.root.add_widget(magnet, index=randint(0, len(self.root.children)))

    def add_col(self, *args):
        self.root.cols += 1

    def scramble(self, *args):
        for i in sample(self.root.children, len(self.root.children)):
            self.root.remove_widget(i)
            self.root.add_widget(i)

if __name__ == '__main__':
   MagnetDemo().run() 
