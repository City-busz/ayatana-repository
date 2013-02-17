/**
 * @file geis/geis.h
 * This is the public interface for the GEIS gesture API.
 *
 * Copyright 2010, 2011 Canonical Ltd.
 *
 * This library is free software; you can redistribute it and/or modify it under
 * the terms of version 3 of the GNU Lesser General Public License as published
 * by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.	 See the GNU Lesser General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; if not, write to the Free Software Foundation, Inc., 51
 * Franklin St, Fifth Floor, Boston, MA  02110-1301 US
 */
#ifndef GEIS_GEIS_H_
#define GEIS_GEIS_H_

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @defgroup geis_common Common Types and Definitions
 *
 * These types and values are common to both the simplified and advanced GEIS
 * interfaces.
 */

/**
  * @defgroup geis_v1 The Simplified GEIS Interface
  *
  * The simplified GEIS interface is the original (GEIS v1) API.  It provides a
  * way to specify a list of gesture names and input devices for which gestures
  * will be recognized on a given window.
  *
  * See @ref using_geis_v1.
  */

/**
 * @defgroup geis_v2 The Advanced GEIS Interface
 *
 * The advanced GEIS interface (GEIS v2) was developed to give a more nuanced
 * control over the types of gestures and input devices for which gestures will
 * be recognized.
  *
  * See @ref using_geis_v2.
 */

/**
  * GEIS version macros
  *
  * These macros can be tested at compile time to query for support of various
  * features.
  */
#define GEIS_VERSION_1_0  1
#define GEIS_VERSION_2_0  20101122

#include <geis/geisimpl.h>

/**
 * Errors returned from calls.
 * @ingroup geis_common
 *
 * Most GEIS API calls return a status code indicating success or, in the event
 * of a lack of success, the reson for failure.
 */
typedef enum GeisStatus
{
  GEIS_STATUS_SUCCESS       = 0,    /**< normal successful completion */
  GEIS_STATUS_CONTINUE      = 20,   /**< normal successful completion
                                         with data still remaining */
  GEIS_STATUS_EMPTY         = 21,   /**< normal successful completion
                                         with no data retrieved */
  GEIS_STATUS_NOT_SUPPORTED = 10,   /**< a requested feature is not supported */
  GEIS_BAD_ARGUMENT         = 1000, /**< a bad argument value was passed */
  GEIS_UNKNOWN_ERROR        = 9999, /**< any other error condition */
  GEIS_STATUS_BAD_ARGUMENT  = -100, /**< a bad argument value was passed */
  GEIS_STATUS_UNKNOWN_ERROR = -999  /**< any other error condition */
} GeisStatus;

/**
 * Attribute data types.
 * @ingroup geis_common
 */
typedef enum GeisAttrType
{
  GEIS_ATTR_TYPE_UNKNOWN,    /**< Attr is an unknown type. */
  GEIS_ATTR_TYPE_BOOLEAN,    /**< Attr is truth-valued . */
  GEIS_ATTR_TYPE_FLOAT,      /**< Attr is real-valued. */
  GEIS_ATTR_TYPE_INTEGER,    /**< Attr is a counting number. */
  GEIS_ATTR_TYPE_POINTER,    /**< Attr is a pointer to a data structure. */
  GEIS_ATTR_TYPE_STRING      /**< Attr is a null-terminated UTF-8 string. */

} GeisAttrType;

#define GEIS_FALSE 0
#define GEIS_TRUE  1

/* Standard fundamental gestures */
#define GEIS_GESTURE_DRAG    "Drag"
#define GEIS_GESTURE_PINCH   "Pinch"
#define GEIS_GESTURE_ROTATE  "Rotate"
#define GEIS_GESTURE_TAP     "Tap"
#define GEIS_GESTURE_TOUCH   "Touch"

/* Extra higher-level gestures. */
#define GEIS_GESTURE_FLICK   "Flick"

/**
 * @defgroup geis_v1_gesture_types Gesture Types
 * @ingroup geis_v1
 *
 * The names of gesture types.  These names can be passed to 
 * geis_subscribe() in a NULL-terminated list to specify only a subset of
 * available gestures.
 */

/**
 * @defgroup geis_v1_gesture_primitives Gesture Primitives 
 * @ingroup geis_v1_gesture_types
 *
 * These are the prime gesture primitive that describes the general action of
 * the touchpoints at an instant in time.
 *
 * These are the values passed as the @p gesture_type parameter to the 
 * GeisGestureCallback.
 *
 * @{
 *
 * @def GEIS_GESTURE_PRIMITIVE_DRAG
 * A translate gesture:  dragging, swiping, flicking, moving in a generally
 * linear fashion.
 *
 * @def GEIS_GESTURE_PRIMITIVE_PINCH
 * A pinch or expand gesture:  two or more touch points generally moving toward
 * or away from a common point.
 *
 * @def GEIS_GESTURE_PRIMITIVE_ROTATE
 * A rotation gesture.  Two or more points moving relatively along an arc with a
 * commonish centre.
 *
 * @def GEIS_GESTURE_PRIMITIVE_TAP
 * A tap.  Touch down, touch up, one or more touches.
 *
 * @def GEIS_GESTURE_PRIMITIVE_TOUCH
 * A parenthetical gesture event.  Touch down (start) and up (finish).
 */
#define GEIS_GESTURE_PRIMITIVE_DRAG    0
#define GEIS_GESTURE_PRIMITIVE_PINCH   1
#define GEIS_GESTURE_PRIMITIVE_ROTATE  2
#define GEIS_GESTURE_PRIMITIVE_TAP    15 
#define GEIS_GESTURE_PRIMITIVE_TOUCH  32

/* @} */

#define GEIS_GESTURE_ID_FLICK 128

/**
 * @defgroup geis_v1_standar_gesture_types Standard Gesture Types
 * @ingroup geis_v1_gesture_types
 *
 * These gesture types should be available on all GEIS implementations.
 *
 * @{
 */

/* Gesture names for the Simplified Interface */
#define GEIS_GESTURE_TYPE_DRAG1   "Drag,touch=1"
#define GEIS_GESTURE_TYPE_DRAG2   "Drag,touch=2"
#define GEIS_GESTURE_TYPE_DRAG3   "Drag,touch=3"
#define GEIS_GESTURE_TYPE_DRAG4   "Drag,touch=4"
#define GEIS_GESTURE_TYPE_DRAG5   "Drag,touch=5"
#define GEIS_GESTURE_TYPE_PINCH1  "Pinch,touch=1"
#define GEIS_GESTURE_TYPE_PINCH2  "Pinch,touch=2"
#define GEIS_GESTURE_TYPE_PINCH3  "Pinch,touch=3"
#define GEIS_GESTURE_TYPE_PINCH4  "Pinch,touch=4"
#define GEIS_GESTURE_TYPE_PINCH5  "Pinch,touch=5"
#define GEIS_GESTURE_TYPE_ROTATE1 "Rotate,touch=1"
#define GEIS_GESTURE_TYPE_ROTATE2 "Rotate,touch=2"
#define GEIS_GESTURE_TYPE_ROTATE3 "Rotate,touch=3"
#define GEIS_GESTURE_TYPE_ROTATE4 "Rotate,touch=4"
#define GEIS_GESTURE_TYPE_ROTATE5 "Rotate,touch=5"
#define GEIS_GESTURE_TYPE_TAP1    "Tap,touch=1"
#define GEIS_GESTURE_TYPE_TAP2    "Tap,touch=2"
#define GEIS_GESTURE_TYPE_TAP3    "Tap,touch=3"
#define GEIS_GESTURE_TYPE_TAP4    "Tap,touch=4"
#define GEIS_GESTURE_TYPE_TAP5    "Tap,touch=5"
#define GEIS_GESTURE_TYPE_TOUCH1  "Touch,touch=1"
#define GEIS_GESTURE_TYPE_TOUCH2  "Touch,touch=2"
#define GEIS_GESTURE_TYPE_TOUCH3  "Touch,touch=3"
#define GEIS_GESTURE_TYPE_TOUCH4  "Touch,touch=4"
#define GEIS_GESTURE_TYPE_TOUCH5  "Touch,touch=5"

/* @} */

/**
 * @defgroup geis_v1_vendor_extensions Vendor Extension Gesture Types
 * @ingroup geis_v1_gesture_types
 *
 * Vendor-specific extensions to the GEIS v1 API.
 *
 * @{
 */

/**
 * A special gesture type than enabled system-wide gesture priority.
 */
#define GEIS_GESTURE_TYPE_SYSTEM  "Sysflags"

#define GEIS_GESTURE_TYPE_FLICK1  "Flick,touch=1"
#define GEIS_GESTURE_TYPE_FLICK2  "Flick,touch=2"
#define GEIS_GESTURE_TYPE_FLICK3  "Flick,touch=3"
#define GEIS_GESTURE_TYPE_FLICK4  "Flick,touch=4"
#define GEIS_GESTURE_TYPE_FLICK5  "Flick,touch=5"

/* @} */

