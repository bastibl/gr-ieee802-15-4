#!/usr/bin/env python

########################################################################################################################
# This script shall simulate the throughput between MAC and higher layers and the latency of the IEEE 802.15.4 MAC in a
# direct peer-to-peer communication between two devices.
#
# The standard offers several different medium access schemes: beacon-enabled (forming superframes) and nonbeacon-enabled
#
# Beacon-enabled:
#     Superframes are formed by periodically transmitting beacons. The superframe consists of the beacon, the active and
#     the inactive period. The beacon can be used by the coordinator to indicate pending messages for devices. The active
#     period immediately follows the beacon and starts with the CAP followed by the CFP. The CAP uses a slotted
#     CSMA-CA or ALOHA algorithm. The CFP consists of up to 7 guaranteed time slots (GTSs) that can be assigned to
#     specific devices. Acknowledgment and beacon frames are sent without using a CSMA-CA mechanism.
#
# Nonbeacon-enabled:
#     All devices use an unslotted CSMA-CA or ALOHA channel access mechanism. Acknowledgment frames are sent without
#     using a CSMA-CA mechanism.
#
# Transmissions can be carried out with or without acknowledgment after successful application of the CSMA-CA algorithm..
# With ACK:
#   - If nonbeacon-enabled or in CFP, ACK transmission begins macSIFSPeriod after the reception of the data frame
#   - If beacon-enabled, the ACK is to be sent either macSIFSPeriod after the data frame or at a backoff period boundary.
#     In the latter case, the ACK transmission shall begin between macSIFSPeriod and (macSIFSPeriod + aUnitBackoffPeriod
#     after the data frame.
#   - Scenarios to consider: A: successful transmission, B: data frame gets lost, C: ACK gets lost
#
#
# For a successful transmission there are various important parameters.
# External: Channel occupation by other devices, general channel influence (noise, fading,...)
# Internal: Choice of algorithm parameters such as max wait time, number of retries etc
#
# Signal propagation time has been neglected throughout the simulation.
########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from csma_ca import csma_unslotted

# constants - times are given in multiples of symbol durations if not otherwise stated
PHY_OQPSK = 0
PHY_CSS_FAST = 1
PHY_CSS_SLOW = 2
MAC_UNSLOTTED = 0
MAC_SLOTTED = 1
vPhyModeStr = ['OQPSK', 'CSS1M', 'CSS250k']

aUnitBackoffPeriod = 20
aTurnaroundTime = 12
vPhySHRDuration = [6.0, 6.0, 12.0]
vPhySymbolsPerOctet = [2.0, 1.3, 5.3]
vPhySymbolDurationSec = [16e-6, 6e-6, 6e-6]
vPhyDataRate = [250e3, 1e6, 250e3] # this treats every information (incl. SHR & PHR) as data!
macLIFSPeriod = 40
macSIFSPeriod = 12
aMacMaxSIFSFrameSize = 18 # in bytes, refers to the MPDU (MAC frame)
t_ACK = macSIFSPeriod # this is still in symbols
aMacMinNumBytesBeaconFrame = 13 # 2+1+4+0+2+1+1+0+2
aMacNumBytesAckFrame = 5
macMinNumBytesDataFrameOverhead = 7 # 2+1+2+0+2
aPhyMaxNumBytesPayload = 127
aPhyNumBitsPHR = 7
aMacMaxBytesPayload = aPhyMaxNumBytesPayload - macMinNumBytesDataFrameOverhead
macAvgCSMABackoff = 3.5 * aUnitBackoffPeriod # E[uniformdistribution(0...2**3)] = (7+1)/2 = 3.5

# configuration parameters
phy_mode = PHY_CSS_SLOW
mac_mode = MAC_UNSLOTTED
bit_error_ratio = np.logspace(-5.0, -2.0, 50)
collision_probability = [0.5, 0.1, 0.0]
nbytes_mac_payload = aMacMaxBytesPayload
nbytes_mac_data_frame_overhead = macMinNumBytesDataFrameOverhead

# simulation stop criteria
t_max = 100

