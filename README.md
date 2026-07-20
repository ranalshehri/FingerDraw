# Finger Draw ✍️

Draw on your webcam feed using just your index finger! Built with OpenCV and MediaPipe hand tracking — no mouse, no stylus, just your hand in front of the camera.

## How It Works

- Hold up **1 finger** (index finger) → drawing mode (green dot) — the tip of your index finger paints a magenta trail on screen.
- Hold up **2 or more fingers** → pause mode (red dot) — move your hand freely without drawing, like lifting a pen off paper.
- The app tracks 21 hand landmarks per frame using MediaPipe and checks whether each fingertip is above its lower joint to determine which fingers are extended.

## Requirements

- Python 3.7+
- A webcam

### Dependencies

```bash
pip install opencv-python mediapipe numpy
```

## Usage

```bash
python finger_draw.py
```

### Controls

| Key / Gesture | Action |
|---|---|
| ☝️ 1 finger up | Draw |
| ✌️ 2+ fingers up | Pause (move without drawing) |
| `c` | Clear the canvas/trail |
| `q` | Quit the application |

## Project Structure

```
opencv.py     # Main script — capture, hand tracking, drawing logic
```

## Technical Notes

- **Resolution:** Camera capture is set to 640×480 for performance; adjust `CAP_PROP_FRAME_WIDTH` / `CAP_PROP_FRAME_HEIGHT` if you want a different size.
- **Finger detection:** `count_fingers_up()` checks the index, middle, ring, and pinky fingers only (thumb is excluded for simplicity, since its extension logic differs due to its sideways orientation).
- **Trail breaks:** When you switch to pause mode, a `None` is inserted into the trail list so the line doesn't jump across the pause — this keeps separate strokes visually distinct.
- **Detection confidence:** `min_detection_confidence` and `min_tracking_confidence` are both set to `0.7` for more stable tracking; lower these if hand detection feels too strict in dim lighting.

## Known Limitations

- Only tracks one hand at a time (`max_num_hands=1`).
- Performance depends on lighting and camera quality — poor lighting can cause flickery landmark detection.
- The trail is stored in memory only; there's no save-to-file feature yet.

## Possible Improvements

- Add a "save drawing as image" feature (e.g., pressing `s` to export the canvas via `cv2.imwrite`).
- Support color switching via additional gestures or key presses.
- Add an eraser mode (e.g., open palm = erase nearby trail points).
- Draw on a separate transparent canvas layer instead of directly on the video frame, so the drawing persists independent of hand visibility.

## License

Feel free to use, modify, and share.
