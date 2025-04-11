//
// Copyright (C) 2021 Asanga Udugama (adu@comnets.uni-bremen.de)
//
// SPDX-License-Identifier: GPL-3.0-or-later
//

package inbaversim;

//
// Interface of a CCN application.
//
// @author : Asanga Udugama (adu@comnets.uni-bremen.de)
// @date   : 31-mar-2021
//
//
moduleinterface IApplication
{
    parameters:
        @display("i=block/app;t=Application,l");

    gates:
        inout forwarderInOut;

}
