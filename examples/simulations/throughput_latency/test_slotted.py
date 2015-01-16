import mac_slotted as mac
import parameters as params

if __name__ == "__main__":
    p = params.parameters("OQPSK", 0.001, 0.0)
    m = mac.mac_slotted(p)
    lat, bytes = m.run()
    print "lat:", lat
    print "bytes:", bytes