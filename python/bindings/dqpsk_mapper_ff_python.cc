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
/* BINDTOOL_HEADER_FILE(dqpsk_mapper_ff.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(f76afdebe46747547a09b37a66a6dbac)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/dqpsk_mapper_ff.h>
// pydoc.h is automatically generated in the build directory
#include <dqpsk_mapper_ff_pydoc.h>

void bind_dqpsk_mapper_ff(py::module& m)
{

    using dqpsk_mapper_ff    = ::gr::ieee802_15_4::dqpsk_mapper_ff;


    py::class_<dqpsk_mapper_ff, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<dqpsk_mapper_ff>>(m, "dqpsk_mapper_ff", D(dqpsk_mapper_ff))

        .def(py::init(&dqpsk_mapper_ff::make),
           py::arg("framelen"),
           py::arg("forward"),
           D(dqpsk_mapper_ff,make)
        )
        



        ;




}








