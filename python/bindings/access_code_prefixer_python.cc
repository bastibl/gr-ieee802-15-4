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
/* BINDTOOL_HEADER_FILE(access_code_prefixer.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(b74bd0506a3cff0b89a450dd6a498204)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/access_code_prefixer.h>
// pydoc.h is automatically generated in the build directory
#include <access_code_prefixer_pydoc.h>

void bind_access_code_prefixer(py::module& m)
{

    using access_code_prefixer    = ::gr::ieee802_15_4::access_code_prefixer;


    py::class_<access_code_prefixer, gr::block, gr::basic_block,
        std::shared_ptr<access_code_prefixer>>(m, "access_code_prefixer", D(access_code_prefixer))

        .def(py::init(&access_code_prefixer::make),
           py::arg("pad") = 0,
           py::arg("preamble") = 167,
           D(access_code_prefixer,make)
        )
        



        ;




}








