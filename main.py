"""
Paula Camila Gonzalez Ortega
18398
"""
from gl import Render

posX = 250
posY = 250
width = 1000
height = 1000

bitmap = Render(width, height) #los ultimos tres son los colores son los del background

bitmap.glViewPort(500, 500, width , height)
bitmap.glClearColor(0, 0, 0) #background color
bitmap.glclear()
bitmap.glColor(1, 1, 1) #estos colores son los que se usaran en Vertex
bitmap.glModel('./JapaneseGates.obj', (500, 500), (10, 10))


bitmap.finish('out.bmp')