//
// Copyright (C) 2021 Asanga Udugama (adu@comnets.uni-bremen.de)
//
// SPDX-License-Identifier: GPL-3.0-or-later
//

package inbaversim;

//
// Interface of a CCN forwarder.
//
// @author : Asanga Udugama (adu@comnets.uni-bremen.de)
// @date   : 31-mar-2021
//
//
moduleinterface IForwarder
{
    parameters:
        @display("i=block/fork;t=Forwarding,l");

    gates:
        inout appInOut[];
        inout transportInOut[];
}