/**
 * @name Standard fundamental gesture attributes
 *
 * @{
 *
 * @def GEIS_GESTURE_ATTRIBUTE_ANGLE
 * Angle covered by a gesture since it has started, in radians, counterclockwise.
 * Its value ranges from -pi to pi.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_ANGLE_DELTA
 * Angle covered by a gesture since its last update, in radians,
 * counterclockwise.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_CENTROID_X
 * This attribute provides the X coordinate of the centroid of the
 * non-self-intersecting closed polygon defined by the touch points of the
 * gesture, in device coordinates.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_CENTROID_Y
 * This attribute provides the Y coordinate of the centroid of the
 * non-self-intersecting closed polygon defined by the touch points of the
 * gesture, in device coordinates.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_FOCUS_X
 * This attribute provides the X coordinate of the focus point of a gesture,
 * in screen coordinates.
 * For direct devices (GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH is GEIS_TRUE) it's
 * the centroid point. For indirect devices it's the pointer/cursor position.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_FOCUS_Y
 * This attribute provides the Y coordinate of the focus point of a gesture,
 * in screen coordinates.
 * For direct devices (GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH is GEIS_TRUE) it's
 * the centroid point. For indirect devices it's the pointer/cursor position.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_GESTURE_NAME
 * Name of the gesture.
 * This attribute is filled only when using GEIS v1 API (the simplified
 * interface). On GEIS v2 this attribute has been replaced by the concept of
 * gesture classes. Use geis_frame_is_class() instead.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_POSITION_X
 * This attribute provides the X coordinate of the position of a gesture, in
 * device coordinates. It's the same as the centroid of a gesture. See
 * GEIS_GESTURE_ATTRIBUTE_CENTROID_X.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_POSITION_Y
 * This attribute provides the Y coordinate of the position of a gesture, in
 * device coordinates. It's the same as the centroid of a gesture. See
 * GEIS_GESTURE_ATTRIBUTE_CENTROID_Y.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_0_ID
 * This attribute provides the ID of the touch at index0.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_0_X
 * This attribute provides the X coordinate of the touch at index0.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_0_Y
 * This attribute provides the Y coordinate of the touch at index0.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_1_ID
 * This attribute provides the ID of the touch at index1.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_1_X
 * This attribute provides the X coordinate of the touch at index1.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_1_Y
 * This attribute provides the Y coordinate of the touch at index1.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_2_ID
 * This attribute provides the ID of the touch at index2.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_2_X
 * This attribute provides the X coordinate of the touch at index2.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_2_Y
 * This attribute provides the Y coordinate of the touch at index2.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_3_ID
 * This attribute provides the ID of the touch at index3.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_3_X
 * This attribute provides the X coordinate of the touch at index3.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_3_Y
 * This attribute provides the Y coordinate of the touch at index3.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_4_ID
 * This attribute provides the ID of the touch at index4.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_4_X
 * This attribute provides the X coordinate of the touch at index4.
 * Only used by GEIS v1 API.
 *
 * @def GEIS_GESTURE_ATTRIBUTE_TOUCH_4_Y
 * This attribute provides the Y coordinate of the touch at index4.
 * Only used by GEIS v1 API.
 */
#define GEIS_GESTURE_ATTRIBUTE_ANGLE            "angle"
#define GEIS_GESTURE_ATTRIBUTE_ANGLE_DELTA      "angle delta"
#define GEIS_GESTURE_ATTRIBUTE_ANGULAR_VELOCITY "angular velocity"
#define GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_X1   "boundingbox x1"
#define GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_Y1   "boundingbox y1"
#define GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_X2   "boundingbox x2"
#define GEIS_GESTURE_ATTRIBUTE_BOUNDINGBOX_Y2   "boundingbox y2"
#define GEIS_GESTURE_ATTRIBUTE_CHILD_WINDOW_ID  "child window id"
#define GEIS_GESTURE_ATTRIBUTE_CENTROID_X       "centroid x"
#define GEIS_GESTURE_ATTRIBUTE_CENTROID_Y       "centroid y"
#define GEIS_GESTURE_ATTRIBUTE_DELTA_X          "delta x"
#define GEIS_GESTURE_ATTRIBUTE_DELTA_Y          "delta y"
#define GEIS_GESTURE_ATTRIBUTE_DEVICE_ID        "device id"
#define GEIS_GESTURE_ATTRIBUTE_EVENT_WINDOW_ID  "event window id"
#define GEIS_GESTURE_ATTRIBUTE_FOCUS_X          "focus x"
#define GEIS_GESTURE_ATTRIBUTE_FOCUS_Y          "focus y"
#define GEIS_GESTURE_ATTRIBUTE_GESTURE_NAME     "gesture name"
#define GEIS_GESTURE_ATTRIBUTE_POSITION_X       "position x"
#define GEIS_GESTURE_ATTRIBUTE_POSITION_Y       "position y"
#define GEIS_GESTURE_ATTRIBUTE_RADIAL_VELOCITY  "radial velocity"
#define GEIS_GESTURE_ATTRIBUTE_RADIUS_DELTA     "radius delta"
#define GEIS_GESTURE_ATTRIBUTE_RADIUS           "radius"
#define GEIS_GESTURE_ATTRIBUTE_ROOT_WINDOW_ID   "root window id"
#define GEIS_GESTURE_ATTRIBUTE_TAP_TIME         "tap time"
#define GEIS_GESTURE_ATTRIBUTE_TIMESTAMP        "timestamp"
#define GEIS_GESTURE_ATTRIBUTE_TOUCHES          "touches"
#define GEIS_GESTURE_ATTRIBUTE_VELOCITY_X       "velocity x"
#define GEIS_GESTURE_ATTRIBUTE_VELOCITY_Y       "velocity y"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_0_ID       "touch 0 id"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_0_X        "touch 0 x"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_0_Y        "touch 0 y"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_1_ID       "touch 1 id"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_1_X        "touch 1 x"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_1_Y        "touch 1 y"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_2_ID       "touch 2 id"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_2_X        "touch 2 x"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_2_Y        "touch 2 y"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_3_ID       "touch 3 id"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_3_X        "touch 3 x"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_3_Y        "touch 3 y"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_4_ID       "touch 4 id"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_4_X        "touch 4 x"
#define GEIS_GESTURE_ATTRIBUTE_TOUCH_4_Y        "touch 4 y"
/* @} */

/**
 * @defgroup geis_meta Initialization and Cleanup
 * @ingroup geis_v1
 *
 * Each instance of a gesture subscription must be created using the geis_init()
 * call and destroyed using the geis_finish() call.
 *
 * A particular subscription instance is associated with a display region.  The
 * nature of the display region depends on the underlying display technology.
 * For example, an X11 window or even a subregion of an X11 window could be an
 * associated display region when geis is layered over X11 technology.
 *
 * The nature of the display desciption information depends on the actual
 * underlyinggeis implementation and is documented separately.  The
 * implementation-specific description must be passed to geis_init using a 
 * GeisWinInfo structure.
 *
 * @{
 */

/**
 * @class GeisInstance
 * A geis gesture subscription instance.
 */
/** @cond typedef */
typedef struct _GeisInstance *GeisInstance;
/** @endcond */

/**
 * @class GeisWinInfo
 * Generic display region description block
 */
typedef struct GeisWinInfo
{
  uint32_t win_type;    /**< Selects the implementation-specific window type. */
  void    *win_info;    /**< Additional info dependent on the window type. */
} GeisWinInfo;

/**
 * Initializes a geis subscription instance for a display region.
 * @memberof GeisInstance
 *
 * @param[in]  win_info         a display region description block
 *                              -- see geis implementtaion documentation
 * @param[out] geis_instance    an opaque pointer to a geis gesture subscription
 *                              instance
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid GeisWinInfo was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_init(GeisWinInfo *win_info, GeisInstance *geis_instance);

/**
 * Cleans up a geis subscription instance for a display region.
 * @memberof GeisInstance
 *
 * @param[in] geis_instance     an opaque pointer to a geis gesture subscription
 *                              instance
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid GeisInstance was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_finish(GeisInstance  geis_instance);

/* @} */

/**
 * @defgroup geis_v1_config Configuration and Control
 * @ingroup geis_v1
 * @{
 */

/**
 * Gets the Unix file descriptor for GEIS events.
 *
 * Applications or toolkits can use this file descriptor to intgerate geis event
 * handling into their main event dispatch loop.  When a GEIS event is available
 * for processing, the fd will have a read-available state indicated in
 * select(), poll(), epoll(), etc.
 */
#define GEIS_CONFIG_UNIX_FD 10001

/**
 * Indicates if a particular feaure is supported.
 *
 * @param[in] geis_instance      An opaque pointer to a geis gesture subscription
 *                               instance.
 * @param[in] configuration_item Indicates which configuration item will be
 *                               checked for support.
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid argument value was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_configuration_supported(GeisInstance geis_instance,
                                                 int          configuration_item);

/**
 * Gets a feature configuration value.
 *
 * @param[in] geis_instance      An opaque pointer to a geis gesture subscription
 *                               instance.
 * @param[in] configuration_item Indicates which configuration item will be
 *                               get.
 * @param[in] value              A pointer to where the retrieved value will be
 *                               stored.
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid argument value was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_configuration_get_value(GeisInstance geis_instance, 
                                                 int          configuration_item,
                                                 void         *value);

/**
 * Sets a feature configuration value.
 *
 * @param[in] geis_instance      An opaque pointer to a geis gesture subscription
 *                               instance.
 * @param[in] configuration_item Indicates which configuration item will be
 *                               set.
 * @param[in] value              A pointer to where the value to be set will be
 *                               read.
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid argument value was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_configuration_set_value(GeisInstance geis_instance,
                                                 int          configuration_item, 
                                                 void         *value);

/**
 * Dispatches geis events until there are no further events available.
 *
 * @param[in] geis_instance     an opaque pointer to a geis gesture subscription
 *                              instance
 *
 * This function is used to integrate geis even dispatch into the main event
 * loop of an application or toolkit.
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid GeisInstance was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_event_dispatch(GeisInstance geis_instance);

/* @} */

/**
 * @defgroup geis_v2_geis The Geis API Object
 * @ingroup geis_v2
 *
 * @{
 */

/**
 * @class Geis
 * Represents an instance of the gesture recognition engine
 */
/** @cond typedef */
typedef struct _Geis *Geis;
/** @endcond */

