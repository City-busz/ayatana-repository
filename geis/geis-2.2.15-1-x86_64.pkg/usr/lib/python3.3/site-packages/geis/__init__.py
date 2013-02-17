# Copyright (C) 2011 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 3 of the GNU General Public License as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA



"""Python bindings for the GEIS gesture recognition interface.
"""


__all__ = (
        'Geis', 'Event', 'Filter', 'Subscription',
        'NoMoreEvents',
        'GEIS_STATUS_SUCCESS',
        'GEIS_STATUS_CONTINUE',
        'GEIS_STATUS_EMPTY',
        'GEIS_STATUS_NOT_SUPPORTED',
        'GEIS_STATUS_BAD_ARGUMENT',
        'GEIS_STATUS_UNKNOWN_ERROR',
        'GEIS_ATTR_TYPE_BOOLEAN',
        'GEIS_ATTR_TYPE_FLOAT',
        'GEIS_ATTR_TYPE_INTEGER',
        'GEIS_ATTR_TYPE_POINTER',
        'GEIS_ATTR_TYPE_STRING',
        'GEIS_INIT_SERVICE_PROVIDER',
        'GEIS_INIT_TRACK_DEVICES',
        'GEIS_INIT_TRACK_GESTURE_CLASSES',
        'GEIS_INIT_SYNCHRONOUS_START',
        'GEIS_INIT_MOCK_BACKEND',
        'GEIS_INIT_DBUS_BACKEND',
        'GEIS_INIT_GRAIL_BACKEND',
        'GEIS_INIT_XCB_BACKEND',
        'GEIS_CLASS_ATTRIBUTE_ID',
        'GEIS_CLASS_ATTRIBUTE_NAME',
        'GEIS_CONFIGURATION_FD',
        'GEIS_CONFIG_MAX_EVENTS',
        'GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH',
        'GEIS_DEVICE_ATTRIBUTE_ID',
        'GEIS_DEVICE_ATTRIBUTE_INDEPENDENT_TOUCH',
        'GEIS_DEVICE_ATTRIBUTE_NAME',
        'GEIS_DEVICE_ATTRIBUTE_TOUCHES',
        'GEIS_EVENT_ATTRIBUTE_CLASS',
        'GEIS_EVENT_ATTRIBUTE_DEVICE',
        'GEIS_EVENT_ATTRIBUTE_GROUPSET',
        'GEIS_EVENT_ATTRIBUTE_GROUPSET',
        'GEIS_EVENT_ATTRIBUTE_TOUCHSET',
        'GEIS_EVENT_ATTRIBUTE_TOUCHSET',
        'GEIS_EVENT_CLASS_AVAILABLE',
        'GEIS_EVENT_CLASS_CHANGED',
        'GEIS_EVENT_CLASS_UNAVAILABLE',
        'GEIS_EVENT_DEVICE_AVAILABLE',
        'GEIS_EVENT_DEVICE_UNAVAILABLE',
        'GEIS_EVENT_ERROR',
        'GEIS_EVENT_GESTURE_BEGIN',
        'GEIS_EVENT_GESTURE_END',
        'GEIS_EVENT_GESTURE_UPDATE',
        'GEIS_EVENT_INIT_COMPLETE',
        'GEIS_EVENT_USER_DEFINED',
        'GEIS_GESTURE_ATTRIBUTE_ANGLE',
        'GEIS_GESTURE_ATTRIBUTE_ANGLE_DELTA',
        'GEIS_GESTURE_ATTRIBUTE_ANGULAR_VELOCITY',
        'GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_X1',
        'GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_X2',
        'GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_Y1',
        'GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_Y2',
        'GEIS_GESTURE_ATTRIBUTE_CHILD_WINDOW_ID',
        'GEIS_GESTURE_ATTRIBUTE_DELTA_X',
        'GEIS_GESTURE_ATTRIBUTE_DELTA_Y',
        'GEIS_GESTURE_ATTRIBUTE_DEVICE_ID',
        'GEIS_GESTURE_ATTRIBUTE_EVENT_WINDOW_ID',
        'GEIS_GESTURE_ATTRIBUTE_FOCUS_X',
        'GEIS_GESTURE_ATTRIBUTE_FOCUS_Y',
        'GEIS_GESTURE_ATTRIBUTE_GESTURE_NAME',
        'GEIS_GESTURE_ATTRIBUTE_POSITION_X',
        'GEIS_GESTURE_ATTRIBUTE_POSITION_Y',
        'GEIS_GESTURE_ATTRIBUTE_RADIAL_VELOCITY',
        'GEIS_GESTURE_ATTRIBUTE_RADIUS',
        'GEIS_GESTURE_ATTRIBUTE_RADIUS_DELTA',
        'GEIS_GESTURE_ATTRIBUTE_ROOT_WINDOW_ID',
        'GEIS_GESTURE_ATTRIBUTE_TAP_TIME',
        'GEIS_GESTURE_ATTRIBUTE_TIMESTAMP',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_0_ID',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_0_X',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_0_Y',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_1_ID',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_1_X',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_1_Y',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_2_ID',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_2_X',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_2_Y',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_3_ID',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_3_X',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_3_Y',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_4_ID',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_4_X',
        'GEIS_GESTURE_ATTRIBUTE_TOUCH_4_Y',
        'GEIS_GESTURE_ATTRIBUTE_TOUCHES',
        'GEIS_GESTURE_ATTRIBUTE_VELOCITY_X',
        'GEIS_GESTURE_ATTRIBUTE_VELOCITY_Y',
        'GEIS_REGION_ATTRIBUTE_WINDOWID',
        'GEIS_REGION_X11_ROOT',
        'GEIS_REGION_X11_WINDOWID',
        'GEIS_TOUCH_ATTRIBUTE_ID',
        'GEIS_TOUCH_ATTRIBUTE_ID',
        'GEIS_TOUCH_ATTRIBUTE_X',
        'GEIS_TOUCH_ATTRIBUTE_X',
        'GEIS_TOUCH_ATTRIBUTE_Y',
        'GEIS_TOUCH_ATTRIBUTE_Y',
        'GEIS_FILTER_DEVICE',
        'GEIS_FILTER_CLASS',
        'GEIS_FILTER_REGION',
        'GEIS_FILTER_OP_EQ',
        'GEIS_FILTER_OP_NE',
        'GEIS_FILTER_OP_GT',
        'GEIS_FILTER_OP_GE',
        'GEIS_FILTER_OP_LT',
        'GEIS_FILTER_OP_LE',
        )

