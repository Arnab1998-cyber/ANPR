import numpy as np
import tensorflow as tf
import cv2
import os
import matplotlib.pyplot as plt
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils


class DetectNumberPlate:
    def __init__(self, image_path):
        self.image = image_path

    def get_detections(self):
        detect_fn = tf.saved_model.load('NumberPlateDetectionModel')
        category_index = label_map_util.create_category_index_from_labelmap('label_map.pbtxt',
                                                                                use_display_name=True)
        img = cv2.imread(self.image)
        image_np = np.array(img)
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.uint8, name='input_tensor')
        input_tensor = input_tensor[:, :, :, :3]
        detections = detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))
        detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
        label_id_offset = 1
        image_np_with_detections = image_np.copy()
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'] + label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=5,
            min_score_thresh=.6,
            agnostic_mode=False)
        return detections, image_np_with_detections
    
    def get_cropped_image(self):
        detections,image=self.get_detections()
        detection_threshold = 0.6
        scores = list(filter(lambda x: x > detection_threshold, detections['detection_scores']))
        boxes = detections['detection_boxes'][:1]
        classes = detections['detection_classes'][:1]
        width = image.shape[1]
        height = image.shape[0]
        for idx,box in enumerate(boxes):
            roi = box * [height, width, height, width]
            region = image[int(roi[0]):int(roi[2]), int(roi[1]):int(roi[3])]
        return region

    def save_image(self,img,filepath):
        cv2.imwrite(filename=filepath,img=img)