/**
 * @name Standard Initialization Arguments
 *
 * @par
 * These initialization arguments are defined by the GEIS v2 specification.
 *
 * @{
 *
 * @def GEIS_INIT_SERVICE_PROVIDER
 * Enables GEIS to provide a networked service.
 * This initialization argument takes no parameters.
 *
 * @def GEIS_INIT_TRACK_DEVICES
 * Tells GEIS to send input device events.
 * This initialization argument takes no parameters.
 *
 * @def GEIS_INIT_TRACK_GESTURE_CLASSES
 * Tells GEIS to send gesture class events.
 * This initialization argument takes no parameters.
 *
 * @def GEIS_INIT_SYNCHRONOUS_START
 * Performs all setup synchronously: geis_new() will block until all setup has
 * completed successfully or unsuccessfully.
 */

#define GEIS_INIT_SERVICE_PROVIDER     "org.libgeis.init.server"
#define GEIS_INIT_TRACK_DEVICES        "org.libgeis.init.track-devices"
#define GEIS_INIT_TRACK_GESTURE_CLASSES  "org.libgeis.init.track-gesture-classes"
#define GEIS_INIT_SYNCHRONOUS_START      "org.libgeis.init.synchronous-start"

/* @} */

/**
 * @name Vendor-defined Initialization Arguments
 *
 * @par
 * These initialization arguments are not a part of the GEIS specification and
 * may change.
 *
 * @{
 *
 * @def GEIS_INIT_DBUS_BACKEND
 * Uses the DBus back end (default).
 *
 * @def GEIS_INIT_GRAIL_BACKEND
 * Uses the native grail back end (fallback).
 *
 * @def GEIS_INIT_XCB_BACKEND
 * Uses the grail-embedded-in-X11 back end.
 *
 * @def GEIS_INIT_NO_ATOMIC_GESTURES
 * Disables the use of (GEIS v1-style) atomic gestures:  only a single gesture
 * is recognized at a time.
 *
 * @def GEIS_INIT_SEND_TENTATIVE_EVENTS
 * Causes tentative events to be sent.  Tentative events indicate gestures may
 * possibly be detected soon and allow early rejection if the events occur
 * outside any area of interest.
 *
 * @def GEIS_INIT_SEND_SYNCHRONOS_EVENTS
 * Causes all gesture events to be sent, even if there is zero apparent time
 * difference between the events.  Normally all but the first consecutive event
 * are discarded, since velocity values can not be calculated and multiple
 * events between frame redraws are unlikely do have any value beyong consuming
 * CPU.  Setting this init value will give the events to you if you really want
 * them.
 */

#define GEIS_INIT_DBUS_BACKEND           "com.canonical.oif.backend.dbus"
#define GEIS_INIT_GRAIL_BACKEND          "com.canonical.oif.backend.grail"
#define GEIS_INIT_XCB_BACKEND            "com.canonical.oif.backend.xcb"
#define GEIS_INIT_NO_ATOMIC_GESTURES     "com.canonical.oif.no-atomic.gestures"
#define GEIS_INIT_SEND_TENTATIVE_EVENTS  "com.canonical.oif.events.tentative"
#define GEIS_INIT_SEND_SYNCHRONOS_EVENTS "com.canonical.oif.events.synchronous"
/* @} */


/**
 * Initializes an instance of the GEIS v2.0 API.
 * @ingroup geis_v2_geis
 * @memberof Geis
 *
 * @param[in]  init_arg_name  The name of an initializaer argument.
 * @param[in]  ...            The remaining initializaer arguments.
 *
 * A NULL-terminated list of zero or more initialization arguments is passed to
 * this function to create and initialize a connection to a gesture recognition
 * engine.
 *
 * If no initialization arguments are passed, the parameter list consists of a
 * single NULL argument.
 */
GEIS_API GEIS_VARARG Geis geis_new(GeisString init_arg_name, ...);

/**
 * Cleans up an instance of the GEIS v2.0 API.
 * @ingroup geis_v2_geis
 * @memberof Geis
 *
 * @param[in] geis  An instance of the GEIS v2.0 API.
 *
 * Tears down the instance of the API and releases any resources associated with
 * that instance.
 */
GEIS_API GeisStatus geis_delete(Geis geis);

/* @} */

/**
 * @defgroup geis_v2_error Error Reporting
 * @ingroup geis_v2
 * @{
 */

/**
 * Gets the number of status codes in the error stack.
 *
 * @param[in] geis A GEIS API instance or NULL for the global stack
 *
 * This function is used primarily to determine the failure details of a GEIS
 * function that does not explicitly return a GeisStatus value.  This is
 * required for _new() fucntions that return NULL to indicate failure.  If the
 * call to geis_new() itself fails and returns a NULL, the global error stack
 * must be used, otherwise the API instance error stack must be used.
 *
 * The error stack is reset on each GEIS API call, so failure reasons should be
 * determined immmediately after a GEIS API call.
 */
GEIS_API GeisSize geis_error_count(Geis geis);

/**
 * Gets the indicated status code from the error stack.
 *
 * @param[in] geis  A GEIS API instance or NULL for the global stack
 * @param[in] index Indicates the status value to retrieve.  Valid status values
 *                  are between 0 and less than the value returned from
 *                  geis_error_count() otherwise GEIS_STATUS_BAD_ARGUMENT will
 *                  be returned.
 */
GEIS_API GeisStatus geis_error_code(Geis geis, GeisSize index);

/**
 * Gets the localized error message, if any, associated with the indicated
 * error.
 *
 * @param[in] geis  A GEIS API instance or NULL for the global stack
 * @param[in] index Indicates the status value to retrieve.  Valid status values
 *                  are between 0 and less than the value returned from
 *                  geis_error_count() otherwise GEIS_STATUS_BAD_ARGUMENT will
 *                  be returned.
 */
GEIS_API GeisString geis_error_message(Geis geis, GeisSize index);

/* @} */

/**
 * @defgroup geis_v2_config Configuration
 * @ingroup geis_v2
 * @{
 */

/**
 * @name Required Configuration Items
 *
 * @par
 * These configuration items are defined by the GEIS specification.
 *
 * @{
 *
 * @def GEIS_CONFIGURATION_FD
 * Gets a Unix file descriptor that will signal the availablility of GEIS events
 * for processing.
 */

#define GEIS_CONFIGURATION_FD "org.libgeis.configuration.fd"

/* @} */

/**
 * @name Vendor-defined Configuration Items
 *
 * @par
 * These configuration items are not a part of the GEIS specification and may
 * change.
 *
 * @{
 *
 * @def GEIS_CONFIG_MAX_EVENTS
 */

#define GEIS_CONFIG_MAX_EVENTS  "com.canonical.oif.max_events"

/**
 * @def GEIS_CONFIG_ATOMIC_GESTURES
 * Indicates if atomic gestures are in use.  Value type GeisBoolean.
 */
#define GEIS_CONFIG_ATOMIC_GESTURES "com.canonical.use.atomic.gestures"

/**
 * @def GEIS_CONFIG_SEND_TENTATIVE_EVENTS
 * See GEIS_INIT_SEND_TENTATIVE_EVENTS
 */
#define GEIS_CONFIG_SEND_TENTATIVE_EVENTS  "com.canonical.oif.events.tentative"

/**
 * @def GEIS_CONFIG_SEND_SYNCHRONOS_EVENTS
 * See GEIS_INIT_SEND_SYNCHRONOS_EVENTS
 */
#define GEIS_CONFIG_SEND_SYNCHRONOS_EVENTS "com.canonical.oif.events.synchronous"

/**
 * @def GEIS_CONFIG_DRAG_THRESHOLD
 * Movement threshold for recognizing a DRAG gesture (in meters).  Value type
 * GeisFloat.
 */
#define GEIS_CONFIG_DRAG_THRESHOLD "com.canonical.oif.drag.threshold"

/**
 * @def GEIS_CONFIG_DRAG_TIMEOUT
 * Timeout for recognizing a DRAG gesture (in milliseconds).  Value type
 * GeisInteger.
 */
#define GEIS_CONFIG_DRAG_TIMEOUT "com.canonical.oif.drag.timeout"

/**
 * @def GEIS_CONFIG_PINCH_THRESHOLD
 * Movement threshold for recognizing a PINCH gesture (in meters).  Value type
 * GeisFloat.
 */
#define GEIS_CONFIG_PINCH_THRESHOLD "com.canonical.oif.pinch.threshold"

/**
 * @def GEIS_CONFIG_PINCH_TIMEOUT
 * Timeout for recognizing a PINCH gesture (in milliseconds).  Value type
 * GeisInteger.
 */
#define GEIS_CONFIG_PINCH_TIMEOUT "com.canonical.oif.pinch.timeout"

/**
 * @def GEIS_CONFIG_ROTATE_THRESHOLD
 * Movement threshold for recognizing a ROTATE gesture (in meters).  Value type
 * GeisFloat.
 */
#define GEIS_CONFIG_ROTATE_THRESHOLD "com.canonical.oif.rotate.threshold"

/**
 * @def GEIS_CONFIG_ROTATE_TIMEOUT
 * Timeout for recognizing a ROTATE gesture (in milliseconds).  Value type
 * GeisInteger.
 */
#define GEIS_CONFIG_ROTATE_TIMEOUT "com.canonical.oif.rotate.timeout"

/**
 * @def GEIS_CONFIG_TAP_THRESHOLD
 * Movement threshold for recognizing a TAP gesture (in meters).  Value type
 * GeisFloat.
 */
#define GEIS_CONFIG_TAP_THRESHOLD "com.canonical.oif.tap.threshold"

/**
 * @def GEIS_CONFIG_TAP_TIMEOUT
 * Timeout for recognizing a TAP gesture (in milliseconds).  Value type
 * GeisInteger.
 */
#define GEIS_CONFIG_TAP_TIMEOUT "com.canonical.oif.tap.timeout"

/* @} */

