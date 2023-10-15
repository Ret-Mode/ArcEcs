import esper
import arcade
import pymunk

from typing import Tuple


class UtilityProcessor:

    _p:esper.Processor = None

    @classmethod
    def getInstance(cls) -> esper.Processor:
        return cls._p
    
    @classmethod
    def set(cls, processor: esper.Processor) -> None:
        cls._p = processor


class MouseUtilsProcessor(UtilityProcessor):
    ...


class SpriteCom:

    def __init__(self, sprite:arcade.Sprite):
        self.sprite = sprite


class MouseCom:

    def __init__(self):
        self.lmb = False
        self.mmb = False
        self.rmb = False
        self.dx = 0
        self.dy = 0
        self.mx = 0
        self.my = 0


class PhysicsCom:

    def __init__(self, body:pymunk.Body):
        self.body = body


class World:

    def __init__(self, threaded:bool = False, gravity:Tuple[float, float] = (0.0, 0.0), dt:float=1.0/60.0):
        self.world = pymunk.Space(threaded)
        self.world.gravity = gravity
        self.dt = dt


class PhysicsProcessor(esper.Processor):

    def process(self):
        sprite: SpriteCom
        body: PhysicsCom
        for _, (sprite, body) in esper.get_components(SpriteCom, PhysicsCom):
            print(body.body.position[0], body.body.position[1])
            sprite.sprite.position = (body.body.position[0], body.body.position[1])


class DrawProcessor(esper.Processor):

    def process(self):
        proxy: SpriteCom
        for _, proxy in esper.get_component(SpriteCom):
            proxy.sprite.draw()


class MouseProcessor(esper.Processor):

    def process(self):
        mouse:MouseCom

