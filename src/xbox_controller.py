from inputs import get_gamepad
import math
import threading
from djitellopy import Tello
import easygui
# This doesnt work on Mac as no devices can be natively connected

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        # Dpad Fix
        self.DPadY = 0
        self.DPadX = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self): # returns inputs
        left_y = self.LeftJoystickX
        left_x = self.LeftJoystickY
        right_y = self.RightJoystickY
        right_x = self.RightJoystickX
        # Buttons
        a = self.A
        x = self.X
        b = self.B
        y = self.Y
        # D pad
        
        Dpad_x = self.DPadX
        Dpad_y = self.DPadY
        # Bumbers
        rb = self.RightBumper
        rt = self.RightTrigger
        lb = self.LeftBumper
        lt = self.LeftTrigger
        # Extras
        start = self.Start
        select = self.Back

        # Extra for spacenavigator to controll lift
        extra = self.RightTrigger - self.LeftTrigger
        return [left_y, left_x, right_y, right_x, a, x, y, b, Dpad_x, Dpad_y, rb, rt, lb, lt, start, select, extra]


    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_START':
                    self.Back = event.state
                elif event.code == 'BTN_SELECT':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state
                # DPad Fix
                elif event.code == 'ABS_HAT0X':
                    self.DPadX = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.DPadY = event.state

    def flight_xbox(self, tello, help):
        cont = self

        print(cont.read())
        if cont.read()[15] == 1:
            easygui.msgbox("Press 'Ok' to engage throw takeoff",title="Info")
            tello.initiate_throw_takeoff()
            help = 1
        elif cont.read()[14] == 1 and help == 0:
            tello.takeoff()
            help = 1
            print("Takeoff")
        elif cont.read()[14] == 1 and help != 0:
            tello.land()
        elif cont.read()[9] == 1:
            tello.flip("b")
        elif cont.read()[8] == -1:
            tello.flip("l")
        elif cont.read()[9] == -1:
            tello.flip("f")
        elif cont.read()[8] == 1:
            tello.flip("r")
        tello.send_rc_control(int(cont.read()[0]*100), int(cont.read()[1]*100), int(cont.read()[16]*100), int(cont.read()[3]*100))

def controller_test(object):

    print(object.read())

if __name__ == '__main__':

    joy = XboxController()
    while True:

            print(joy.read())
        