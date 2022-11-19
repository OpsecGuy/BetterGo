import gui, threading


def main():
    wnd.create()
    threading.Thread(target=wnd.update, daemon=True).start()
    wnd.run()
    wnd.destroy()


if __name__ == '__main__':
    wnd = gui.Window()
    main()