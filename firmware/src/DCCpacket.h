
#define DCC_PACKET_PREAMBLE 0b1111111111111110




class DCCPacket {
    private:
        byte address;
        unsigned 
    public:
        DCCPacket();
        void write(int pin);


};