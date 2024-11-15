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


Traceback (most recent call last):
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 188, in <module>
    app = CameraApp(root, picam2)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 20, in __init__
    self.net = cv2.dnn.readNetFromONNX("deeplabv3_mnv2.onnx")  # Replace with your ONNX model path
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cv2.error: OpenCV(4.6.0) ./modules/dnn/src/onnx/onnx_importer.cpp:255: error: (-5:Bad argument) Can't read ONNX file: deeplabv3_mnv2.onnx in function 'ONNXImporter'

/dev/video0:         38606 38607

Traceback (most recent call last):
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 188, in <module>
    app = CameraApp(root, picam2)
          ^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Camera/camera.py", line 20, in __init__
    self.net = cv2.dnn.readNetFromONNX("../../assets/model/tiny-yolov3-11.onnx")  # Replace with your ONNX model path
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cv2.error: OpenCV(4.6.0) ./modules/dnn/src/onnx/onnx_graph_simplifier.cpp:842: error: (-210:Unsupported format or combination of formats) Unsupported data type: BOOL in function 'getMatFromTensor'

c@1/ov5647@36 - Selected sensor format: 640x480-SGBRG10_1X10 - Selected unicam format: 640x480-pGAA
INFO: Created TensorFlow Lit
e XNNPACK delegate for CPU.
Model loaded successfully
Capturing image
Starting image processing
Applying background blur
Error in process_image_thread: Cannot set tensor: Dimension mismatch. Got 256 but expected 257 for dimension 1 of input 183.
Processing failed

format: 640x480-pGAA
INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
Model loaded successfully
Capturing image
Starting image processing
Applying background blur
Error in process_image_thread: operands could not be broadcast together with shapes (480,480,63,1) (480,480,3) (480,480,3) 
Processing failed

rror in vector conversion: [Errno 2] No such file or directory: 'images/../../assets/images/image_20241115_021758.jpg.svg'
./camera.sh: line 7: 135538 Killed                  python3 camera.py



Lines:   0%|                                           | 0/490 [00:00<?, ?it/s]Error during drawing: 'NoneType' object has no attribute 'total'
Exception in thread Thread-7 (drawing_thread):
Traceback (most recent call last):
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Robot/robot.py", line 58, in drawing_thread
    self.bg.plot_file(json_path)
  File "/home/student334/CPSC334/Module4/CreativeTask/src/BrachioGraphCaricature/plotter.py", line 195, in plot_file
    self.plot_lines(lines, bounds, angular_step, wait, resolution, flip=True)
  File "/home/student334/CPSC334/Module4/CreativeTask/src/BrachioGraphCaricature/plotter.py", line 213, in plot_lines
    for line in tqdm.tqdm(lines, desc="Lines", leave=False):
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Robot/robot.py", line 45, in custom_tqdm_init
    if progress_callback and progress_bar.total:
                             ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'total'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.11/threading.py", line 1038, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.11/threading.py", line 975, in run
    self._target(*self._args, **self._kwargs)
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Robot/robot.py", line 73, in drawing_thread
    self.bg.park()
  File "/home/student334/CPSC334/Module4/CreativeTask/src/BrachioGraphCaricature/plotter.py", line 501, in park
    self.move_angles(self.servo_1_parked_angle, self.servo_2_parked_angle)
  File "/home/student334/CPSC334/Module4/CreativeTask/src/BrachioGraphCaricature/plotter.py", line 426, in move_angles
    for step in tqdm.tqdm(
                ^^^^^^^^^^
  File "/home/student334/CPSC334/Module4/CreativeTask/src/Robot/robot.py", line 45, in custom_tqdm_init
    if progress_callback and progress_bar.total:
                             ^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'total'