# helper function
def calc_phyFrameDuration(mode, phy_packet_size):
    if mode == PHY_OQPSK:
        return vPhySHRDuration[mode] + np.ceil((nbytes_phy_payload+1)*vPhySymbolsPerOctet[mode])
    elif mode == PHY_CSS_FAST:
        return vPhySHRDuration[mode] + (1.5 + 3.0/4*np.ceil(4.0/3*nbytes_phy_payload))*vPhySymbolsPerOctet[mode]
    elif mode == PHY_CSS_SLOW:
        return vPhySHRDuration[mode] + 3*np.ceil(1.0/3*(1.5 + nbytes_phy_payload))*vPhySymbolsPerOctet[mode]
    else:
        raise RuntimeError("Invalid mode")

# parameters depending on the configuration
phy_mode_str = vPhyModeStr[phy_mode]
nbytes_phy_payload = nbytes_mac_data_frame_overhead + nbytes_mac_payload
phyDataFrameDuration = calc_phyFrameDuration(phy_mode, nbytes_phy_payload)
phyAckFrameDuration = calc_phyFrameDuration(phy_mode, aMacNumBytesAckFrame)
phySHRDuration = vPhySHRDuration[phy_mode]
phySymbolsPerOctet = vPhySymbolsPerOctet[phy_mode]
phySymbolDurationSec = vPhySymbolDurationSec[phy_mode]
phyDataRate = vPhyDataRate[phy_mode]
macAckWaitDuration = aUnitBackoffPeriod+aTurnaroundTime+phySHRDuration+np.ceil(6*phySymbolsPerOctet)
macIFSPeriod = macLIFSPeriod if nbytes_phy_payload > aMacMaxSIFSFrameSize else macSIFSPeriod
csma = csma_unslotted()

phyPayloadDataRate =  8.0*nbytes_phy_payload/phyDataFrameDuration/phySymbolDurationSec

# assuming no CSMA backoff and an acknowledged transmission
macTheoreticalMaxDataRate = phyPayloadDataRate * nbytes_mac_payload/nbytes_phy_payload * phyDataFrameDuration / (macAvgCSMABackoff + phyDataFrameDuration + t_ACK + phyAckFrameDuration + macIFSPeriod)

def tx_successful(success_prob):
    randnum = np.random.randint(0,1e9)
    if randnum < success_prob*1e9:
        return True
    else:
        return False

