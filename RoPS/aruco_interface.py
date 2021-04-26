# -*- coding: utf-8 -*-
"""
Created on Wed Apr 7 13:46:40 2021

@author: AdilDSW
"""

import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_4X4_50)
ARUCO_PARAMS = aruco.DetectorParameters_create()

TEXT_COLOR = (75, 96, 227) # BGR Format
BORDER_COLOR = (147, 214, 104) # BGR Format

# Generates a Table of ArUco Markers
def gen_aruco_marker_table(column, row, filename):
    fig = plt.figure()
    for i in range(1, row * column + 1):
        ax = fig.add_subplot(row, column, i)
        ax.axis("off")
        img = aruco.drawMarker(ARUCO_DICT, i, 500)
        plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    plt.savefig(filename, bbox_inches="tight")
    
# Generates an ArUco Marker
def gen_aruco_marker(aruco_id, filename):
    plt.axis("off")
    img = aruco.drawMarker(ARUCO_DICT, aruco_id, 500)
    plt.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    plt.savefig(filename, bbox_inches="tight")

# Detect ArUco Marker in Frame
def detect_and_draw_aruco_markers(frame):
    corners, ids, _ = aruco.detectMarkers(frame, ARUCO_DICT, parameters=ARUCO_PARAMS)
    print (ids)
    if ids is None:
        ids = []
        
    for idx in range(len(ids)):
        marker_id = str(ids[idx][0])
        
        corner = corners[idx].reshape(4, 2)
        (topLeft, topRight, bottomRight, bottomLeft) = corner
        
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        
        cv2.line(frame, topLeft, topRight, BORDER_COLOR, 2)
        cv2.line(frame, topRight, bottomRight, BORDER_COLOR, 2)
        cv2.line(frame, bottomRight, bottomLeft, BORDER_COLOR, 2)
        cv2.line(frame, bottomLeft, topLeft, BORDER_COLOR, 2)
        
        cv2.putText(frame, marker_id, (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 3)
        
    return frame

# Detect ArUco Marker in Frame
def detect_aruco_markers(frame):
    corners, ids, _ = aruco.detectMarkers(frame, ARUCO_DICT, parameters=ARUCO_PARAMS)
    res = {
        "marker_id": [],
        "marker_pos_x": [],
        "marker_pos_y": [],
        "marker_direction_x": [],
        "marker_direction_y": []
    }

    marker_id = []
    marker_pos_x = []
    marker_pos_y = []
    marker_direction_x = []
    marker_direction_y = []
    
    if ids is None:
        ids = []
        
    for idx in range(len(ids)):
        corner = corners[idx].reshape(4, 2)
        (topLeft, topRight, bottomRight, bottomLeft) = corner
        
        topLeft = (int(topLeft[0]), int(topLeft[1]))
        topRight = (int(topRight[0]), int(topRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))

        mid = ((topLeft[0] + bottomRight[0])/2, (topLeft[1] + bottomRight[1])/2)
        direction = (((topLeft[0] - bottomLeft[0]) + (topRight[0] - bottomRight[0]))/2, ((topLeft[1] - bottomLeft[1]) + (topRight[1] - bottomRight[1]))/2)

        marker_id.append(int(ids[idx][0]))
        marker_pos_x.append(mid[1])
        marker_pos_y.append(mid[0])
        marker_direction_x.append(direction[1])
        marker_direction_y.append(direction[0])
        
    res["marker_id"] = marker_id
    res["marker_pos_x"] = marker_pos_x
    res["marker_pos_y"] = marker_pos_y
    res["marker_direction_x"] = marker_direction_x
    res["marker_direction_y"] = marker_direction_y

    return res

if __name__ == "__main__":
    gen_aruco_marker_table(7, 7, "markers.png")