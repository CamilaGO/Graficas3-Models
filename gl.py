"""
Paula Camila Gonzalez Ortega
18398
"""
import struct
from obj import Obj

def char(c):
	return struct.pack('=c', c.encode('ascii'))

def word(c):
	return struct.pack('=h', c)

def dword(c):
	return struct.pack('=l', c)

def changecolor(r, g, b):
	return bytes([b, g, r])

BLACK = changecolor(0,0,0)
WHITE = changecolor(255,255,255)
RED = changecolor(255, 0, 0)

class Render(object):
	def __init__(self, width, height):
		self.framebuffer = []
		self.clear_color = BLACK
		self.curr_color = RED
		self.glCreateWindow(width, height)

	def glInit():
		#Se inicializan variables
		pass

	def glCreateWindow(self, width, height):
		self.width = width
		self.height = height

	def glViewPort(self, x, y, width, height):
		self.vpWidth = width
		self.vpHeight = height
		self.vpx = x
		self.vpy = y

	def glclear(self):
		self.framebuffer = [
		[self.clear_color for x in range(self.width)]
		for y in range(self.height)
		]

	def glClearColor(self, r, g, b):
		red = round(r*255)
		green = round(g*255)
		blue = round(g*255)
		self.clear_color = changecolor(red, green, blue)

	def glVertex(self, x, y):
		new_x = round((x+1)*(self.vpWidth/2)+self.vpx)
		new_y = round((y+1)*(self.vpHeight/2)+self.vpy)
		#Linea 59 y 58 basadas en https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glViewport.xhtml
		self.framebuffer[new_y][new_x] = self.curr_color
	
	def glColor(self, r=1, g=1, b=1):
		red = round(r*255)
		green = round(g*255)
		blue = round(g*255)
		self.curr_color = changecolor(red, green, blue)

	def glLinePoint(self, x, y):
		try:
			self.framebuffer[y][x] = self.curr_color
		except:
			pass

	#Funciones para aplicar la ecuacion de la recta y dibujar lineas
	def glLine(self, x0, y0, x1, y1):
		#Para poder solo recibir coordenadas entre -1 y 1
		x0 = round((x0+1)*(self.vpWidth/2)+self.vpx)
		y0 = round((y0+1)*(self.vpHeight/2)+self.vpy)
		x1 = round((x1+1)*(self.vpWidth/2)+self.vpx)
		y1 = round((y1+1)*(self.vpHeight/2 )+self.vpy)

		dx = abs(x1 - x0)
		dy = abs(y1 - y0)

		steep = dy > dx

		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
		 	x0, x1 = x1, x0
		 	y0, y1 = y1, y0

		dx = abs(x1 - x0)
		dy = abs(y1 - y0)

		offset = 0
		limit = dx
		
		y = y0
		for x in range(x0, x1):
			if steep:
				self.glLinePoint(y, x)
			else:
				self.glLinePoint(x, y)
			
			offset += dy*2
			if offset >= limit:
				y += 1 if y0 < y1 else -1
				limit += 2*dx

		#Funciones para aplicar la ecuacion de la recta y dibujar lineas
	def glLineModel(self, x0, y0, x1, y1):
		#Para puede recibir coordenadas mayores al rango de -1 y 1
		dx = abs(x1 - x0)
		dy = abs(y1 - y0)

		steep = dy > dx

		if steep:
			x0, y0 = y0, x0
			x1, y1 = y1, x1
		if x0 > x1:
		 	x0, x1 = x1, x0
		 	y0, y1 = y1, y0

		dx = abs(x1 - x0)
		dy = abs(y1 - y0)

		offset = 0
		limit = dx
		
		y = y0
		for x in range(x0, x1):
			if steep:
				self.glLinePoint(y, x)
			else:
				self.glLinePoint(x, y)
			
			offset += dy*2
			if offset >= limit:
				y += 1 if y0 < y1 else -1
				limit += 2*dx

	def glModel(self, filename, translate, scale):
	    model = Obj(filename)
	    
	    for face in model.faces:
	      vcount = len(face)

	      for j in range(vcount):
	        f1 = face[j][0]
	        f2 = face[(j + 1) % vcount][0]

	        v1 = model.vertices[f1 - 1]
	        v2 = model.vertices[f2 - 1]
	        
	        x1 = round((v1[0] + translate[0]) * scale[0])
	        y1 = round((v1[1] + translate[1]) * scale[1])
	        x2 = round((v2[0] + translate[0]) * scale[0])
	        y2 = round((v2[1] + translate[1]) * scale[1])
	        print(x1, y1, x2, y2)
	        self.glLineModel(x1, y1, x2, y2)

	def finish(self, filename):
		f = open(filename, 'bw')

		# file header
		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(14 + 40 + self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(14 + 40))

		# image header
		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		# pixel data
		for x in range(self.height):
			for y in range(self.width):
				f.write(self.framebuffer[x][y])


		f.close()

