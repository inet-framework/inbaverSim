//
// Formats of messages used by transports
//

//
// Transport message that encapsulates CCNx messages
//
packet TransportMsg
{
    // source, destination addresses
    string sourceAddress;
    bool broadcastMsg;
    string destinationAddress;

    // msg sizes in bytes
    int headerSize;
    int payloadSize;

}

