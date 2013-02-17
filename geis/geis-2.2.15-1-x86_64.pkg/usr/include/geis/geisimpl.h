/**
 * geisimpl.h
 *
 * Copyright 2010 Canonical Ltd.
 *
 * This library is free software; you can redistribute it and/or modify it under
 * the terms of version 3 of the GNU Lesser General Public License as published
 * by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
 */
#ifndef LIBGEIS_XCB_GEISIMPL_H_
#define LIBGEIS_XCB_GEISIMPL_H_

#include <stdint.h>
#include <stdlib.h>

/* Provide some cross-platform symbol export decorations. */
#if defined _WIN32 || defined __CYGWIN__
  #define GEIS_HELPER_DSO_IMPORT __declspec(dllimport)
  #define GEIS_HELPER_DSO_EXPORT __declspec(dllexport)
  #define GEIS_HELPER_DSO_LOCAL
#else
  #if __GNUC__ >= 4
    #define GEIS_HELPER_DSO_IMPORT __attribute__ ((visibility("default")))
    #define GEIS_HELPER_DSO_EXPORT __attribute__ ((visibility("default")))
    #define GEIS_HELPER_DSO_LOCAL  __attribute__ ((visibility("hidden")))
  #else
    #define GEIS_HELPER_DSO_IMPORT
    #define GEIS_HELPER_DSO_EXPORT
    #define GEIS_HELPER_DSO_LOCAL
  #endif
#endif

#ifdef GEIS_BUILDING_DSO
  #ifdef GEIS_DSO_EXPORTS 
    #define GEIS_API GEIS_HELPER_DSO_EXPORT
  #else
    #define GEIS_API GEIS_HELPER_DSO_IMPORT
  #endif /* GEIS_DSO_EXPORTS */
  #define GEIS_LOCAL GEIS_HELPER_DSO_LOCAL
#else 
  #define GEIS_API
  #define GEIS_LOCAL
#endif /* GEIS_BUILDING_DSO */

/* If available, provide a NULL terminator check decoration. */
#if __GNUC__ >= 4
# define GEIS_VARARG __attribute__((sentinel(0)))
#else
# define GEIS_VARARG 
#endif

/**
 * Portability types
 */
typedef size_t         GeisSize;
typedef uint32_t       GeisBoolean;
typedef int32_t        GeisInteger;
typedef float          GeisFloat;
typedef void*          GeisPointer;
typedef const char    *GeisString;

/**
 * @brief Magic for constructing geis win_type values.
 */
static inline uint32_t _geis_win_type_str(const char tag[5])
{ return (((((tag[3] << 8 ) | tag[2]) << 8) | tag[1]) << 8) | tag[0]; }

#define geis_win_type_str(tag) _geis_win_type_str(#tag)

/** A full X11 window */
#define GEIS_XCB_FULL_WINDOW  geis_win_type_str(GXWF)

/**
 * @brief Contains XCB-specific window information
 */
typedef struct _GeisXcbWinInfo
{
  const char  *display_name;
  int         *screenp;
  uint32_t     window_id;
} GeisXcbWinInfo;

#endif /* LIBGEIS_XCB_GEISIMPL_H_ */

