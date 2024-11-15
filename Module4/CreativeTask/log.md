this is going to be going insane

22:00 - why am i blue
22:13 - `libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile
libpng warning: iCCP: known incorrect sRGB profile`


Exception in Tkinter callback
Traceback (most recent call last):
  File "/usr/lib/python3.11/tkinter/__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/tkinter/__init__.py", line 861, in callit
    func(*args)
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 38, in update_frame
    if not self.captured_image:
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
^Z
[1]+  Stopped                 ./camera.sh
student334@334ces-M:~/CPSC334/Module4/CreativeTask/scripts$ ./camera.sh
[0:43:48.456814719] [23327]  INFO Camera camera_manager.cpp:325 libcamera v0.3.2+27-7330f29b
[0:43:48.485870058] [23330]  WARN RPiSdn sdn.cpp:40 Using legacy SDN tuning - please consider moving SDN inside rpi.denoise
[0:43:48.489300105] [23330]  INFO RPI vc4.cpp:447 Registered camera /base/soc/i2c0mux/i2c@1/ov5647@36 to Unicam device /dev/media4 and ISP device /dev/media2
[0:43:48.489381086] [23330]  INFO RPI pipeline_base.cpp:1126 Using configuration file '/usr/share/libcamera/pipeline/rpi/vc4/rpi_apps.yaml'
[0:43:48.491288360] [23327]  INFO Camera camera.cpp:1003 Pipeline handler in use by another process
Camera __init__ sequence did not complete.
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/picamera2/picamera2.py", line 269, in __init__
    self._open_camera()
  File "/usr/lib/python3/dist-packages/picamera2/picamera2.py", line 478, in _open_camera
    self.camera.acquire()
RuntimeError: Failed to acquire camera: Device or resource busy

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 77, in <module>
    picam2 = Picamera2()
             ^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/picamera2/picamera2.py", line 281, in __init__
    raise RuntimeError("Camera __init__ sequence did not complete.")
RuntimeError: Camera __init__ sequence did not complete.

[0:48:25.376675803] [23551]  INFO Camera camera_manager.cpp:325 libcamera v0.3.2+27-7330f29b
[0:48:25.405253058] [23554]  WARN RPiSdn sdn.cpp:40 Using legacy SDN tuning - please consider moving SDN inside rpi.denoise
[0:48:25.408455220] [23554]  INFO RPI vc4.cpp:447 Registered camera /base/soc/i2c0mux/i2c@1/ov5647@36 to Unicam device /dev/media4 and ISP device /dev/media2
[0:48:25.408566201] [23554]  INFO RPI pipeline_base.cpp:1126 Using configuration file '/usr/share/libcamera/pipeline/rpi/vc4/rpi_apps.yaml'
[0:48:25.413563157] [23551]  INFO Camera camera.cpp:1003 Pipeline handler in use by another process
Camera __init__ sequence did not complete.
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/picamera2/picamera2.py", line 269, in __init__
    self._open_camera()
  File "/usr/lib/python3/dist-packages/picamera2/picamera2.py", line 478, in _open_camera
    self.camera.acquire()
RuntimeError: Failed to acquire camera: Device or resource busy

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 84, in <module>
    picam2 = Picamera2()
             ^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/picamera2/picamera2.py", line 281, in __init__
    raise RuntimeError("Camera __init__ sequence did not complete.")
RuntimeError: Camera __init__ sequence did not complete.
./camera.sh: line 8: syntax error near unexpected token `"WM_DELETE_WINDOW",'
./camera.sh: line 8: `root.protocol("WM_DELETE_WINDOW", root.quit)'


Traceback (most recent call last):
  File "/usr/lib/python3.11/tkinter/__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/tkinter/__init__.py", line 861, in callit
    func(*args)
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 50, in update_frame
    self.label.configure(image=imgtk)
  File "/usr/lib/python3.11/tkinter/__init__.py", line 1702, in configure
    return self._configure('configure', cnf, kw)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/tkinter/__init__.py", line 1692, in _configure
    self.tk.call(_flatten((self._w, cmd)) + self._options(cnf))

2024-11-14 22:22:42 initInitialise: Can't lock /var/run/pigpio.pid


