import cv2

def distance2(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

class StickManager:
    points = []
    length = 0
    not_found = True

    def set(self, points, shape):
        cx, cy = shape[0]/2, shape[0]/2
        self.length = max(self.length, distance2(points[:2], points[2:]))
        if distance2(points[:2], [cx, cy]) < distance2(points[2:], [cx, cy]):
            self.points = points
        else:
            self.points = points[2:] + points[:2]
        self.not_found = False

    def collision(self, ball):
        x, y = self.points[:2]
        return (ball.x - x)**2 + (ball.y - y)**2 < ball.r**2

    def draw(self, img):
        if len(self.points) != 4 or self.not_found:
            return
        cv2.line(img, self.points[:2], self.points[2:], (255,0,0), 3)


manager = StickManager()
