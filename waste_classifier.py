"""
handles the image capture from the  camera and waste classification

Hardware dependencies (TODO for hardware team):
  - Raspberry Pi Camera Module 3
  - TensorFlow Lite model file (ml_model.tflite)
  - LED ring light (optional)

To implement:
  - Fill in _initialise_camera() with picamera2 setup
  - Fill in _load_model() with TFLite interpreter setup
  - Fill in capture_image() to return a numpy array from the camera
  - Fill in classify() to run inference and return (WasteCategory, confidence)
"""

from config import WasteCategory, MODEL_PATH


class WasteClassifier:
    """
    captures an image and classifies it into a WasteCategory

    THE main entry point for the rest of the system is capture_and_classify()
    returns a (WasteCategory, float) tuple
    """

    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.camera = None
        self._initialise_camera()
        self._load_model()

    def _initialise_camera(self):
        """
        TODO: HARDWARE
        Initialise Raspberry Pi Camera Module 3.

        Example (picamera2):
            from picamera2 import Picamera2
            self.camera = Picamera2()
            self.camera.start()
        """
        self.camera = None  # placeholder
        print("[WasteClassifier] Camera initialised (stub)")

    def _load_model(self):
        """
        TODO: HARDWARE / ML
        Load TensorFlow Lite model for waste classification.

        Example:
            import tflite_runtime.interpreter as tflite
            self.model = tflite.Interpreter(model_path=self.model_path)
            self.model.allocate_tensors()
        """
        self.model = None  # placeholder
        print(f"[WasteClassifier] Model loaded from {self.model_path} (stub)")

    def capture_image(self):
        """
        TODO: HARDWARE
        Capture an image from the camera.
        Should return a numpy array suitable for the ML model (e.g. 224x224 RGB).

        Example:
            return self.camera.capture_array()
        """
        print("[WasteClassifier] Image captured (stub)")
        return None  # placeholder

    def classify(self, image) -> tuple[WasteCategory, float]:
        """
        TODO: HARDWARE / ML
        Run the TFLite model on a captured image.
        Returns (WasteCategory, confidence) where confidence is 0.0 - 1.0.
        Return UNKNOWN if confidence is below an acceptable threshold.

        Example:
            input_details  = self.model.get_input_details()
            output_details = self.model.get_output_details()
            self.model.set_tensor(input_details[0]['index'], preprocessed_image)
            self.model.invoke()
            output     = self.model.get_tensor(output_details[0]['index'])
            category_index = output.argmax()
            confidence     = float(output.max())
            return list(WasteCategory)[category_index], confidence
        """
        print("[WasteClassifier] classify() called (stub) - returning UNKNOWN")
        return WasteCategory.UNKNOWN, 0.0

    def capture_and_classify(self) -> tuple[WasteCategory, float]:
        """
        convenience method: capture an image then classify it
        this is the primary method called by SmartBin during a sort cycle,
        it returns (WasteCategory, confidence)
        """
        image = self.capture_image()
        return self.classify(image)
