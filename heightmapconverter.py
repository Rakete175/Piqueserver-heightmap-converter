'''
Script author: Rakete175
LICENSE: The Unlicense. (Do what you want with it)

Hey, this is a heightmap converter for Ace of Spades.
It is meant for mapmakers, because many tools for this stuff are either broken or in a vanished Dropbox.


How it works:
* replace path with the one of your heightmap, including the image itself
* include this into your config file
* open terminal
* type piqueserver --copy-config to refresh it to the new config file
* type piqueserver to start the server and wait a moment
* type the word "draw" into your terminal
* wait until it tells you that its done
* join with OpenSpades and press 8 or join with AoS old client and press F1 (I think).
* now you have the .vxl somewhere on your pc. If you are using Aos it is C:/Ace of Spades/vxl/lastsav.vxl, on OpenSpades it is called shot0001.vxl for example (OpenSpades tells you, just search it).

If your map looks strange it can have two reasons:
* colourmap not yet implemented, but is planned
* your heightmap needs to be inverted first

Warning: NEVER implement this in a public server. If you use the /draw command, everyone disconnects
'''




from piqueserver.commands import command
import PIL
from PIL import Image
img = Image.open('paste-your-path-with-picturefile-here').convert('RGB')
xwidth, yheight = img.size

@command('draw')
def draw(connection):
    connection.protocol.drawmap()

def apply_script(protocol, connection, config):
    class heightmapprotocol(protocol):
        def drawmap(self):
            map=self.map
            newmap=map.copy()
            print('drawing map now')
            xwidth, yheight = img.size
            if xwidth != 512 or yheight != 512:
                print('set 512 x 512 pixels pls before doing this')
            else:
                pixels=img.load()
                for x in range(xwidth):
                    for y in range(yheight):
                        (r,g,b) = (pixels[x, y])
                        h=(r+b+g)/12
                        for z in range(64):
                            if z>=h:
                                solid=True
                            elif z<h:
                                solid=False
                            colour=(r,g,b)
                            if solid:
                                map.set_point(x,y,z,(r,g,b))
                            else:
                                map.remove_point(x,y,z)
                print('ok done')
                self.map=map
                    
    class heightmapconnection(connection):
        whothisreadsisawesome=True
    
    return heightmapprotocol, heightmapconnection
