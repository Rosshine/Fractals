import os
import turtle

from PIL import Image, ImageGrab
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class LSystems:
    def __init__(self, axiom, rules, angle, iterations, distance):
        self.axiom = axiom
        self.rules = rules
        self.angle = angle
        self.iterations = iterations
        self.distance = distance

    def apply_rule(self):
        for _ in range(self.iterations):
            new_string = ""
            for char in self.axiom:
                new_string += self.rules.get(char, char)
            self.axiom = new_string
        print(self.axiom)
    def draw_l_system(self):
        stack = []
        t = turtle.Turtle()
        t.reset()
        # screen_width = turtle.Screen().window_width()
        # screen_height = turtle.Screen().window_height()
        screen = turtle.Screen()
        screen.setup(width=1.0, height=1.0)
        t.hideturtle()
        t.speed(0)
        t.clear()
        # t.left(90)
        for char in self.axiom:
            if char == "F":
                t.forward(self.distance)
            elif char == "+":
                t.left(self.angle)
            elif char == "-":
                t.right(self.angle)
            elif char == "[":
                stack.append((t.position(), t.heading()))
            elif char == "]":
                position, heading = stack.pop()
                t.penup()
                t.setposition(position)
                t.setheading(heading)
                t.pendown()

        return t

class FractalModel(BaseModel):
    angle: float
    rules: dict
    axiom: str
    iterations: int
    distance: int

@app.post('/generate_fractal/')
async def generate_structures(item: FractalModel):
    axiom = item.axiom
    rules = item.rules
    angle = item.angle
    iterations = item.iterations
    distance = item.distance
    error_message, status = await validate_parameter(angle, axiom, distance, iterations, rules)
    if not status:
        raise HTTPException(status_code=400, detail=error_message)
    l_system = LSystems(axiom, rules, angle, iterations, distance)
    l_system.apply_rule()
    l_system.draw_l_system()
    screenshot = ImageGrab.grab()
    width, height = screenshot.size
    left = 50
    top = 100
    right = width
    bottom = height - 200
    im1 = screenshot.crop((left, top, right, bottom))
    image_path = "{0}.png".format(axiom)
    image_path = os.path.join(os.getcwd(), image_path)
    im1.save(image_path)
    # img = Image.open(f"{axiom}_fractal.eps", gs='path/to/gswin64c.exe')

    # screenshot.show()
    return {"message": "Fractal generated successfully", "image_path": image_path}


async def validate_parameter(angle, axiom, distance, iterations, rules):
    error_message = "Provide valid inputs for:\n "
    status = True
    if axiom == "" or axiom is None:
        error_message += "Axiom\n "
        status = False
    if not rules or any(char not in ['F','A', 'B', '+', '-'] for char in rules):
        error_message += "Rules(Provide Valid Rules, Rules Accept only A, B, F, + and -)\n "
        status = False
    if angle == 0:
        error_message += "Angle (Provide valid number between -180 to 180, other than 0)\n "
        status = False
    if iterations == 0:
        error_message += "Iterations (Provide valid number > 0)\n "
        status = False
    if distance == 0:
        error_message += "Distance (Provide valid distance > 0)\n "
        status = False
    if status:
        return "Parameters Validated", status
    return error_message, status


@app.get('/health/')
def health():
    return {"message": "Server is Up and Running"}
