import turtle

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

    def draw_l_system(self):
        t = turtle.Turtle()
        turtle.reset()
        turtle.hideturtle()
        turtle.speed(0)

        for char in self.axiom:
            if char == "F":
                t.forward(self.distance)
            elif char == "+":
                t.left(self.angle)
            elif char == "-":
                t.right(self.angle)


class FractalModel(BaseModel):
    angle: int
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

    return {"message": "Fractal generated successfully"}


async def validate_parameter(angle, axiom, distance, iterations, rules):
    error_message = "Provide valid inputs for:\n "
    status = True
    if axiom == "" or axiom is None:
        error_message += "Axiom\n "
        status = False
    if not rules:
        error_message += "Rules\n "
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
