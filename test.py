import array
import arcade
from arcade.gl import BufferDescription
from arcade import ArcadeContext

from typing import List, Tuple
import esper

from dataclasses import dataclass as component

import pymunk
from ecs.ecs import SpriteProxy, World, PhysicsProcessor, WorldProcessor, DrawProcessor

class GridDraw:
    
    def __init__(self, ctx:ArcadeContext):
        vertexShader="""
            #version 330
            in vec2 inVert;
            uniform WindowBlock
            {
                mat4 projection;
                mat4 view;
            } window;  
            uniform ABC {
                vec4 color;
                vec2 delta;
            } abc;
            void main() {
                gl_Position = vec4(inVert.xy, 0.0, 1.0);
            }
            """

        geometryShader="""
            #version 330 core
            layout (points) in;
            layout (line_strip, max_vertices = 256) out;
            uniform ABC {
                vec4 color;
                vec2 delta;
            } abc;
            void main() {
                int dx;
                int dy;
                for (dx = 0; dx < 8; ++dx)
                {
                    for (dy = 0; dy < 8; ++dy)
                    {
                        
                        float x = gl_in[0].gl_Position.x + dx * abc.delta.x;
                        float y = gl_in[0].gl_Position.y + dy * abc.delta.y;
                        
                        ////// THIS CONTINUE MESSES LINES
                        if (x > 1.0 || y > 1.0) continue;
                        gl_Position = vec4(x-0.01, y, 0.0, 1.0); 
                        EmitVertex();
                        gl_Position = vec4(x+0.01, y, 0.0, 1.0); 
                        EmitVertex();
                        
                        EndPrimitive();
                        gl_Position = vec4(x, y-0.01, 0.0, 1.0); 
                        EmitVertex();
                        gl_Position = vec4(x, y+0.01, 0.0, 1.0); 
                        EmitVertex();
                        
                        EndPrimitive();
                    }
                }
            } 
            """

        fragmentShader="""
            #version 330
            uniform ABC {
                vec4 color;
                vec2 delta;
            } abc;
            out vec4 fColor;
            void main() {
                fColor = vec4(abc.color.rgb, 1.0);
            }
            """
        self.program = ctx.program(vertex_shader=vertexShader, geometry_shader=geometryShader, fragment_shader=fragmentShader)

        verts = array.array('f', [
                        -1.0, -1.0, -0.89, -0.89
        ])
        
        self.verts = ctx.buffer(data=verts)
        vertsDescription = BufferDescription(self.verts, '2f', ['inVert'] )

        indices = array.array('I', [0,0])
        self.indices = ctx.buffer(data=indices)

        uniform = array.array('f', [
                        1.0, 0.5, 1.0, 1.0, 0.1, 0.1, 0.0, 0.0])
        self.uniform = ctx.buffer(data=uniform)
        
        self.uniform.bind_to_uniform_block(1)

        self.program.set_uniform_safe('ABC', 1)
        # keep Window Block uniform
        self.program.set_uniform_safe('WindowBlock', 0)

        self.geometry = ctx.geometry([vertsDescription],
                                     mode=ctx.POINTS, 
                                     index_buffer=self.indices)
        #ctx.disable(pyglet.gl.GL_DEPTH_TEST)

    def updateVerts(self, verts:List[float]):
        vertsInBytes = len(verts) * 4
        if vertsInBytes != self.verts.size:
            self.verts.orphan(size=vertsInBytes)
        self.verts.write(array.array('f', verts))

        indices = [i for i in range(len(verts)//2)]
        indicesInBytes = len(indices) * 4
        if indicesInBytes != self.indices.size:
            self.indices.orphan(size=indicesInBytes)
            self.geometry.num_vertices = len(indices)
        self.indices.write(array.array('I', indices))

    def updateParams(self, deltas:List[float], color:List[float]):
        arr = color + [1.0] + deltas + [0.0, 0.0]
        self.uniform.write(array.array('f', arr))

    def draw(self):
        self.geometry.render(self.program)


class Runner(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

        worldEnt = esper.create_entity()
        world = World(False, (0.0, -10.0))
        esper.add_component(worldEnt, world)

        ent = esper.create_entity()

        body = pymunk.Body()
        circle = pymunk.Circle(body=body, radius=30)
        circle.mass=6.0
        world.world.add(body, circle)
        body.position = 400, 400
        body.mass = 400
        self.proxy = SpriteProxy(arcade.Sprite('pinky.png'), body)
        esper.add_component(ent, self.proxy)
        esper.add_processor(WorldProcessor())
        esper.add_processor(PhysicsProcessor())
        esper.add_processor(DrawProcessor())

        # self.gridDraw = GridDraw(self.ctx)
        # self.vert = -0.3
        # self.color = 0.0
        # self.deltas = 0.001

    def on_draw(self):
        self.clear()
        esper.process()

Runner(800, 600, "ShaderTest").run()