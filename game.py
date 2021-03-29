import arcade
from arcade.application import MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT
import math


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SPRITE_SCALING = 1

CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HEIGHT/2
# INITIAL_D = 'Takumi'

class Rocket: #Creates rocket class
    def __init__(self):
        # Position variables
        self.x = CENTER_X #Symbolic X position of rocket (Rocket stays at 0, 0 and everything is moved around it)
        self.y = CENTER_Y #Symbolic Y position of rocket
        
        #Velocity Variables
        self.velocity_x = 0 #Current X velocity of rocket
        self.velocity_y = 0 #Current Y Velocity of rocket

        # active variables
        self.thrusters = False #If thrusters are enabled
        self.dampers = False #If dampers are enabled

        # Upgrade variables
        self.thrust = 1 #Acceleration of rocket (Default = 1)
        self.damping = 0 #Auto-decelleration of rocket (Default = 0)

rocket = Rocket()



class RocketSprite(arcade.Sprite):
    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.center_x = CENTER_X
        self.center_y = CENTER_Y
    
    def update(self):
        mouse_x_relative = mouse.x-CENTER_X #Finds mouse x relative to position of rocket
        mouse_y_relative = mouse.y-CENTER_Y #Finds mouse y relative to position of rocket
        self.radians = math.atan2(mouse_y_relative, mouse_x_relative) - 1.5708



class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0


mouse = Mouse()


class MyGameWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK) # Sets background color of window to black

        self.ax = 100 # Test Asteroid X 
        self.ay = 100 # Test Asteroid Y

        self.rocket_list = None

        self.rocket_sprite = None

    def setup(self):
        self.rocket_list = arcade.SpriteList()

        self.rocket_sprite = RocketSprite('sprites/stillsprites/still.png', SPRITE_SCALING)

        self.center_x = CENTER_X
        self.center_y = CENTER_Y
        self.rocket_list.append(self.rocket_sprite)



    def on_draw(self):
        arcade.start_render()

        arcade.draw_circle_filled(
            CENTER_X-rocket.x, CENTER_Y-rocket.y, 10, arcade.color.GRAY)
        
        self.rocket_list.draw()

    def on_update(self, delta_time):
        rocket.x += rocket.velocity_x*delta_time #Delta time is the time between frames
        rocket.y += rocket.velocity_y*delta_time

        if rocket.thrusters:
            mouse_x_relative = mouse.x-CENTER_X #Finds mouse x relative to position of rocket
            mouse_y_relative = mouse.y-CENTER_Y #Finds mouse y relative to position of rocket

            hypr = (mouse_x_relative**2 + mouse_y_relative**2)**0.5 #Finds euclidean distance to rocket

            rocket.velocity_x += (mouse_x_relative/hypr)*rocket.thrust
            rocket.velocity_y += (mouse_y_relative/hypr)*rocket.thrust
        self.rocket_list.update()

        

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int): #When a mouse button is pressed this function is executed
        if button == arcade.MOUSE_BUTTON_LEFT: #If left mouse button is clicked thrusters are enabled - Rocket will start accelerating
            rocket.thrusters = True
        if button == arcade.MOUSE_BUTTON_RIGHT: #If Right mouse button is clicked dampers are enabled - Rocket will start decellerating
            rocket.dampers = True

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int): #When a mouse button is released this function is executed
        if button == arcade.MOUSE_BUTTON_LEFT: #If left mouse button is released thrusters are disabled - Rocket will stop accelerating
            rocket.thrusters = False
        if button == arcade.MOUSE_BUTTON_RIGHT: #If Right mouse button is clicked dampers are disabled - Rocket will stop decellerating
            rocket.dampers = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float): #When the mouse is moved this function is executed
        mouse.x = x 
        mouse.y = y


window = MyGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, 'My game window')
window.setup()
arcade.run()
