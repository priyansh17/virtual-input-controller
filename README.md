# Virtual Input Controller

This Python repository provides functionality for controlling mouse movements and keyboard inputs using hand gestures captured through a webcam. It utilizes the Hand Tracking Module along with OpenCV for hand detection and tracking.

## Features

- **Hand Tracking**: Utilizes the `handTrackingModule` to detect and track hand movements in real-time.
- **Mouse Control**: Allows control of the mouse cursor based on hand movements, enabling users to move the cursor and perform clicks.
- **Keyboard Emulation**: Recognizes specific hand gestures to trigger keyboard inputs, facilitating control over keyboard functions.

## Requirements

Ensure you have the following dependencies installed:

- `opencv-python`: OpenCV library for image and video processing.
- `autopy`: Cross-platform Python library for simulating mouse and keyboard inputs.
- `numpy`: Fundamental package for scientific computing with Python.
- `pynput`: Library for controlling input devices such as keyboard and mouse.

You can install the dependencies via pip:

```bash
pip install opencv-python autopy numpy pynput
```

## Usage

1. Clone the repository:
```bash
git clone https://github.com/priyansh17/virtual-input-controller.git
```

2. Navigate to the project directory:

```bash
cd virtual-input-controller
```

3. Run the Python script:

```bash
python virtual_input_controller.py
```

4. Ensure your webcam is connected and positioned correctly to capture hand gestures.

5. Perform the following gestures for corresponding actions:

   - **Mouse Control**:
     - Extend your index finger to control the mouse cursor.
     - Make a closed fist to perform a left click.

   - **Keyboard Emulation**:
     - Raise your hand with the index finger pointing up to emulate the 'W' key (move up).
     - Lower your hand with the index finger pointing down to emulate the 'S' key (move down).
     - Move your hand left while keeping the index finger raised to emulate the 'A' key (move left).
     - Move your hand right while keeping the index finger raised to emulate the 'D' key (move right).

6. Press `Esc` to exit the application.
