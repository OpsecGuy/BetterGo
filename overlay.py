from OpenGL.GL import glPushAttrib, glMatrixMode, glLoadIdentity, glOrtho, glDisable, glEnable, glBlendFunc, glClear, \
    glLineWidth, glBegin, glColor4f, glVertex2f, glEnd, glPointSize, GL_ALL_ATTRIB_BITS, GL_PROJECTION, GL_DEPTH_TEST, \
    GL_TEXTURE_2D, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, GL_LINE_LOOP, GL_POINTS, GL_LINES

from glfw import init, window_hint, create_window, set_input_mode, make_context_current, swap_interval, swap_buffers, \
    poll_events, set_window_should_close, window_should_close, destroy_window, FLOATING, DECORATED, RESIZABLE, \
    TRANSPARENT_FRAMEBUFFER, SAMPLES, CURSOR, CURSOR_DISABLED

from win32con import WS_EX_LAYERED, GWL_EXSTYLE, WS_EX_TRANSPARENT
from win32gui import FindWindow, GetWindowLong, SetWindowLong
from math import tan, cos, pi
from helper import ScreenSize, Vector3
from memory import kernel32

overlay_state = True
        
class Overlay():
    def __init__(self, target='Counter-Strike: Global Offensive - Direct3D 9'):
        # init glfw
        init()
        
        # set window hints
        window_hint(FLOATING, True)
        window_hint(DECORATED, False)
        window_hint(RESIZABLE, False)
        window_hint(TRANSPARENT_FRAMEBUFFER, True)
        window_hint(SAMPLES, 8)

        if target == 'Counter-Strike: Global Offensive - Direct3D 9':
            self.window = create_window(ScreenSize.x - 1, ScreenSize.y - 1, title:='Overlay', None, None)
            
            set_input_mode(self.window, CURSOR, CURSOR_DISABLED)
            make_context_current(self.window)
            swap_interval(1)
            
            # set window attributes
            glPushAttrib(GL_ALL_ATTRIB_BITS)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0, ScreenSize.x - 1, 0, ScreenSize.y - 1, -1, 1)
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # get handle to created window
            self.handle = FindWindow(None, title)
            
            # make window transparent
            exstyle = GetWindowLong(self.handle, GWL_EXSTYLE)
            exstyle |= WS_EX_LAYERED
            exstyle |= WS_EX_TRANSPARENT
            SetWindowLong(self.handle, GWL_EXSTYLE, exstyle)
            SetWindowLong(self.handle, GWL_EXSTYLE,
                                exstyle | WS_EX_LAYERED)

    def close(self):
        set_window_should_close(self.window, True)
        if window_should_close(self.window) == 1:
            overlay_state = False
            destroy_window(self.window)
            kernel32.CloseHandle(self.handle)
    
    def refresh(self):
        swap_buffers(self.window)
        glClear(GL_COLOR_BUFFER_BIT)
        poll_events()
    
    def draw_empty_circle(self, cx: float, cy: float, r: float, points: int, color: Vector3):
        # credits to https://stackoverflow.com/, I just edited it for my needs
        glColor4f(*color, 255)
        theta = pi * 2 / float(points)
        tangetial_factor = tan(theta)
        radial_factor = cos(theta)
        x = r
        y = 0
        glLineWidth(1)
        glBegin(GL_LINE_LOOP)
        
        for i in range(points):
            glVertex2f(x + cx, y + cy)
            tx = -y
            ty = x

            x += tx * tangetial_factor
            y += ty * tangetial_factor

            x *= radial_factor
            y *= radial_factor
        glEnd()
        
    def draw_filled_dot(self, start_point_x: float, start_point_y: float, line_width: float, color: Vector3):
        glPointSize(line_width)
        glBegin(GL_POINTS)
        glColor4f(color[0], color[1], color[2], 255)
        glVertex2f(start_point_x, start_point_y)
        glEnd()
        
    def draw_line(self, start_point_x: float, start_point_y: float, end_point_x: float, end_point_y: float, line_width: float, color: Vector3):
        glLineWidth(line_width)
        glBegin(GL_LINES)
        glColor4f(color[0], color[1], color[2], 255)
        glVertex2f(start_point_x, start_point_y)
        glVertex2f(end_point_x, end_point_y)
        glEnd()
