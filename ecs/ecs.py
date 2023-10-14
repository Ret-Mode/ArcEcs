import esper
import arcade
import pymunk

from typing import Tuple


class SpriteProxy:

    def __init__(self, sprite:arcade.Sprite, body:pymunk.Body):
        self.sprite = sprite
        self.body = body


class World:

    def __init__(self, threaded:bool = False, gravity:Tuple[float, float] = (0.0, 0.0), dt:float=1.0/60.0):
        self.world = pymunk.Space(threaded)
        self.world.gravity = gravity
        self.dt = dt


class WorldProcessor(esper.Processor):
    
    def process(self):
        world:World
        for _, world in esper.get_component(World):
            world.world.step(world.dt)


class PhysicsProcessor(esper.Processor):

    def process(self):
        proxy: SpriteProxy
        for _, proxy in esper.get_component(SpriteProxy):
            print(proxy.body.position[0], proxy.body.position[1])
            proxy.sprite.position = (proxy.body.position[0], proxy.body.position[1])


class DrawProcessor(esper.Processor):

    def process(self):
        proxy: SpriteProxy
        for _, proxy in esper.get_component(SpriteProxy):
            proxy.sprite.draw()