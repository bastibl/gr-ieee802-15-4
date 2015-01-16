from constants import *
import numpy as np

class parameters:
    def __init__(self, phy_mode_str, ber, coll_prob, nbytes_mac_payload=aMacMaxNumDataBytesPayload,
                 nbytes_mac_data_frame_overhead=aMacMinNumBytesDataFrameOverhead,
                 macBeaconOrder=aMacMaxBeaconOrder, macSuperframeOrder=aMacMaxSuperframeOrder,
                 macBeaconInterval=aBaseSuperframeDuration*2**aMacMaxBeaconOrder,
                 macSuperframeDuration=aBaseSuperframeDuration*2**aMacMaxSuperframeOrder, macBatteryLifeExtension=False):

        self.phy_mode = vPhyModeDict[phy_mode_str]
        self.ber = ber
        self.p_col = coll_prob
        self.nbytes_mac_payload = aMacMaxBytesPayload
        self.nbytes_mac_data_frame_overhead = nbytes_mac_data_frame_overhead
        self.nbytes_phy_payload = self.nbytes_mac_payload + self.nbytes_mac_data_frame_overhead
        self.macBeaconInterval = macBeaconInterval
        self.macSuperframeDuration = macSuperframeDuration
        self.macBatteryLifeExtension = macBatteryLifeExtension
        if macBatteryLifeExtension:
            raise NotImplementedError()
        self.phyDataFrameDuration = self.calc_phyFrameDuration(self.nbytes_phy_payload)
        self.phyAckFrameDuration = self.calc_phyFrameDuration(aMacNumBytesAckFrame)
        self.macIFSPeriod = aMacLIFSPeriod if self.nbytes_phy_payload > aMacMaxSIFSFrameSize else aMacSIFSPeriod
        self.phyTransmissionWithAckDuration = self.phyDataFrameDuration + t_ACK + self.phyAckFrameDuration + self.macIFSPeriod
        self.phyBeaconDuration = self.calc_phyFrameDuration(aMacMinNumBytesBeaconFrame)

    def calc_phyFrameDuration(self, phy_packet_size):
        if self.phy_mode == PHY_OQPSK:
            return vPhySHRDuration[self.phy_mode] + np.ceil((self.nbytes_phy_payload+1)*vPhySymbolsPerOctet[self.phy_mode])
        elif self.phy_mode == PHY_CSS1M:
            return vPhySHRDuration[self.phy_mode] + (1.5 + 3.0/4*np.ceil(4.0/3*self.nbytes_phy_payload))*vPhySymbolsPerOctet[self.phy_mode]
        elif self.phy_mode == PHY_CSS250k:
            return vPhySHRDuration[self.phy_mode] + 3*np.ceil(1.0/3*(1.5 + self.nbytes_phy_payload))*vPhySymbolsPerOctet[self.phy_mode]
        else:
            raise RuntimeError("Invalid mode")