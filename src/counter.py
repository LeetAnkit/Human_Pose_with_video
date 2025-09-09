from angle_utils import calculate_angle

class CurlCounter:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def update(self, shoulder, elbow, wrist):
        angle = calculate_angle(shoulder, elbow, wrist)

        if angle > 160:
            self.stage = "down"
        if angle < 30 and self.stage == "down":
            self.stage = "up"
            self.counter += 1

        return angle, self.counter, self.stage
