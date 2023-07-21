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
/* BINDTOOL_HEADER_FILE(chips_to_bits_fb.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(8b2d311cb935ae8ae5d15320de3a6d5d)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/chips_to_bits_fb.h>
// pydoc.h is automatically generated in the build directory
#include <chips_to_bits_fb_pydoc.h>

void bind_chips_to_bits_fb(py::module& m)
{

    using chips_to_bits_fb    = ::gr::ieee802_15_4::chips_to_bits_fb;


    py::class_<chips_to_bits_fb, gr::sync_decimator,
        std::shared_ptr<chips_to_bits_fb>>(m, "chips_to_bits_fb", D(chips_to_bits_fb))

        .def(py::init(&chips_to_bits_fb::make),
           py::arg("chip_seq"),
           D(chips_to_bits_fb,make)
        )
        



        ;




}