/**
 * Gets a feature configuration value.
 *
 * @param[in]  geis                     An opaque GEIS API object.
 * @param[in]  configuration_item_name  Selects the configuration value to return.
 * @param[out] configuration_item_value Points to a buffer to contain the output
 *                                      value.  The actual type of this buffer
 *                                      depends on the
 *                                      @p configuration_value_name.
 *
 * @retval GEIS_STATUS_BAD_ARGUMENT   an invalid argument value was passed
 * @retval GEIS_STATUS_NOT_SUPPORTED  the configuration value is not supported
 * @retval GEIS_STATUS_SUCCESS        normal successful completion
 */
GEIS_API GeisStatus geis_get_configuration(Geis        geis, 
                                           GeisString  configuration_item_name,
                                           void       *configuration_item_value);

/**
 * Sets a feature configuration value.
 *
 * @param[in] geis                     An opaque GEIS API object.
 * @param[in] configuration_item_name  Selects the configuration value to return.
 * @param[in] configuration_item_value Points to a buffer to contain the output
 *                                     configuration value.  The actual type of
 *                                     this buffer depends on the
 *                                     @p configuration_value_name.
 *
 * @retval GEIS_STATUS_BAD_ARGUMENT   an invalid argument value was passed
 * @retval GEIS_STATUS_NOT_SUPPORTED  the configuration value is not supported
 * @retval GEIS_STATUS_SUCCESS        normal successful completion
 */
GEIS_API GeisStatus geis_set_configuration(Geis        geis,
                                           GeisString  configuration_item_name, 
                                           void       *configuration_item_value);

/* @} */

/**
 * @defgroup geis_v1_input Input Devices
 * @ingroup geis_v1
 * @{
 */

typedef unsigned int GeisInputDeviceId;

#define GEIS_ALL_INPUT_DEVICES ((GeisInputDeviceId)0)

/**
 * Prototype for input device callback functions.
 */
typedef void (*GeisInputCallback)(void             *cookie,
                                  GeisInputDeviceId device_id,
                                  void             *attrs);

/**
 * Callback functions used to handle changes in the available input devices.
 */
typedef struct GeisInputFuncs
{
  GeisInputCallback  added;   /**< Receives new input device notices */
  GeisInputCallback  changed; /**< Receives modified input device notices */
  GeisInputCallback  removed; /**< Receives removes input device notices */

} GeisInputFuncs;


/**
 * Registers a callback to receive information on input devices.
 *
 * @param[in] geis_instance   points to a geis gesture subscription
 *                            instance
 * @param[in] func            points to a GeisInputFuncs table
 * @param[in] cookie          an application specific value to be passed to
 *                            the callback
 *
 * The callback is called for each gesture-capable input device available for
 * the display region associated with the geis subscription instance.  Over
 * time, as gesture-capable input devices appear and disappear or change their
 * abilities or configuration, the callback may be called again.
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid argument value was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_input_devices(GeisInstance    geis_instance,
                                       GeisInputFuncs *func,
                                       void           *cookie);

/* @} */

/**
 * @defgroup geis_v1_subscription Gesture Subscription
 * @ingroup geis_v1
 * @{
 */
typedef unsigned int GeisGestureType;
typedef unsigned int GeisGestureId;

/** Selects ALL input devices. */
#define GEIS_ALL_GESTURES ((GeisGestureType)0)

#define GEIS_NO_GESTURE_ID ((GeisGestureId)0)

/**
 * An individual gesture attribute.
 *
 * Gesture events are associated with a list of attributes, each of which is a
 * (name, type, value) tuple.  These attribute reveal a little piece of
 * information about a gesture.
 */
typedef struct GeisGestureAttr
{
  /** The name of the gesture attribute. */
  GeisString name;
  /** The data type of the gesture attribute. */
  GeisAttrType type;
  /** The value of the attributes. */
  __extension__ union
  {
    GeisBoolean boolean_val;
    GeisFloat   float_val;
    GeisInteger integer_val;
    GeisString  string_val;
  };
} GeisGestureAttr;

/**
 * A callback used for different gesture events.
 *
 * @param[in] cookie         an application-specific value to be passed to the
 *                           callback.
 * @param[in] gesture_type   a gesture type
 * @param[in] gesture_id     a unique gesture identifier
 * @param[in] attrs          parameters
 */
typedef void (*GeisGestureCallback)(void             *cookie,
                                    GeisGestureType   gesture_type,
                                    GeisGestureId     gesture_id,
                                    GeisSize          attr_count,
                                    GeisGestureAttr  *attrs);

/**
 * The set of callback functions invoked for various gesture-related events.
 *
 * An application must define callback functions to handle the various gesture
 * events.  These callbacks are provided in a table passed to geis_subscribe for
 * each window on which gesture events may occur.
 */
typedef struct GeisGestureFuncs
{
  /** Invoked when a new gesture type has been defined. */
  GeisGestureCallback  added;
  /** Invoked when a defined gesture type is no longer available. */
  GeisGestureCallback  removed;
  /** Invoked when a new gesture starts. */
  GeisGestureCallback  start;
  /** Invoked when a gesture has changed values. */
  GeisGestureCallback  update;
  /** Invoked when a gesture finishes. */
  GeisGestureCallback  finish;
} GeisGestureFuncs;


/**
 * Registers a callback to receive gesture events.
 *
 * @param[in] geis_instance     an opaque pointer to a geis gesture subscription
 *                              instance
 * @param[in] input_list        a null-terminated list of input device IDs
 * @param[in] gesture_list      a null-terminated list of C-style strings naming
 *                              gestures for subscription
 * @param[in] funcs             a pointer to a GeisGestureFuncs structure
 * @param[in] cookie            an application specific value to be passed to
 *                              the callback
 *
 * @retval GEIS_BAD_ARGUMENT    an invalid argument value was passed
 * @retval GEIS_STATUS_SUCCESS  normal successful completion
 */
GEIS_API GeisStatus geis_subscribe(GeisInstance         geis_instance,
                                   GeisInputDeviceId   *input_list,
                                   const char*         *gesture_list,
                                   GeisGestureFuncs    *funcs,
                                   void                *cookie);

/**
 * Unsubscribes to one or more gestures.
 *
 * @param[in] geis_instance     an opaque pointer to a geis gesture subscription
 *                              instance
 * @param[in] gesture_list      a null-terminated list of gesture types
 */
GEIS_API GeisStatus geis_unsubscribe(GeisInstance     geis_instance,
                                     GeisGestureType *gesture_list);

/* @} */

/**
 * @defgroup geis_v2_attrs Attributes
 * @ingroup geis_v2
 *
 * Attributes are named values associated with various GEIS entities, including
 * input devices, gesture types, and gesture events.
 *
 * @{
 */

/**
 * An opaque type that encapsulates a GEIS attribute.
 *
 * GeisAttr objects may not be created or destroyed by the application, they may
 * only have their data examined or extracted.
 */
/** @cond typedef */
typedef struct _GeisAttr *GeisAttr;
/** @endcond */

/**
 * Gets the name of an attribute.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisString geis_attr_name(GeisAttr attr);

/**
 * Gets the type of an attribute value.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisAttrType geis_attr_type(GeisAttr attr);

/**
 * Gets the value of an attribute as a GeisBoolean.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisBoolean geis_attr_value_to_boolean(GeisAttr attr);

/**
 * Gets the value of an attribute as a GeisFloat.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisFloat geis_attr_value_to_float(GeisAttr attr);

/**
 * Gets the value of an attribute as a GeisInteger.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisInteger geis_attr_value_to_integer(GeisAttr attr);

/**
 * Gets the value of an attribute as a GeisPointer.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisPointer geis_attr_value_to_pointer(GeisAttr attr);

/**
 * Gets the value of an attribute as a GeisString.
 *
 * @param[in] attr  Identifies the attribute.
 */
GEIS_API GeisString geis_attr_value_to_string(GeisAttr attr);

/* @} */

/**
 * @defgroup geis_v2_event_control Event Control
 * @ingroup geis_v2
 *
 * These functions are used to dispatch events generated from the various other
 * GEIS components.
 *
 * Applications must invoke geis_dispatch_events() from time to time to generate
 * input device, gesture type, and gesture events.  The GEIS events are then
 * retrieved either from the internal event queue using the geis_next_event()
 * call or through an application-supplied callback set through the
 * geis_register_event_callback() call.
 *
 * @{
 */

typedef enum _GeisEventType
{ 
  GEIS_EVENT_DEVICE_AVAILABLE         = 1000,
  GEIS_EVENT_DEVICE_UNAVAILABLE       = 1010,
  GEIS_EVENT_CLASS_AVAILABLE          = 2000,
  GEIS_EVENT_CLASS_CHANGED            = 2005,
  GEIS_EVENT_CLASS_UNAVAILABLE        = 2010,
  GEIS_EVENT_GESTURE_BEGIN            = 3000,
  GEIS_EVENT_GESTURE_UPDATE           = 3010,
  GEIS_EVENT_GESTURE_END              = 3020,
  GEIS_EVENT_TENTATIVE_BEGIN          = 3500,
  GEIS_EVENT_TENTATIVE_UPDATE         = 3510,
  GEIS_EVENT_TENTATIVE_END            = 3520,
  GEIS_EVENT_INIT_COMPLETE            = 4000,
  GEIS_EVENT_USER_DEFINED             = 6000,
  GEIS_EVENT_ERROR                    = 7000
} GeisEventType;

/**
 * @class GeisEvent
 * A generic GEIS event.
 *
 * Applications must determine the type of the actual event and convert the
 * opaque pointer to a concrete event pointer, if required.
 *
 * Events are created by the GEIS API but must be destroyed by the application.
 */
/** @cond typedef */
typedef struct _GeisEvent *GeisEvent;
/** @endcond */

