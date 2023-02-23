import OpenGL.GL as gl
import OpenGL.GLUT as glut
import glfw

from win32con import WS_EX_LAYERED, GWL_EXSTYLE, WS_EX_TRANSPARENT
from win32gui import FindWindow, GetWindowLong, SetWindowLong, GetWindowRect, GetForegroundWindow, GetWindowText, GetActiveWindow
from math import tan, cos, pi
from helper import ScreenSize, Vector3
from memory import kernel32

class Overlay():
    def __init__(self):
        self.overlay_state = False
        self.csgo_window_title = 'Counter-Strike: Global Offensive - Direct3D 9'
        # Initialize GLFW and GLUT
        if not glfw.init() or not glut.glutInit():
            return

        # Window hints - set before creating a window
        glfw.window_hint(glfw.FLOATING, True)
        glfw.window_hint(glfw.DECORATED, False)
        glfw.window_hint(glfw.RESIZABLE, False)
        glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
        glfw.window_hint(glfw.SAMPLES, 2)

        self.window = glfw.create_window(ScreenSize.x - 1, ScreenSize.y - 1, title:='BG_Overlay', None, None)
        if not self.window:
            return
        # Get handle to the created window
        self.handle = FindWindow(None, title)

        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.make_context_current(self.window)
        glfw.swap_interval(0)
        
        # Set window attributes
        gl.glPushAttrib(gl.GL_ALL_ATTRIB_BITS)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, ScreenSize.x - 1, 0, ScreenSize.y - 1, -1, 1)
        gl.glDisable(gl.GL_DEPTH_TEST)
        # gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # Make window transparent
        exstyle = GetWindowLong(self.handle, GWL_EXSTYLE)
        exstyle |= WS_EX_LAYERED
        exstyle |= WS_EX_TRANSPARENT
        SetWindowLong(self.handle, GWL_EXSTYLE, exstyle)
        SetWindowLong(self.handle, GWL_EXSTYLE,
                            exstyle | WS_EX_LAYERED)
        
        self.overlay_state = True

    def close(self):
        glfw.set_window_should_close(self.window, True)
        if glfw.window_should_close(self.window) == 1:
            self.overlay_state = False
            kernel32.CloseHandle(self.handle)
            glfw.destroy_window(self.window)
    
    def window_focused(self):
        return GetWindowText(GetForegroundWindow()) == self.csgo_window_title
    
    def refresh(self):
        glfw.swap_buffers(self.window)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glfw.poll_events()

    def draw_empty_circle(self, cx: float, cy: float, r: float, points: int, color: Vector3):
        gl.glColor4f(*color, 1.0)
        theta = pi * 2 / float(points)
        tangetial_factor = tan(theta)
        radial_factor = cos(theta)
        x = r
        y = 0
        gl.glLineWidth(1)
        gl.glBegin(gl.GL_LINE_LOOP)
        
        for i in range(points):
            gl.glVertex2f(x + cx, y + cy)
            tx = -y
            ty = x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor
        gl.glEnd()
        gl.glFlush()

    def draw_filled_dot(self, start_point_x: float, start_point_y: float, line_width: float, color: Vector3):
        gl.glPointSize(line_width)
        gl.glBegin(gl.GL_POINTS)
        gl.glColor4f(*color, 1.0)
        gl.glVertex2f(start_point_x, start_point_y)
        gl.glEnd()
        gl.glFlush()

    def draw_line(self, start_point_x: float, start_point_y: float, end_point_x: float, end_point_y: float, line_width: float, color: Vector3):
        gl.glLineWidth(line_width)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color, 1.0)
        gl.glVertex2f(start_point_x, start_point_y)
        gl.glVertex2f(end_point_x, end_point_y)
        gl.glEnd()
        gl.glFlush()

    def draw_lines(self, start_point_x: float, start_point_y: float, line_width: float, color: Vector3):
        gl.glLineWidth(line_width)
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(*color, 1.0)
        gl.glVertex2f(start_point_x, start_point_y + 5)
        gl.glVertex2f(start_point_x, start_point_y - 5)
        gl.glVertex2f(start_point_x - 5, start_point_y)
        gl.glVertex2f(start_point_x + 5, start_point_y)
        gl.glEnd()
        gl.glFlush()

    def draw_full_box(self, start_point_x: float, start_point_y: float, width, height, line_width: float, color: Vector3):
        gl.glLineWidth(line_width)
        gl.glBegin(gl.GL_LINE_LOOP)
        gl.glColor4f(*color, 1.0)
        gl.glVertex2f(start_point_x, start_point_y)
        gl.glVertex2f(start_point_x + width, start_point_y)
        gl.glVertex2f(start_point_x + width, start_point_y + height)
        gl.glVertex2f(start_point_x, start_point_y + height)
        gl.glEnd()
        gl.glFlush()

    def draw_text(self, text: str, x: int, y: int, font=glut.GLUT_BITMAP_9_BY_15):
        gl.glRasterPos2f(x, y)
        gl.glColor4f(0.0, 1.0, 0.0, 1.0)
        lines = text.split("\n")
        line_height = 24
        
        for i, line in enumerate(lines):
            y = y - i * line_height / 1.2

            for c in line:
                glut.glutBitmapCharacter(font, ord(c))
        gl.glFlush()

