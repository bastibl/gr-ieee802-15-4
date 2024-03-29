/*
 * Copyright 2021 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(frame_buffer_cc.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(8f6dcd5bc62eeca65790ab67a2a56ea7)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/frame_buffer_cc.h>
// pydoc.h is automatically generated in the build directory
#include <frame_buffer_cc_pydoc.h>

void bind_frame_buffer_cc(py::module& m)
{

    using frame_buffer_cc    = ::gr::ieee802_15_4::frame_buffer_cc;


    py::class_<frame_buffer_cc, gr::block, gr::basic_block,
        std::shared_ptr<frame_buffer_cc>>(m, "frame_buffer_cc", D(frame_buffer_cc))

        .def(py::init(&frame_buffer_cc::make),
           py::arg("nsym_frame"),
           D(frame_buffer_cc,make)
        )
        



        ;




}








