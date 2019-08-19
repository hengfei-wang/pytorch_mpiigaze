from typing import Optional

import numpy as np

from common import FaceParts


class Eye(FaceParts):
    def __init__(self, name: str):
        super().__init__(name)
        self.normalized_gaze_angles: Optional[np.ndarray] = None
        self.normalized_gaze_vector: Optional[np.ndarray] = None
        self.gaze_vector: Optional[np.ndarray] = None

    def angle_to_vector(self):
        pitch, yaw = self.normalized_gaze_angles
        self.normalized_gaze_vector = -np.array([
            np.cos(pitch) * np.sin(yaw),
            np.sin(pitch),
            np.cos(pitch) * np.cos(yaw)
        ])

    def denormalize_gaze_vector(self) -> None:
        normalizing_rot = self.normalizing_rot.as_matrix()
        self.gaze_vector = self.normalized_gaze_vector @ normalizing_rot

    @staticmethod
    def vector_to_angle(vector: np.ndarray) -> np.ndarray:
        assert vector.shape == (3, )
        x, y, z = vector
        pitch = np.arcsin(-y)
        yaw = np.arctan2(-x, -z)
        return np.array([pitch, yaw])