/**
 * Destroys a GeisEvent.
 * @memberof GeisEvent
 *
 * @param[in] event The GeisEvent to destroy.
 */
GEIS_API void geis_event_delete(GeisEvent event);

/**
 * Gets the type of the event.
 * @memberof GeisEvent
 *
 * @param[in] event The GeisEvent to destroy.
 */
GEIS_API GeisEventType geis_event_type(GeisEvent event);

/**
 * Gets the number of attributes in the event.
 * @memberof GeisEvent
 *
 * @param[in] event The GeisEvent.
 */
GEIS_API GeisSize geis_event_attr_count(GeisEvent event);

/**
 * Gets an indicated attribute from the event.
 * @memberof GeisEvent
 *
 * @param[in] event  The GeisEvent.
 * @param[in] index  Indicates the attribute to retrieve.
 */
GEIS_API GeisAttr geis_event_attr(GeisEvent event, GeisSize index);

/**
 * Gets a named attribute from the event.
 * @memberof GeisEvent
 *
 * @param[in] event     The GeisEvent.
 * @param[in] attr_name The name of the attribute to retrieve.
 */
GEIS_API GeisAttr geis_event_attr_by_name(GeisEvent event, GeisString attr_name);

/**
 * The application callback type for the event dispatcher.
 *
 * @param[in] geis    the GEIS API instance
 * @param[in] event   the opaque event pointer
 * @param[in] context the application-supplied context value
 */
typedef void (*GeisEventCallback)(Geis geis, GeisEvent event, void *context);

/**
 * A special constant indicating the use of the default event callback.
 */
#define GEIS_DEFAULT_EVENT_CALLBACK ((GeisEventCallback)0)

/**
 * Registers an event-handler callback.
 *
 * @param[in] geis           the GEIS API instance
 * @param[in] event_callback the callback to register
 * @param[in] context        the caller context
 *
 * This function registers the callback to be executed whenever a new GeisEvent
 * is generated.  The default function pushes the GeisEvent onto an internal
 * queue to be picked up by a call to geis_next_event().
 *
 * Calling geis_register_event_callback() with a callback of
 * GEIS_DEFAULT_EVENT_CALLBACK replaces any registered function wit hthe default
 * function.
 *
 * The callback is executed in the same thread context as the one
 * geis_dispatch_events() is called from.
 */
GEIS_API void geis_register_event_callback(Geis               geis,
                                           GeisEventCallback  event_callback,
                                           void              *context);

/**
 * Pumps the GEIS event loop.
 *
 * @param[in]  geis  The GEIS API instance.
 *
 * Processes input events until there are no more input events to process and
 * generates zero or more gesture events, reporting them via the user-supplied
 * callback or pushing them on the internal event queue for retrieval via the
 * geis_next_event() call.
 *
 * @retval GEIS_STATUS_SUCCESS       The event loop was successfully pumped and
 *                                   no further events remain to be processed at
 *                                   this time.
 *
 * @retval GEIS_STATUS_CONTINUE      The event loop was successfully pumped but
 *                                   the system detected there are events
 *                                   still remaining to be processed.
 *
 * @retval GEIS_STATUS_UNKNOWN_ERROR Some error occurred
 */
GEIS_API GeisStatus geis_dispatch_events(Geis geis);

/**
 * Retrieves the next queued GEIS event.
 *
 * @param[in]  geis  The GEIS API instance.
 * @param[out] event The GeisEvent retrieved, if any.
 *
 * Pulls the next available GeisEvent from the internal event queue, if any, and
 * indicates whether there are more events left.
 *
 * @retval GEIS_STATUS_SUCCESS       An event was successfully pulled from the
 *                                   queue and the queue is now empty.
 *
 * @retval GEIS_STATUS_CONTINUE      An event was successfully pulled from the
 *                                   queue and one or more events remain in the
 *                                   queue.
 *
 * @retval GEIS_STATUS_EMPTY         No event was pulled from the queue because
 *                                   it is empty.  The value of *event remains
 *                                   unchanged.
 *
 * @retval GEIS_STATUS_UNKNOWN_ERROR Some error occurred
 */
GEIS_API GeisStatus geis_next_event(Geis geis, GeisEvent *event);

/* @} */

/**
 * @defgroup geis_v2_device Input Devices
 * @ingroup geis_v2
 * @{
 */

/**
 * @name Device Event Attributes
 * @{
 *
 * @def GEIS_EVENT_ATTRIBUTE_DEVICE
 * The event attribute containing a pointer to a GeisDevice.
 *
 * The GEIS_EVENT_DEVICE_AVAILABLE and GEIS_EVENT_DEVICE_UNAVAILABLE events
 * should have a GEIS_ATTR_TYPE_POINTER attribute with this name.  It
 * should contain a pointer to a GeisDevice describing the device made available
 * or unavailable.
 */
#define GEIS_EVENT_ATTRIBUTE_DEVICE             "device"

/* @} */

/**
 * @name Device Attributes
 * @{
 *
 * @def GEIS_DEVICE_ATTRIBUTE_NAME
 * The name of the input device.  Not guaranteed unique.
 *
 * The attribute value is of type GeisString.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_ID
 * The unique integer ID of the device.  Guaranteed unique within a Geis
 * instance.
 *
 * The attribute values is of type GeisInteger.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_TOUCHES
 * The maximum number of touches a device is capable of reporting.
 * This integer is the number if simultaneous touches the device claims to be
 * able to detect if it is a multi-touch device.  A value of zero indicates the
 * maximum number of touches can not be determined.
 *
 * The attribute value is of type GeisInteger.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH
 * Indicates the device is a direct touch device.
 * The present of this boolean attribute with a value of GEIS_TRUE indicates the
 * device is a direct touch multi-touch device (for example, a touchscreen),
 * otherwise it is an indirect touch device (such as a touchpad) or not a touch
 * device at all.
 *
 * The attribute value is of type GeisBoolean.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_INDEPENDENT_TOUCH
 * Indicates the device is an independent touch device.
 * The presence of this boolean attribute with a value of GEIS_TRUE indicates
 * the device is an independent touch device (for example, an Apple MagicMouse).
 * Other multi-touch devices should report GEIS_FALSE.
 *
 * The attribute value is of type GeisBoolean.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_MIN_X
 * The lower bound of the X-axis (nominally horizontal) coordinate values
 * reported by the device.
 *
 * The attribute values is of type GeisFloat.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_MAX_X
 * The upper bound of the X-axis (nominally horizontal) coordinate values
 * reported by the device.
 *
 * The attribute values is of type GeisFloat.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_RES_X
 * The resolution of the X-axis (nominally horizontal) coordinate values
 * reported by the device.
 *
 * The attribute values is of type GeisFloat.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_MIN_Y
 * The lower bound of the Y-axis (nominally vertical) coordinate values
 * reported by the device.
 *
 * The attribute values is of type GeisFloat.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_MAX_Y
 * The upper bound of the Y-axis (nominally vertical) coordinate values
 * reported by the device.
 *
 * The attribute values is of type GeisFloat.
 *
 * @def GEIS_DEVICE_ATTRIBUTE_RES_Y
 * The resolution of the Y-axis (nominally vertical) coordinate values
 * reported by the device.
 *
 * The attribute values is of type GeisFloat.
 */
#define GEIS_DEVICE_ATTRIBUTE_NAME              "device name"
#define GEIS_DEVICE_ATTRIBUTE_ID                "device id"
#define GEIS_DEVICE_ATTRIBUTE_TOUCHES           "device touches"
#define GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH      "direct touch"
#define GEIS_DEVICE_ATTRIBUTE_INDEPENDENT_TOUCH "independent touch"
#define GEIS_DEVICE_ATTRIBUTE_MIN_X             "device X minimum"
#define GEIS_DEVICE_ATTRIBUTE_MAX_X             "device X maximum"
#define GEIS_DEVICE_ATTRIBUTE_RES_X             "device X resolution"
#define GEIS_DEVICE_ATTRIBUTE_MIN_Y             "device Y minimum"
#define GEIS_DEVICE_ATTRIBUTE_MAX_Y             "device Y maximum"
#define GEIS_DEVICE_ATTRIBUTE_RES_Y             "device Y resolution"

/* @} */

/**
 * @class GeisDevice
 * A gesture-capable input device.
 *
 * GeisDevice objects are created by the GEIS API and are reference counted.
 */
/** @cond typedef */
typedef struct _GeisDevice *GeisDevice;
/** @endcond */

GEIS_API void geis_register_device_callback(Geis               geis,
                                            GeisEventCallback  event_callback,
                                            void              *context);

/**
 * Gets a cached device description for an identified device.
 *
 * @param[in]  geis      The GEIS API instance.
 * @param[in]  device_id Identifies the device.
 *
 * The GEIS instance caches a list of gesture-capable input devices that have
 * been reported.  The GeisDevice description for an identified device may be
 * retrieved from that cache with this call.
 *
 * @returns a valid GeisDevice for the identified device, or NULL if no such
 * device is in the cache.
 */
GEIS_API GeisDevice geis_get_device(Geis geis, GeisInteger device_id);

/**
 * Adds a reference count to a device.
 * @memberof GeisDevice
 *
 * @param[in] device The device.
 *
 * An application that wishes to guarantee the device object remains valid
 * should add a reference using this call, and unref when the object is no
 * longer needed.
 *
 * @returns @p device for syntactic convenience.
 */
GEIS_API GeisDevice geis_device_ref(GeisDevice device);

/**
 * Removes a reference count from a device.
 * @memberof GeisDevice
 *
 * @param[in] device The device.
 *
 * This function decrements the number of references to the device and, if the
 * number of references hits zero, deletes the device.
 */
GEIS_API void geis_device_unref(GeisDevice device);

/**
 * Gets the name of the input device.
 * @memberof GeisDevice
 *
 * @param[in] device The device.
 */