from _geis_bindings import GEIS_STATUS_SUCCESS, \
                           GEIS_STATUS_CONTINUE, \
                           GEIS_STATUS_EMPTY, \
                           GEIS_STATUS_NOT_SUPPORTED, \
                           GEIS_STATUS_BAD_ARGUMENT, \
                           GEIS_STATUS_UNKNOWN_ERROR

from _geis_bindings import GEIS_ATTR_TYPE_BOOLEAN, \
                           GEIS_ATTR_TYPE_FLOAT, \
                           GEIS_ATTR_TYPE_INTEGER, \
                           GEIS_ATTR_TYPE_POINTER, \
                           GEIS_ATTR_TYPE_STRING

from _geis_bindings import GEIS_INIT_SERVICE_PROVIDER, \
                           GEIS_INIT_TRACK_DEVICES, \
                           GEIS_INIT_TRACK_GESTURE_CLASSES, \
                           GEIS_INIT_MOCK_BACKEND, \
                           GEIS_INIT_DBUS_BACKEND, \
                           GEIS_INIT_GRAIL_BACKEND, \
                           GEIS_INIT_XCB_BACKEND, \
                           GEIS_INIT_SYNCHRONOUS_START

from _geis_bindings import GEIS_CONFIGURATION_FD, \
                           GEIS_CONFIG_MAX_EVENTS

from _geis_bindings import GEIS_EVENT_ATTRIBUTE_DEVICE, \
                           GEIS_DEVICE_ATTRIBUTE_NAME, \
                           GEIS_DEVICE_ATTRIBUTE_ID, \
                           GEIS_DEVICE_ATTRIBUTE_TOUCHES, \
                           GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH, \
                           GEIS_DEVICE_ATTRIBUTE_INDEPENDENT_TOUCH

from _geis_bindings import GEIS_EVENT_ATTRIBUTE_CLASS, \
                           GEIS_CLASS_ATTRIBUTE_NAME, \
                           GEIS_CLASS_ATTRIBUTE_ID

