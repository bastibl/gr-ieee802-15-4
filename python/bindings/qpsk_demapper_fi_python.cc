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
/* BINDTOOL_HEADER_FILE(qpsk_demapper_fi.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(211dfc618fcc712aaa027804f620ae87)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <ieee802_15_4/qpsk_demapper_fi.h>
// pydoc.h is automatically generated in the build directory
#include <qpsk_demapper_fi_pydoc.h>

void bind_qpsk_demapper_fi(py::module& m)
{

    using qpsk_demapper_fi    = ::gr::ieee802_15_4::qpsk_demapper_fi;


    py::class_<qpsk_demapper_fi, gr::sync_block, gr::block, gr::basic_block,
        std::shared_ptr<qpsk_demapper_fi>>(m, "qpsk_demapper_fi", D(qpsk_demapper_fi))

        .def(py::init(&qpsk_demapper_fi::make),
           D(qpsk_demapper_fi,make)
        )
        



        ;




}







