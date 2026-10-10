from constants import LINE_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH
import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)        
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen,"white",self.triangle(),LINE_WIDTH)
                

    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with(self, other) -> bool:        
        return self.position.distance_to(other.position) <= self.radius + other.radius

    def wrap_around(self):
           # Wrap horizontally
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
    
            # Wrap vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def collides_with_triangle(self, triangle_points):
        # triangle_points is [a, b, c] - the 3 vertices of the ship
        center = self.position
        radius = self.radius

        # 1. Check if circle center is inside the triangle
        if self._point_in_triangle(center, triangle_points):
            return True

        # 2. Check if circle intersects any of the 3 edges (a-b, b-c, c-a)
        edges = [
            (triangle_points[0], triangle_points[1]),
            (triangle_points[1], triangle_points[2]),
            (triangle_points[2], triangle_points[0]),
        ]
        for p1, p2 in edges:
            if self._distance_to_segment(center, p1, p2) <= radius:
                return True

        return False

    def _point_in_triangle(self, pt, triangle):
        p1, p2, p3 = triangle

        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(pt, p1, p2)
        d2 = sign(pt, p2, p3)
        d3 = sign(pt, p3, p1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def _distance_to_segment(self, point, a, b):
        ab = b - a
        ab_len_sq = ab.length_squared()
        if ab_len_sq == 0:
            return (point - a).length()

        # Project point onto line segment, clamped between 0 and 1
        t = max(0, min(1, (point - a).dot(ab) / ab_len_sq))
        projection = a + ab * t
        return (point - projection).length()
            