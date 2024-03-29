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
/* BINDTOOL_HEADER_FILE(zeropadding_removal_b.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(6c035154dd89a931ebdb801b6fed7228)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/zeropadding_removal_b.h>
// pydoc.h is automatically generated in the build directory
#include <zeropadding_removal_b_pydoc.h>

void bind_zeropadding_removal_b(py::module& m)
{

    using zeropadding_removal_b    = ::gr::ieee802_15_4::zeropadding_removal_b;


    py::class_<zeropadding_removal_b, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<zeropadding_removal_b>>(m, "zeropadding_removal_b", D(zeropadding_removal_b))

        .def(py::init(&zeropadding_removal_b::make),
           py::arg("phr_payload_len"),
           py::arg("nzeros"),
           D(zeropadding_removal_b,make)
        )
        



        ;




}