GEIS_API GeisString geis_device_name(GeisDevice device);

/**
 * Gets the system identifier of the iput device.
 * @memberof GeisDevice
 *
 * @param[in] device The device.
 *
 * The system-defined device identifier is system- and possibly
 * device-dependent.
 */
GEIS_API GeisInteger geis_device_id(GeisDevice device);

/**
 * Gets the number of attributes of the device.
 * @memberof GeisDevice
 *
 * @param[in] device The device.
 */
GEIS_API GeisSize geis_device_attr_count(GeisDevice device);

/**
 * Gets the indicated attribute of the device.
 * @memberof GeisDevice
 *
 * @param[in] device The device.
 * @param[in] index  Indicates which attr to retrieve.
 */
GEIS_API GeisAttr geis_device_attr(GeisDevice device, GeisSize index);

/**
 * Gets a named attribute from the device.
 * @memberof GeisDevice
 *
 * @param[in] device    The device.
 * @param[in] attr_name The name of the attribute to retrieve.
 */
GEIS_API GeisAttr geis_device_attr_by_name(GeisDevice device, GeisString attr_name);

/* @} */

/**
 * @defgroup geis_v2_class Gesture Classes
 * @ingroup geis_v2
 * @{
 */

/**
 * @class GeisGestureClass
 * A defined gesture classifier.
 *
 * GeisGestureClass objects are created by the GEIS API and are reference
 * counted.  An application needs to increment and decrement the reference
 * count of a gesture class object to control its persistence.
 */
/** @cond typedef */
typedef struct _GeisGestureClass *GeisGestureClass;
/** @endcond */

/**
 * @name Gesture Class Event Attributes
 * @{
 *
 * @def GEIS_EVENT_ATTRIBUTE_CLASS
 * The event attribute containing a pointer to a GeisGestureClass. 
 *
 * The GEIS_EVENT_CLASS_AVAILABLE and GEIS_EVENT_CLASS_UNAVAILABLE events
 * should have a GEIS_ATTR_TYPE_POINTER attribute with this name.  It
 * should contain a pointer to a GeisGestureClass describing the gesture class
 * made available or unavailable.
 */
#define GEIS_EVENT_ATTRIBUTE_CLASS  "gesture class"

/* @} */

/**
 * @name Gesture Class Attributes
 * @{
 *
 * @def GEIS_CLASS_ATTRIBUTE_NAME
 * The name of the gesture class. 
 *
 * @def GEIS_CLASS_ATTRIBUTE_ID
 * The unique integer ID of the gesture class.
 */
#define GEIS_CLASS_ATTRIBUTE_NAME   "class name"
#define GEIS_CLASS_ATTRIBUTE_ID     "class id"

/* @} */

/**
 * Registers a callback to receive gesture class change notifications.
 *
 * @param[in] geis            The API instance.
 * @param[in] event_callback  The callback function.
 * @param[in] context         Contextual data to be passed through to the
 *                            callback.
 *
 * This function is used to register a function to be executed when a change to
 * the available gesture class definitions has occurred.  If no function is
 * registered, the default action is to deliver gesture class events through the
 * main event mechanism.
 *
 * Passing a value of GEIS_DEFAULT_EVENT_CALLBACK as the @p event-callback will
 * reset the callback function to the default action.
 *
 * The @p event_callback function will be executed in the same thread context as
 * geis_dispatch_events().
 */
GEIS_API void geis_register_class_callback(Geis               geis,
                                           GeisEventCallback  event_callback,
                                           void              *context);

/**
 * Increments the reference count of a gesture class object.
 * @memberof GeisGestureClass
 *
 * @param[in] gesture_class  The gesture class object.
 */
GEIS_API void geis_gesture_class_ref(GeisGestureClass gesture_class);

/**
 * Decrements the reference count of a gesture class object.
 * @memberof GeisGestureClass
 *
 * @param[in] gesture_class  The gesture class object.
 *
 * The reference count of the object is decremented and, if it reaches zero, the
 * object is destroyed.
 */
GEIS_API void geis_gesture_class_unref(GeisGestureClass gesture_class);

/**
 * Gets the name of the gesture class.
 * @memberof GeisGestureClass
 *
 * @param[in] gesture_class  The gesture class object.
 */
GEIS_API GeisString geis_gesture_class_name(GeisGestureClass gesture_class);

/**
 * Gets the numeric identifier of the gesture class.
 * @memberof GeisGestureClass
 *
 * @param[in] gesture_class  The gesture class object.
 */
GEIS_API GeisInteger geis_gesture_class_id(GeisGestureClass gesture_class);

/**
 * Gets the number of attributes of the gesture class.
 * @memberof GeisGestureClass
 *
 * @param[in] gesture_class  The gesture class object.
 */
GEIS_API GeisSize geis_gesture_class_attr_count(GeisGestureClass gesture_class);

/**
 * Gets the indicated attribute of the gesture class.
 * @memberof GeisGestureClass
 *
 * @param[in] gesture_class  The gesture class object.
 * @param[in] index          The index of the attribute to retrieve.
 */
GEIS_API GeisAttr geis_gesture_class_attr(GeisGestureClass gesture_class,
                                          int              index);

/* @} */

/**
 * @defgroup geis_v2_region Gesture Regions
 * @ingroup geis_v2
 * @{
 */

/**
 * @class GeisRegion
 * Defines a region over which gestures may take place.
 */
/** @cond typedef */
typedef struct _GeisRegion *GeisRegion;
/** @endcond */

/**
 * @name Region Attributes
 *
 * @par
 * These attributes can be used to construct filter terms to restrict a
 * gesture subscription to a particular region.
 *
 * @{
 *
 * @def GEIS_REGION_ATTRIBUTE_WINDOWID
 * The X11 windowid in which a gesture occurred. Used for filter matching.
 */
#define GEIS_REGION_ATTRIBUTE_WINDOWID          "windowid"

/* @} */

/**
 * @name Region Initialization Arguments
 *
 * @par
 * Gesture regions are created to describe a particular display/feedback region.
 * The type of the region can not be changed after creation (just create a new
 * region for that).  The types of regions are platform specific and each type
 * may require addition arguments.
 *
 * @par
 * The following region initialization argument names are required by the
 * GEIS v2.0 specification.
 *
 * @{
 *
 * @def GEIS_REGION_X11_ROOT
 * Selects the X11 root window as a region.
 *
 * @def GEIS_REGION_X11_WINDOWID
 * Selects an X11 window as a region.
 * Requires the window_id as an argument.
 */
#define GEIS_REGION_X11_ROOT       "org.libgeis.region.x11.root"

#define GEIS_REGION_X11_WINDOWID   "org.libgeis.region.x11.windowid"

/* @} */

/**
 * Creates a new GEIS v2.0 region.
 * @memberof GeisRegion
 *
 * @param[in] geis           The GEIS API instance.
 * @param[in] name           A name.  Used for diagnostics.
 * @param[in] init_arg_name  The name of the first initialization argument.
 *
 * The initialization argument list must be terminated by a NULL.
 *
 * @returns a newly created region, or NULL on failure.
 */
GEIS_API GEIS_VARARG GeisRegion geis_region_new(Geis       geis,
                                                GeisString name,
                                                GeisString init_arg_name, ...);

/**
 * Destroys a GEIS v2.0 region.
 * @memberof GeisRegion
 *
 * @param[in] region  The region.
 */
GEIS_API GeisStatus geis_region_delete(GeisRegion region);

/**
 * Gets the name of a GEIS v2.0 region.
 * @memberof GeisRegion
 *
 * @param[in] region  The region.
 *
 * Returns the @p name value used when creating the region.
 */
GEIS_API GeisString geis_region_name(GeisRegion region);

/* @} */

/**
 * @defgroup geis_v2_filter Gesture Filter
 * @ingroup geis_v2
 * @{
 */

/**
 * @class GeisFilter
 * Selects a subset of possible gestures in a subscription.
 *
 * A GeisFilter is a collection of filter terms, each of which defines a
 * criterion for selection of gestures returned on a subscription.
 *
 * All filter terms are effectively ANDed together in a filter.
 **/
/** @cond typedef */
typedef struct _GeisFilter *GeisFilter;
/** @endcond */

/**
 * Indicates the type of filter.
 */
typedef enum _GeisFilterFacility
{
  GEIS_FILTER_DEVICE   = 1000,  /**< Filters on device attributes. */
  GEIS_FILTER_CLASS    = 2000,  /**< Filters on gesture class and gesture attributes. */
  GEIS_FILTER_REGION   = 3000,  /**< Filters on region attributes. */
  GEIS_FILTER_SPECIAL  = 5000   /**< Filters on special attributes. */
} GeisFilterFacility;

/**
 * Indicates the type of filter operation.
 */
typedef enum _GeisFilterOperation
{
  GEIS_FILTER_OP_EQ,      /**< Compares for equality. */
  GEIS_FILTER_OP_NE,      /**< Compares for inequality */
  GEIS_FILTER_OP_GT,      /**< Compares for greater-than. */
  GEIS_FILTER_OP_GE,      /**< Compares for greater-than-or-equal. */
  GEIS_FILTER_OP_LT,      /**< Compares for less-than. */
  GEIS_FILTER_OP_LE       /**< Compares for less-tha-or-equal. */
} GeisFilterOperation;


/**
 * Creates a new, empty filter.
 * @memberof GeisFilter
 *
 * @param[in] geis  The GEIS API instance.
 * @param[in] name  A name.
 *
 * @returns a GeisFilter object or NULL on failure.
 */
GEIS_API GeisFilter geis_filter_new(Geis geis, GeisString name);

