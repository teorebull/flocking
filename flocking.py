from enum import Enum, auto

import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from vi.config import Config, dataclass, deserialize


@deserialize
@dataclass
class FlockingConfig(Config):
    alignment_weight: float = 0.5
    cohesion_weight: float = 0.5
    separation_weight: float = 0.5

    delta_time: float = 3

    mass: int = 20

    def weights(self) -> tuple[float, float, float]:
        return (self.alignment_weight, self.cohesion_weight, self.separation_weight)


class Bird(Agent):
    config: FlockingConfig

    def find_neighbors(self, R):
        neighbors = []
        for bird in self.simulation.birds:
            if bird != self and self.distance_to(bird) <= R:
                neighbors.append(bird)
                return neighbors


    def change_position(self):
        # Pac-man-style teleport to the other end of the screen when trying to escape
        # Check neighbors within radius R
            neighbors = self.find_neighbors(R)
            if len(neighbors) == 0:
                # No neighbors, perform wandering
                self.wander()
                return
            # Alignment
            avg_velocity = sum(neighbor.velocity for neighbor in neighbors) / len(neighbors)
            alignment = avg_velocity - self.velocity
            # Separation
            separation = sum((self.position - neighbor.position) for neighbor in neighbors) / len(neighbors)
            # Cohesion
            avg_position = sum(neighbor.position for neighbor in neighbors) / len(neighbors)
            cohesion = avg_position - self.position
            # Calculate the total steering force
            ftotal = alpha * alignment + beta * separation + gamma * cohesion
            # Update velocity and apply the steering force
            self.velocity += ftotal / self.mass
            # Limit the maximum velocity
            if self.velocity.magnitude() > MaxVelocity:
                self.velocity = self.velocity.normalize() * MaxVelocity
                # Update the position based on the velocity
                self.position += self.velocity * dt

        



class Selection(Enum):
    ALIGNMENT = auto()
    COHESION = auto()
    SEPARATION = auto()


class FlockingLive(Simulation):
    selection: Selection = Selection.ALIGNMENT
    config: FlockingConfig

    def handle_event(self, by: float):
        if self.selection == Selection.ALIGNMENT:
            self.config.alignment_weight += by
        elif self.selection == Selection.COHESION:
            self.config.cohesion_weight += by
        elif self.selection == Selection.SEPARATION:
            self.config.separation_weight += by

    def before_update(self):
        super().before_update()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.handle_event(by=0.1)
                elif event.key == pg.K_DOWN:
                    self.handle_event(by=-0.1)
                elif event.key == pg.K_1:
                    self.selection = Selection.ALIGNMENT
                elif event.key == pg.K_2:
                    self.selection = Selection.COHESION
                elif event.key == pg.K_3:
                    self.selection = Selection.SEPARATION

        a, c, s = self.config.weights()
        print(f"A: {a:.1f} - C: {c:.1f} - S: {s:.1f}")


(
    FlockingLive(
        FlockingConfig(
            image_rotation=True,
            movement_speed=1,
            radius=50,
            seed=1,
        )
    )
    .batch_spawn_agents(50, Bird, images=["C:\\Users\\teore\\Downloads\\AI BACHELOR\\2nd year\\Project Collective Intelligence\\assignment 0\\code_ass0\\images"])
    .run()
)
