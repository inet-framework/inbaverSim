//
// SPDX-License-Identifier: GPL-3.0-or-later
//

package inbaversim;

//
// Interface of a CCN application.
//
moduleinterface IApplication
{
    parameters:
        @display("i=block/app;t=Application,l");

    gates:
        inout forwarderInOut;

}