/**
 * Creates a new filter by copying an existing filter.
 * @memberof GeisFilter
 *
 * @param[in] original  An existing geisFilter instance.
 * @param[in] name      A name.
 *
 * The original filter remains unchanged.
 *
 * @returns a GeisFilter object or NULL on failure.
 */
GEIS_API GeisFilter geis_filter_clone(GeisFilter original, GeisString name);

/**
 * Destroys a GeisFilter.
 * @memberof GeisFilter
 *
 * @param[in] filter  The filter.
 */
GEIS_API GeisStatus geis_filter_delete(GeisFilter filter);

/**
 * Gets the name given to the filter when it was created.
 * @memberof GeisFilter
 *
 * @param[in] filter  The filter.
 */
GEIS_API GeisString geis_filter_name(GeisFilter filter);

/**
 * Adds a term to a filter.
 * @memberof GeisFilter
 *
 * @param[in] filter   The filter.
 * @param[in] facility The term facility.
 * @param[in] ...      A list of zero or more term descriptions.
 *
 * A term description is generally a (attr-name, filter-op, value) triple in
 * which the meaning of the filter-op and value depend on the type of the attr.
 *
 * The term description list must be terminated by a NULL.
 *
 * In the following example we add terms to filter drag gestures made with three
 * touch points:
 * @code
 * geis_filter_add_term(filter,
 *   GEIS_FILTER_CLASS,
 *   GEIS_CLASS_ATTRIBUTE_NAME, GEIS_FILTER_OP_EQ, GEIS_GESTURE_DRAG,
 *   GEIS_GESTURE_ATTRIBUTE_TOUCHES, GEIS_FILTER_OP_EQ, 3,
 *   NULL);
 * @endcode
 *
 * Term descriptions are usually ANDed together, so that specifying a class name
 * and a number of touches will filter only for gestures that have both
 * characteristics. But if you specify several class names (e.g. drag and pinch),
 * those classes are ORed together instead. So you can receive events from a
 * gesture that belongs to either drag, drag&pinch or only pinch classes.
 * 
 */
GEIS_API GEIS_VARARG GeisStatus geis_filter_add_term(GeisFilter         filter,
                                                     GeisFilterFacility facility,
                                                     ...);

/* @} */

/**
 * @defgroup geis_v2_subscription Gesture Subscription
 * @ingroup geis_v2
 * @{
 */

/**
 * @class GeisSubscription
 * A gesture recognition subscription.
 */
/** @cond typedef */
typedef struct _GeisSubscription *GeisSubscription;
/** @endcond */

/**
 * @enum GeisSubscriptionFlags
 *
 * These flags are used when creating a new subscription and affect the nature
 * of the gestures recognized by the subscription.  They may ORed together.
 *
 * @var GeisSubscriptionFlags::GEIS_SUBSCRIPTION_NONE
 * No special subscription processing:  this is the default.
 *
 * @var GeisSubscriptionFlags::GEIS_SUBSCRIPTION_GRAB
 * The subscription will "grab" all filtered gestures from subwindows.
 *
 * @var GeisSubscriptionFlags::GEIS_SUBSCRIPTION_CONT
 * The gesture engine will return <em>gesture continuations</em>, in which the
 * class of a recognized gestire may change over the lifetime of the gesture.
 * If this flag is not set, a new gesture will be identified for each change in
 * gesture class.
 */
enum
{
  GEIS_SUBSCRIPTION_NONE = 0x0000,
  GEIS_SUBSCRIPTION_GRAB = 0x0001,
  GEIS_SUBSCRIPTION_CONT = 0x0002
};
typedef int GeisSubscriptionFlags;

/**
 * Creates a new subscription.
 * @memberof GeisSubscription
 *
 * @param[in] geis  The GEIS API instance.
 * @param[in] name  A name.
 * @param[in] flags Some flags.
 *
 * @returns a GeisSubscription object or NULL on failure.
 *
 * A gesture subscription is required for any gesture events to be delivered
 * from the GEIS API.
 */
GEIS_API GeisSubscription geis_subscription_new(Geis                  geis,
                                                GeisString            name,
                                                GeisSubscriptionFlags flags);

/**
 * Destroys a GEIS v2.0 subscription object.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 */
GEIS_API GeisStatus geis_subscription_delete(GeisSubscription subscription);

/**
 * Activates a subscription.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 *
 * Puts the subscription into the active state.  Gesture events will be
 * delivered for this subscription.
 */
GEIS_API GeisStatus geis_subscription_activate(GeisSubscription subscription);

/**
 * Deactivates a subscription.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 *
 * Puts the subscription into the inactive state.  Gesture events will not be
 * delivered for this subscription.
 */
GEIS_API GeisStatus geis_subscription_deactivate(GeisSubscription subscription);

/**
 * Gets the name given to a subscription when it was created.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 */
GEIS_API GeisString geis_subscription_name(GeisSubscription subscription);

/**
 * Gets the ID assigned to a subscription when it was created.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 */
GEIS_API GeisInteger geis_subscription_id(GeisSubscription subscription);

/**
 * Adds a filter to a subscription.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 * @param[in] filter        The filter to be added to the subscription.
 *
 * The effect of filters are ORed together so that, for example, a
 * subscription that has a filter for 3-finger drag gestures and another for
 * 2-finger pinch gestures will produce events for both 3-finger drag gestures
 * and 2-finger pinch gestures.
 *
 * The default is no filters:  that is, all possible gesture events will be
 * reported.
 *
 * The subscription will take ownership of the filter.
 */
GEIS_API GeisStatus geis_subscription_add_filter(GeisSubscription subscription,
                                                 GeisFilter       filter);

/**
 * Gets an named filter from a subscription.
 * @memberof GeisSubscription
 *
 * @param[in] sub  The subscription.
 * @param[in] name Names the filter to retrieve.
 *
 * Returns the first filter with the given name or NULL if no such named filter
 * is found.
 */
GEIS_API GeisFilter geis_subscription_filter_by_name(GeisSubscription sub,
                                                     GeisString       name);

/**
 * Removes a filter from a subscription.
 * @memberof GeisSubscription
 *
 * @param[in] subscription  The subscription.
 * @param[in] filter        The filter to be removed from the subscription.
 *
 * Ownership of the filter is passed to the caller.
 */
GEIS_API GeisStatus geis_subscription_remove_filter(GeisSubscription subscription,
                                                    GeisFilter       filter);


/**
 * Gets a subscription-level configuration item.
 *
 * @param[in]  subscription      The subscription from which the configuration
 *                               item will be retrieved.
 * @param[in]  config_item_name  The name of the configuration item.
 * @param[out] config_item_value A pointer to an appropriate variable to hold
 *                               the retrieved config item value.
 *
 * Not all back ends support all configuration items.
 *
 * @retval GEIS_STATUS_BAD_ARGUMENT   an invalid argument value was passed
 * @retval GEIS_STATUS_NOT_SUPPORTED  the configuration value is not supported
 * @retval GEIS_STATUS_SUCCESS        normal successful completion
 */
GEIS_API GeisStatus geis_subscription_get_configuration(GeisSubscription subscription,
                                                        GeisString       config_item_name,
                                                        GeisPointer      config_item_value);

/**
 * Sets a subscription-level configuration item.
 *
 * @param[in] subscription      The subscription from which the configuration
 *                              item will be retrieved.
 * @param[in] config_item_name  The name of the configuration item.
 * @param[in] config_item_value A pointer to an appropriate variable holding
 *                              the config item value.
 *
 * Not all back ends support all configuration items.
 *
 * @retval GEIS_STATUS_BAD_ARGUMENT   an invalid argument value was passed
 * @retval GEIS_STATUS_NOT_SUPPORTED  the configuration value is not supported
 * @retval GEIS_STATUS_SUCCESS        normal successful completion
 */
GEIS_API GeisStatus geis_subscription_set_configuration(GeisSubscription subscription,
                                                        GeisString       config_item_name,
                                                        GeisPointer      config_item_value);

/* @} */

/**
 * @defgroup geis_v2_gesture Gesture Frames
 * @ingroup geis_v2
 * Gesture state information.
 *
 * Gesture frames, and their associated groups and touches, convey information
 * about the current state of recognized gestures.
 *
 * @{
 */

/**
 * @class GeisGroup
 * A collection of gesture frames.
 *
 * @class GeisGroupSet
 * A collection of GeisGroups.
 *
 * @class GeisTouch
 * An instance of a touch.
 *
 * @class GeisTouchId
 * Relates a touch in a frame to a touch object in a set.
 *
 * @class GeisTouchSet
 * A collection of GeisTouch
 *
 * @class GeisFrame
 * A collection of information describing the state of a gesture.
 */
/** @cond typedef */
typedef struct _GeisGroup    *GeisGroup;
typedef struct _GeisGroupSet *GeisGroupSet;
typedef GeisSize              GeisTouchId;
typedef struct _GeisTouch    *GeisTouch;
typedef struct _GeisTouchSet *GeisTouchSet;
typedef struct _GeisFrame    *GeisFrame;
/** @endcond */

