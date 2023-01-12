

# -*- coding: utf-8 -*-
import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
from imgui_bundle import portable_file_dialogs as pfd

import os
import sys

# For Linux/Wayland users.
if os.getenv("XDG_SESSION_TYPE") == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"

path_to_font = None


class plInfo:
    music_lib = f''
    pl_folder = f''
    new_folder = f''
    ext = '.m3u'
    default_labels = {'music_lib': 'Music Library',
                      'pl_folder': 'Playlist folder',
                      'new_folder': 'Export Folder'}
    paths = {'music_lib': music_lib,
             'pl_folder': pl_folder,
             'new_folder': new_folder}
    extensions = {0:    f'.m3u',
                  1:    f'.m3u8'}


    def update_path(self, key: str, string: str):
        if string == '' or string is None:
            self.paths[key] = self.default_labels[key]
        else:
            self.paths[key] = string

        return self.paths[key]

    def update_ext(self, key: int):
        try:
            self.ext = self.extensions[key]
        except KeyError:
            print('Bad extension!')

def impl_glfw_init(window_name="minimal ImGui/GLFW3 example", width=1280, height=720):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:

        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


class GUI(object):
    def __init__(self):
        super().__init__()
        self.backgroundColor = (0, 0, 0, 1)
        self.window = impl_glfw_init()
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        self.string = ""
        self.f = 0.5

        self.loop()

    def loop(self):

        self.path_inf = plInfo
        ext_num = 0

        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()
            imgui.begin("Custom window", True)

            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File", True):
                    clicked_quit, selected_quit = imgui.menu_item("Quit", "Ctrl+Q", False, True)

                    if clicked_quit:
                        sys.exit(0)

                    imgui.end_menu()
                imgui.end_main_menu_bar()

            imgui.begin_group()
            if imgui.button('Select music library'):
                 self.path_inf.music_lib = pfd.select_folder('Select Music Library').result()

            _, self.path_inf.music_lib = imgui.input_text("Music Library", self.path_inf.music_lib, 256)
            imgui.end_group()

            imgui.begin_group()
            if imgui.button('Select playlist folder'):
                 self.path_inf.pl_folder = pfd.select_folder('Select Playlists').result()

            _, self.path_inf.pl_folder = imgui.input_text("Playlists", self.path_inf.pl_folder, 256)
            imgui.end_group()

            imgui.begin_group()
            if imgui.button('Select music library'):
                 self.path_inf.music_lib = pfd.select_folder('Select Export Path').result()
            _, self.path_inf.new_folder = imgui.input_text("Write Path", self.path_inf.new_folder, 256)
            imgui.end_group()

            imgui.columns(1)

            clicked, ext_num = imgui.combo('Extension', ext_num, [f'.m3u', f'.m3u8'])
            if clicked:
                self.path_inf.update_ext(self.path_inf, ext_num)

            imgui.spacing()

            if imgui.button("Exit"):
                exit(0)

            # imgui.show_test_window()

            imgui.end()

            imgui.render()

            gl.glClearColor(*self.backgroundColor)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()


if __name__ == "__main__":

    gui = GUI()


