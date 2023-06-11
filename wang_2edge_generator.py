import PIL

from PIL import Image, ImageOps, ImageDraw, ImageFont
import os

import random


class WangTiles(object):

    def __init__(self):
        self.cell_size = 350
        self.square_size = 50

        #self.build_cells()
        self.random_dungeon()

    def check_exit(self, index, heading):
        return int(index/heading) % 2

    def room_min(self):
        return random.choice([50,100])

    def dotted_line(self, drawing, spacing, start, end):

        s = start
        e = end
        fold_color = (0,0,0)
        on = True
        
        for axis in range(2):
            draw_length = e[axis] - s[axis]
            if draw_length > spacing:
                count = int(draw_length / spacing)
                
                for c in range(count):
                    
                    if axis == 0:
                        s2 = [s[0] + spacing, s[1]]
                        if on:
                            drawing.line([s[0],s[1],s2[0],e[1]], fill = fold_color, width=4)                        
                    else:
                        s2 = [s[0], s[1] + spacing]
                        if on:
                            drawing.line([s[0],s[1],e[0],s2[1]], fill = fold_color, width=4)

                    s = s2
                    on = not on

    def room_max(self):
        return random.choice([250,300])

    def build_cells(self):
        white = (255,255,255)

        c_array = Image.new("RGB", [350*4, 350*4], color=white)
        r_array = Image.new("RGB", [350*4, 350*4], color=white)
        
        px = 0
        py = 0

        for i in range(16):
            
            color = (200,200,200)
            empty = True
            
            im = Image.new("RGB", [self.cell_size, self.cell_size], color=white)
            draw = ImageDraw.Draw(im)
            edge = (0,0,0)
            
            for x in range(7):
                for y in range(7):
                    x_start = x * 50
                    y_start = y * 50
                    draw.rectangle([x_start, y_start, x_start + 50, y_start + 50], fill = white, outline=color, width=2)

            #draw.rectangle([0,0,350,350], fill = white, outline=edge, width=4)      

            exits = [[0,-1,1], [1,0,2], [0,1,4], [-1,0,8]]
            for e in exits:
                x_mod = e[0]
                y_mod = e[1]
                heading = e[2]

                passing = self.check_exit(i, heading)
                
                if passing == 1:
                    empty = False
                    corridor = [150 + (50 * (x_mod * 4)),150 + (50 * (y_mod*4))]                    
                    
                    draw.rectangle([150,150,corridor[0]+50,corridor[1]+50], fill = color, outline=color, width=4)
                    # center room
                    draw.rectangle([150,150,200,200], fill = color, outline=color, width=0)

            edges = [[[0,0], [0,350]], [[0,0], [350,0]], [[0,350], [350,350]], [[350,0], [350,350]]]
            for edge in edges:
                e_start = edge[0]
                e_end = edge[1]
                self.dotted_line(draw, 15, e_start, e_end)
            
            im.save("./set1/{}a.jpg".format(i), "JPEG")

            

            c_array.paste(im, box=[px*350,py*350])
            
            #make room version
            if not empty:
                rand_room = [self.room_min(), self.room_min(), self.room_max(), self.room_max()]
                draw.rectangle(rand_room, fill = color, outline=color, width=0)

            im.save("./set1/{}b.jpg".format(i), "JPEG")

            r_array.paste(im, box=[px*350,py*350])

            if px < 3:
                px += 1
            else:
                px = 0
                py += 1

            c_array.save("./corridors.jpg", "JPEG")
            r_array.save("./rooms.jpg", "JPEG")

    def random_dungeon(self):
        max_x = 7
        max_y = 5
        white = (255,255,255)
        
        base = Image.new("RGB", [self.cell_size * max_x, self.cell_size * max_y], color=white)                    
        array = [[random.randint(0,2) for y in range(max_y)] for x in range(max_x)]


        for m in range(2):
            for x in range(max_x):
                for y in range(max_y):
                    target_cell = array[x][y]
                    if target_cell == 0:
                        array[x][y] = random.randint(0,1)


        exits = [[0,-1,1], [1,0,2], [0,1,4], [-1,0,8]]       

        

        for x in range(max_x):
            for y in range(max_y):
                room = "a"
                
                base_number = array[x][y]
                set_number = 0
                
                if base_number > 0:
                    if base_number == 2:
                        room = "b"
                    
                    set_number = 0
                    for e in exits:
                        xt = x+e[0]
                        yt = y+e[1]
                        heading = e[2]

                        if xt >= 0 and xt < max_x and yt >= 0 and yt < max_y:                         
                            target_tile  = array[xt][yt]
                            if base_number == 1:
                                if target_tile > 0:
                                    set_number += heading
                                    
                            if base_number == 2:
                                if target_tile == 1:
                                    set_number += heading 
                 
                tile_object = "./set1/{}{}.jpg".format(set_number, room)
                with Image.open(tile_object) as pasted_object:
                    base.paste(pasted_object, box=[x*350, y*350])
                    
        base.save("./random_dungeon.jpg", "JPEG")

            
tile_builder = WangTiles()
print("finished")
        
        
