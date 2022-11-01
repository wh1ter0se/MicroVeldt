import time
import machine, neopixel

LED = neopixel.NeoPixel(machine.Pin(16), 1)
strip0 = neopixel.NeoPixel(machine.Pin(28), 8)
strip1 = neopixel.NeoPixel(machine.Pin(27), 8)

lights = [LED, strip0, strip1]

btn_PWR = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
btn_BUP = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN)
btn_BDN = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_DOWN)
btn_MOD = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN)
btn_CNF = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

class EventButton():
    def __init__(self, pin):
        self.pin = pin
        self.new_event = False
        self.event_val = False
        
    def update(self):
        if self.pin.value() != self.event_val:
            self.event_val = not self.event_val
            self.new_event = True
            
    def check(self):
        if self.new_event:
            self.new_event = False
            return self.event_val
        
class Toggle(EventButton):
    def __init__(self, pin):
        super().__init__(pin)
        self.value = False
        
    def update(self):
        super().update()
        new_val = self.check()
        if new_val == True:
            self.value = not self.value

power = Toggle(btn_PWR)
mode = EventButton(btn_MOD)
config = EventButton(btn_CNF)

void  = (0,0,0)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)
colors = [red, green, blue]

brightness = 1.0
color_indx = 0
off = True

while True:
    for btn in [power, mode, config]:
        btn.update()
    
    if btn_BUP.value():
        brightness += .001
        brightness = min(brightness, 1.0)
    elif btn_BDN.value():
        brightness -= .001
        brightness = max(brightness, 0.0)
    elif mode.check() == True:
        pass
    elif config.check() == True:
        color_indx += 1
        color_indx %= len(colors)
        
    color = colors[color_indx]
    value = tuple([int(channel*brightness) for channel in color])
    
    for seg in lights:
        val = value if power.value else void
        seg.fill(val)
        seg.write()