from _geis_bindings import GEIS_REGION_ATTRIBUTE_WINDOWID, \
                           GEIS_REGION_X11_ROOT, \
                           GEIS_REGION_X11_WINDOWID

from _geis_bindings import GEIS_EVENT_ATTRIBUTE_GROUPSET, \
                           GEIS_EVENT_ATTRIBUTE_TOUCHSET, \
                           GEIS_TOUCH_ATTRIBUTE_ID, \
                           GEIS_TOUCH_ATTRIBUTE_X, \
                           GEIS_TOUCH_ATTRIBUTE_Y

from _geis_bindings import GEIS_EVENT_DEVICE_AVAILABLE, \
                           GEIS_EVENT_DEVICE_UNAVAILABLE, \
                           GEIS_EVENT_CLASS_AVAILABLE, \
                           GEIS_EVENT_CLASS_CHANGED, \
                           GEIS_EVENT_CLASS_UNAVAILABLE, \
                           GEIS_EVENT_GESTURE_BEGIN, \
                           GEIS_EVENT_GESTURE_UPDATE, \
                           GEIS_EVENT_GESTURE_END, \
                           GEIS_EVENT_INIT_COMPLETE, \
                           GEIS_EVENT_USER_DEFINED, \
                           GEIS_EVENT_ERROR

from _geis_bindings import GEIS_GESTURE_ATTRIBUTE_ANGLE, \
                           GEIS_GESTURE_ATTRIBUTE_ANGLE_DELTA, \
                           GEIS_GESTURE_ATTRIBUTE_ANGULAR_VELOCITY, \
                           GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_X1, \
                           GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_X2, \
                           GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_Y1, \
                           GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_Y2, \
                           GEIS_GESTURE_ATTRIBUTE_CHILD_WINDOW_ID, \
                           GEIS_GESTURE_ATTRIBUTE_DELTA_X, \
                           GEIS_GESTURE_ATTRIBUTE_DELTA_Y, \
                           GEIS_GESTURE_ATTRIBUTE_DEVICE_ID, \
                           GEIS_GESTURE_ATTRIBUTE_EVENT_WINDOW_ID, \
                           GEIS_GESTURE_ATTRIBUTE_FOCUS_X, \
                           GEIS_GESTURE_ATTRIBUTE_FOCUS_Y, \
                           GEIS_GESTURE_ATTRIBUTE_GESTURE_NAME, \
                           GEIS_GESTURE_ATTRIBUTE_POSITION_X, \
                           GEIS_GESTURE_ATTRIBUTE_POSITION_Y, \
                           GEIS_GESTURE_ATTRIBUTE_RADIAL_VELOCITY, \
                           GEIS_GESTURE_ATTRIBUTE_RADIUS, \
                           GEIS_GESTURE_ATTRIBUTE_RADIUS_DELTA, \
                           GEIS_GESTURE_ATTRIBUTE_ROOT_WINDOW_ID, \
                           GEIS_GESTURE_ATTRIBUTE_TAP_TIME, \
                           GEIS_GESTURE_ATTRIBUTE_TIMESTAMP, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_0_ID, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_0_X, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_0_Y, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_1_ID, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_1_X, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_1_Y, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_2_ID, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_2_X, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_2_Y, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_3_ID, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_3_X, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_3_Y, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_4_ID, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_4_X, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCH_4_Y, \
                           GEIS_GESTURE_ATTRIBUTE_TOUCHES, \
                           GEIS_GESTURE_ATTRIBUTE_VELOCITY_X, \
                           GEIS_GESTURE_ATTRIBUTE_VELOCITY_Y

from _geis_bindings import GEIS_FILTER_DEVICE, \
                           GEIS_FILTER_CLASS, \
                           GEIS_FILTER_REGION, \
                           GEIS_FILTER_OP_EQ, \
                           GEIS_FILTER_OP_NE, \
                           GEIS_FILTER_OP_GT, \
                           GEIS_FILTER_OP_GE, \
                           GEIS_FILTER_OP_LT, \
                           GEIS_FILTER_OP_LE

from geis.geis_v2 import Geis, Event, Filter, Subscription, NoMoreEvents