/**
 * @name Gesture Frame Event Attributes
 *
 * @par
 * A gesture event (GEIS_EVENT_GESTURE_BEGIN, GEIS_EVENT_GESTURE_UPDATE,
 * GEIS_EVENT_GESTURE_END) should have two GEIS_ATTR_TYPE_POINTER attributes,
 * one containing a GeisGroupSet and one containing a GeisTouchSet.
 *
 * For example: If four fingers are being simultaneously moved over a touchpad
 * or touchscreen surface, Geis could start generating gesture events
 * containing two groups: One group having a single frame from a four-fingers
 * gesture of some class and a second group having two frames, each from a
 * different two-fingers gesture (like one from a Rotate and the other from a
 * Pinch gesture).
 * This means that geis could interpret the movements of those four touch points as
 * both a single four-fingers gesture and as two separate two-fingers gestures.
 *
 * There can be only a single frame per gesture in a gesture event. I.e. no two
 * frames will return the same GeisGestureId in the same gesture event.
 *
 * @{
 *
 * @def GEIS_EVENT_ATTRIBUTE_GROUPSET
 * The event attribute containing a pointer to a GeisGroupSet.
 *
 * @def GEIS_EVENT_ATTRIBUTE_TOUCHSET
 * The event attribute containing a pointer to a GeisTouchSet.
 *
 * @def GEIS_EVENT_ATTRIBUTE_CONSTRUCTION_FINISHED
 * Event attribute containing a boolean.
 * This property allows the client to determine if all the possible gestures
 * from the set of touches in this event have already been presented. When
 * this value is true, the client will have received all the information needed
 * to make a gesture accept and reject decision based on potentially
 * overlapping gestures. An example is when both one and two touch gestures are
 * subscribed on the same window with the same gesture classes and thresholds.
 * When this property is true for one touch gesture events, the client can be
 * sure there are no other touches unless a two touch gesture event has already
 * been sent.
 * Another example is when you subscribe for three touches Touch and four
 * touches Drag. As soon as a third finger is detected a three touches Touch
 * gesture will begin, but you cannot be sure a fourth finger isn't coming
 * right after (that can eventually cause a four touches Drag) until this
 * property is true.
 */
#define GEIS_EVENT_ATTRIBUTE_GROUPSET  "group set"
#define GEIS_EVENT_ATTRIBUTE_TOUCHSET  "touch set"
#define GEIS_EVENT_ATTRIBUTE_CONSTRUCTION_FINISHED  "construction finished"

/* @} */

/**
 * @name Touch Attributes
 *
 * @par
 * Each touch has zero or more attributes associated with it. Differing hardware
 * is capable of reporting differing sets of touch attributes, so there is no
 * guarantee that any or all of the defined touch attributes will bre present.
 *
 * If the touch comes from a direct device (see
 * GEIS_DEVICE_ATTRIBUTE_DIRECT_TOUCH) its position (x and y attributes) will
 * be in window coordinates, otherwise it will be in the input device's own
 * coordinate system.
 *
 * @{
 *
 * @def GEIS_TOUCH_ATTRIBUTE_ID
 * Identifies the touch. 
 *
 * @def GEIS_TOUCH_ATTRIBUTE_X
 * The X coordinate of the touch.
 *
 * @def GEIS_TOUCH_ATTRIBUTE_Y
 * The Y coordinate of the touch.
 */
#define GEIS_TOUCH_ATTRIBUTE_ID                 "touch id"
#define GEIS_TOUCH_ATTRIBUTE_X                  "touch x"
#define GEIS_TOUCH_ATTRIBUTE_Y                  "touch y"

/* @} */

/**
 * Gets the number of gesture groups in a groupset.
 * @memberof GeisGroupSet
 *
 * @param[in] groupset The groupset.
 */
GEIS_API GeisSize geis_groupset_group_count(GeisGroupSet groupset);

/**
 * Gets an indicated gesture group from a groupset.
 * @memberof GeisGroupSet
 *
 * @param[in] groupset The groupset.
 * @param[in] index    Indicates which gesture group to retrieve.
 */
GEIS_API GeisGroup geis_groupset_group(GeisGroupSet groupset, GeisSize index);

/**
 * Gets the identifier of a gesture group.
 * @memberof GeisGroup
 *
 * @param[in] group The gesture group.
 */
GEIS_API GeisInteger geis_group_id(GeisGroup group);

/**
 * Gets the number of gesture frames in a gesture group.
 * @memberof GeisGroup
 *
 * @param[in] group The gesture group.
 */
GEIS_API GeisSize geis_group_frame_count(GeisGroup group);

/**
 * Gets an indicated gesture frame from a gesture group.
 * @memberof GeisGroup
 *
 * @param[in] group The gesture group.
 * @param[in] index Indicates which gesture frame to retrieve.
 */
GEIS_API GeisFrame geis_group_frame(GeisGroup group, GeisSize index);

/**
 * Marks a gesture group as rejected.
 * @memberof GeisGroup
 *
 * @param[in] group The gesture group to reject.
 */
GEIS_API void geis_group_reject(GeisGroup group);

/**
 * Gets the number of touches in a touchset.
 * @memberof GeisTouchSet
 *
 * @param[in] touchset  The touchset,
 */
GEIS_API GeisSize geis_touchset_touch_count(GeisTouchSet touchset);

/**
 * Gets an indicated touch from a touchset.
 * @memberof GeisTouchSet
 *
 * @param[in] touchset  The touchset.
 * @param[in] index     Indicates which touch to retrieve.
 */
GEIS_API GeisTouch geis_touchset_touch(GeisTouchSet touchset, GeisSize index);

/**
 * Gets an identified touch from a touchset.
 * @memberof GeisTouchSet
 *
 * @param[in] touchset  The touchset.
 * @param[in] touchid   Identifies a touch.
 *
 * Returns the identified touch, or NULL if the touchid is not in the touchset.
 */
GEIS_API GeisTouch geis_touchset_touch_by_id(GeisTouchSet touchset,
                                             GeisTouchId  touchid);

/**
 * Gets the identifier of a touch.
 * @memberof GeisTouch
 *
 * @param[in] touch  The touch.
 */
GEIS_API GeisTouchId geis_touch_id(GeisTouch touch);

/**
 * Gets the number of attrs associated with a touch.
 * @memberof GeisTouch
 *
 * @param[in] touch  The touch.
 */
GEIS_API GeisSize geis_touch_attr_count(GeisTouch touch);

/**
 * Gets an indicated attr from a touch.
 * @memberof GeisTouch
 *
 * @param[in] touch  The touch.
 * @param[in] index  Indicates which attr to retrieve.
 */
GEIS_API GeisAttr geis_touch_attr(GeisTouch touch, GeisSize index);

/**
 * Gets a named attr from a touch.
 * @memberof GeisTouch
 *
 * @param[in] touch  The touch.
 * @param[in] name   Names the attr to retrieve.
 *
 * @returns the named attr if it is present, NULL otherwise.
 */
GEIS_API GeisAttr geis_touch_attr_by_name(GeisTouch touch, GeisString name);

/**
 * Gets the identifier of a gesture frame.
 * @memberof GeisFrame
 *
 * @param[in] frame  the gesture frame.
 *
 * @returns the identifier of the gesture to which the given frame belongs.
 */
GEIS_API GeisGestureId geis_frame_id(GeisFrame frame);

/**
 * Indicates if a gesture frame belongs to a gesture class.
 * @memberof GeisFrame
 *
 * @param[in] frame         The gesture frame.
 * @param[in] gesture_class The gesture class.
 *
 * @returns true if the gesture can currently be classified by the @p
 * gesture_class, false otherwise.
 */
GEIS_API GeisBoolean geis_frame_is_class(GeisFrame        frame,
                                         GeisGestureClass gesture_class);

/**
 * Gets the number of attrs associated with a gesture frame.
 * @memberof GeisFrame
 *
 * @param[in] frame  The gesture frame.
 */
GEIS_API GeisSize geis_frame_attr_count(GeisFrame frame);

/**
 * Gets an indicated attr from a gesture frame.
 * @memberof GeisFrame
 *
 * @param[in] frame  The gesture frame.
 * @param[in] index  Indicates which attr to retrieve.
 */
GEIS_API GeisAttr geis_frame_attr(GeisFrame frame, GeisSize index);

/**
 * Gets a named attr from a gesture frame.
 * @memberof GeisFrame
 *
 * @param[in] frame  The gesture frame.
 * @param[in] name   Names the attr to retrieve, such as one of the
 *                   GEIS_GESTURE_ATTRIBUTE_* constants.
 * @returns the named attr if it is present, NULL otherwise.
 *
 * Usage example:
 * @code
 * GeisAttr angle = geis_frame_attr_by_name(frame, GEIS_GESTURE_ATTRIBUTE_ANGLE);
 * @endcode
 */
GEIS_API GeisAttr geis_frame_attr_by_name(GeisFrame frame, GeisString name);

/**
 * Gets the current transform matrix of a gesture.
 * @memberof GeisFrame
 *
 * @param[in] frame  The gesture frame.
 */
GEIS_API GeisFloat *geis_frame_matrix(GeisFrame frame);

/**
 * Gets the number of touches making up a gesture for the frame.
 * @memberof GeisFrame
 *
 * @param[in] frame  The gesture frame.
 */
GEIS_API GeisSize geis_frame_touchid_count(GeisFrame frame);

/**
 * Gets the ID of the indicated touch within the gesture frame.
 * @memberof GeisFrame
 *
 * @param[in] frame  The gesture frame.
 * @param[in] index  Indicates which touch ID to retrieve.
 */
GEIS_API GeisTouchId geis_frame_touchid(GeisFrame frame, GeisSize index);

/**
 * Marks a gesture as accepted.
 *
 * @param[in] geis        The GEIS instance.
 * @param[in] group       The gesture group containing the accepted gesture.
 * @param[in] gesture_id  Identifies the gesture.
 *
 * @sa geis_frame_id
 */
GEIS_API GeisStatus geis_gesture_accept(Geis          geis,
                                        GeisGroup     group,
                                        GeisGestureId gesture_id);

/**
 * Marks a gesture as rejected.
 *
 * @param[in] geis        The GEIS instance.
 * @param[in] group       The gesture group containing the rejected gesture.
 * @param[in] gesture_id  Identifies the gesture.
 *
 * After you reject a gesture you no longer get its frames.
 *
 * @sa geis_frame_id
 */
GEIS_API GeisStatus geis_gesture_reject(Geis          geis,
                                        GeisGroup     group,
                                        GeisGestureId gesture_id);

/* @} */

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* GEIS_GEIS_H_ */