if __name__ == "__main__":

    print "### Setup ###"
    print "BER:", bit_error_ratio
    print "Collision probability:", collision_probability
    print "Data frame duration [ms]:", phyDataFrameDuration*phySymbolDurationSec*1000
    print "ACK frame duration [ms]:", phyAckFrameDuration*phySymbolDurationSec*1000
    print "t_ACK [ms]:", t_ACK*phySymbolDurationSec*1000
    print "IFS [ms]:", macIFSPeriod*phySymbolDurationSec*1000
    print "Theoretical max data rate [kb/s]:", macTheoreticalMaxDataRate/1000

    res_throughput_bps = np.zeros((len(collision_probability), len(bit_error_ratio)))
    res_latency_s = np.zeros((len(collision_probability), len(bit_error_ratio)))

    for c in range(len(collision_probability)):
        print "collision probability:", collision_probability[c]

        for b in range(len(bit_error_ratio)):
            # print "--- BER:", bit_error_ratio[b]
            fail_prob_data_frame = 1 - (1 - bit_error_ratio[b])**(8*nbytes_phy_payload + aPhyNumBitsPHR)
            fail_prob_ack_frame = 1 - (1 - bit_error_ratio[b])**(8*aMacNumBytesAckFrame + aPhyNumBitsPHR)
            success_prob_transmission = (1 - fail_prob_ack_frame)*(1 - fail_prob_data_frame)

            total_sym_elapsed = 0
            total_bytes_transmitted = 0
            latencies = []
            min_latency = phyDataFrameDuration
            cur_latency = min_latency # this is the minimal latency for a data frame
            while total_sym_elapsed*phySymbolDurationSec < t_max:
                # initialize latency for this frame
                sym_elapsed = 0
                bytes_transmitted = 0

                # run CSMA algorithm until the frame can be sent
                success = False
                while success == False:
                    (success, delay) = csma.run(collision_probability[c])
                    sym_elapsed += delay
                    cur_latency += delay

                # now a frame is sent.For a successful transmission, both data frame and ACK frame have to be received correctly
                if tx_successful(success_prob_transmission):
                    bytes_transmitted += nbytes_mac_payload
                    sym_elapsed += phyDataFrameDuration + t_ACK + phyAckFrameDuration + macIFSPeriod
                    latencies.append(cur_latency)
                    cur_latency = min_latency
                else:
                    bytes_transmitted += 0
                    sym_elapsed += phyDataFrameDuration + macAckWaitDuration
                    cur_latency +=phyDataFrameDuration + macAckWaitDuration

                total_sym_elapsed += sym_elapsed
                total_bytes_transmitted += bytes_transmitted

            res_latency_s[c][b] = np.mean(latencies)*phySymbolDurationSec
            res_throughput_bps[c][b] = 8.0*total_bytes_transmitted/(total_sym_elapsed*phySymbolDurationSec)

    # # plot throughput
    # f1 = plt.figure(1)
    # for i in range(res_throughput_bps.shape[0]):
    #     plt.semilogx(bit_error_ratio, res_throughput_bps[i]/1000, label="collision probability: "+str(collision_probability[i]))
    # plt.xlabel("BER")
    # plt.ylim([0,150])
    # plt.ylabel("Average Throughput [kb/s]")
    # plt.legend(loc = 'lower left')
    # plt.grid()
    # # plt.savefig("throughput_unslotted_csma_"+phy_mode_str+"_"+str(nbytes_phy_payload)+"bytePSDU.pdf", bbox='tight')
    #
    # # plot latency
    # f2 = plt.figure(2)
    # for i in range(res_throughput_bps.shape[0]):
    #     plt.semilogx(bit_error_ratio, res_latency_s[i]*1000, label="collision probability: "+str(collision_probability[i]))
    # plt.xlabel("BER")
    # plt.ylim([0,200])
    # plt.ylabel("Average Latency [ms]")
    # plt.legend(loc = 'upper left')
    # plt.grid()
    # # plt.savefig("latency_unslotted_csma_"+phy_mode_str+"_"+str(nbytes_phy_payload)+"bytePSDU.pdf", bbox='tight')

    np.savez("throughput_latency_unslotted_csma_"+phy_mode_str+"_"+str(nbytes_phy_payload)+"bytePSDU", res_latency_s = res_latency_s, res_throughput_bps=res_throughput_bps)

    # combo plot
    vThroughputYLim = [200, 800, 200]
    throughputYLim = vThroughputYLim[phy_mode]
    markers = ['o', 'v', 's', 'x']
    fig, ax1 = plt.subplots()
    for i in range(res_throughput_bps.shape[0]):
        ax1.semilogx(bit_error_ratio, res_throughput_bps[i]/1000,linestyle='-', label="collision probability: "+str(collision_probability[i]), marker=markers[i])
    rate_formatted = "%0.1f" % (macTheoreticalMaxDataRate/1000,)
    ax1.axhline(macTheoreticalMaxDataRate/1000, color='c', marker='p', label="theoretical max. data rate")
    ax1.set_xlabel('BER')
    ax1.set_ylabel('Throughput [kb/s]')
    ax1.set_ylim([0,throughputYLim])
    ax1.legend(loc='upper left')
    ax1.grid()

    ax2 = ax1.twinx()
    for i in range(res_throughput_bps.shape[0]):
        ax2.semilogx(bit_error_ratio, res_latency_s[i]*1000, linestyle='--', marker=markers[i])
    ax2.set_ylabel('Latency [ms]')
    ax2.set_ylim([0,200])

    plt.savefig("latency_throughput_unslotted_csma_"+phy_mode_str+"_"+str(nbytes_phy_payload)+"bytePSDU.pdf", bbox='tight')

    plt.show()

