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
/* BINDTOOL_HEADER_FILE(codeword_soft_demapper_fb.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(b2c725b787d15184d4df030597b6a2be)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/codeword_soft_demapper_fb.h>
// pydoc.h is automatically generated in the build directory
#include <codeword_soft_demapper_fb_pydoc.h>

void bind_codeword_soft_demapper_fb(py::module& m)
{

    using codeword_soft_demapper_fb    = ::gr::ieee802_15_4::codeword_soft_demapper_fb;


    py::class_<codeword_soft_demapper_fb, gr::block, gr::basic_block,
        std::shared_ptr<codeword_soft_demapper_fb>>(m, "codeword_soft_demapper_fb", D(codeword_soft_demapper_fb))

        .def(py::init(&codeword_soft_demapper_fb::make),
           py::arg("bits_per_cw"),
           py::arg("codewords"),
           D(codeword_soft_demapper_fb,make)
        )
        



        ;




}








