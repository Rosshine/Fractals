import unittest
from views import LSystems, FractalModel, app, validate_parameter
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestLSystems(unittest.TestCase):
    def test_apply_rule(self):
        axiom = "F"
        rules = {"F": "F+F-F-F+F"}
        angle = 90
        iterations = 2
        distance = 10

        l_system = LSystems(axiom, rules, angle, iterations, distance)
        l_system.apply_rule()

        expected_axiom = "F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F"
        self.assertEqual(l_system.axiom, expected_axiom)

    def test_draw_l_system(self):
        axiom = "F"
        rules = {"F": "F+F-F-F+F"}
        angle = 90
        iterations = 2
        distance = 10

        l_system = LSystems(axiom, rules, angle, iterations, distance)
        l_system.apply_rule()
        l_system.draw_l_system()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()


class TestFastAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch.object(LSystems, 'draw_l_system', MagicMock())  # Mocking draw_l_system
    def test_generate_fractal(self):
        # input parameters for testing
        fractal_data = {
            "axiom": "F",
            "rules": {"F": "F+F-F-F+F"},
            "angle": 90,
            "iterations": 2,
            "distance": 10
        }

        # Send a POST request to the endpoint
        response = self.client.post("/generate_fractal/", json=fractal_data)

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        expected_response = {"message": "Fractal generated successfully"}
        self.assertEqual(response.json(), expected_response)

    @patch.object(LSystems, 'draw_l_system', MagicMock())  # Mocking draw_l_system
    def test_generate_fractal_invalid(self):
        fractal_data = {
            "axiom": "",
            "rules": {},
            "angle": 0,
            "iterations": 0,
            "distance": 0
        }
        response = self.client.post("/generate_fractal/", json=fractal_data)
        self.assertEqual(response.status_code, 400)

        # Check the response content
        expected_response = {
            "detail": "Provide valid inputs for:\n Axiom\n Rules\n Angle (Provide valid number between -180 to 180, "
                      "other than 0)\n Iterations (Provide valid number > 0)\n Distance (Provide valid distance > "
                      "0)\n "}
        self.assertEqual(response.json(), expected_response)

    @patch.object(LSystems, 'draw_l_system', MagicMock())  # Mocking draw_l_system
    def test_generate_fractal_invalid_param(self):
        fractal_data = {
            "axiom": None,
            "rules": {"F": "F+F-F-F+F"},
            "angle": 90,
            "iterations": 2,
            "distance": 10
        }
        response = self.client.post("/generate_fractal/", json=fractal_data)
        self.assertEqual(response.status_code, 422)

        # Check the response content
        expected_response = {
            "detail": [
                {
                    "type": "string_type",
                    "loc": [
                        "body",
                        "axiom"
                    ],
                    "msg": "Input should be a valid string",
                    "input": None
                }
            ]
        }
        self.assertEqual(response.json(), expected_response)


if __name__ == '__main__':
    unittest.main()


class ValidateParam(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    async def test_validate_parameter(self):
        axiom = "F"
        rules = {"F": "F+F-F-F+F"}
        angle = 90
        iterations = 2
        distance = 10
        message, status = await validate_parameter(axiom, rules, angle, iterations, distance)
        self.assertEqual(status, True)
        self.assertEqual(message, "Parameters Validated")

    async def test_invalid_parameter(self):
        axiom = "F"
        rules = {}
        angle = 0
        iterations = 2
        distance = 10
        message, status = await validate_parameter(axiom, rules, angle, iterations, distance)
        self.assertEqual(status, True)
        expected_response = {
            "detail": "Provide valid inputs for:\n Rules\n Angle (Provide valid number between -180 to 180, "
                      "other than 0)\n "}
        self.assertEqual(message, expected_response)

    async def test_invalid_distance(self):
        axiom = "F"
        rules = {"F": "F+F-F"}
        angle = 40
        iterations = 2
        distance = 0
        message, status = await validate_parameter(axiom, rules, angle, iterations, distance)
        self.assertEqual(status, True)
        expected_response = {
            "detail": "Provide valid inputs for:\n Distance (Provide valid distance > 0)\n "}
        self.assertEqual(status, 400)
        self.assertEqual(message, expected_response)

    async def test_invalid_iteration(self):
        axiom = "F"
        rules = {"F": "F+F-F"}
        angle = 30
        iterations = 0
        distance = 10
        message, status = await validate_parameter(axiom, rules, angle, iterations, distance)
        self.assertEqual(status, True)
        expected_response = {
            "detail": "Provide valid inputs for:\n Iterations (Provide valid number > 0)\n "}
        self.assertEqual(message, expected_response)

    async def test_invalid_rules(self):
        axiom = "F"
        rules = dict()
        angle = 30
        iterations = 0
        distance = 10
        message, status = await validate_parameter(axiom, rules, angle, iterations, distance)
        self.assertEqual(status, True)
        expected_response = {
            "detail": "Provide valid inputs for:\n Rules\n "}
        self.assertEqual(message, expected_response)


if __name__ == '__main__':
    unittest.main()


class TestHealthAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        message = {"message": "Server is Up and Running"}
        self.assertEqual(response.json(), message)


if __name__ == '__main__':
    unittest.main()
