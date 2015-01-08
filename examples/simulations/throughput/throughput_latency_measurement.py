#!/usr/bin/env python

########################################################################################################################
# This script shall simulate the throughput and the latency of the IEEE 802.15.4 MAC in a direct peer-to-peer
# communication between two devices.
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

aUnitBackoffPeriod = 20
aTurnaroundTime = 12
vPhySHRDuration = [6.0, 6.0, 12.0]
vPhySymbolsPerOctet = [2.0, 1.3, 5.3]
vPhySymbolDurationSec = [16e-6, 6e-6, 6e-6]
macLIFSPeriod = 40
macSIFSPeriod = 12
t_ACK = macSIFSPeriod # this is still in symbols
macMinNumBytesBeaconFrame = 13 # 2+1+4+0+2+1+1+0+2
macNumBytesAckFrame = 4
macMinNumBytesDataFrameOverhead = 7 # 2+1+2+0+2
aPhyMaxNumBytesPayload = 127
aMacMaxBytesPayload = aPhyMaxNumBytesPayload - macMinNumBytesDataFrameOverhead

# configuration parameters
phy_mode = PHY_OQPSK
mac_mode = MAC_UNSLOTTED
bit_error_ratio = 1e-3
collision_probability = 1e-2
nbytes_mac_payload = aMacMaxBytesPayload
nbytes_mac_data_frame_overhead = macMinNumBytesDataFrameOverhead

# simulation stop criteria
bits_to_transmit = 1e9
t_max = 10

# parameters depending on the configuration
phySHRDuration = vPhySHRDuration[phy_mode]
phySymbolsPerOctet = vPhySymbolsPerOctet[phy_mode]
phySymbolDurationSec = vPhySymbolDurationSec[phy_mode]
macAckWaitDuration = aUnitBackoffPeriod+aTurnaroundTime+phySHRDuration+np.ceil(6*phySymbolsPerOctet)
nbytes_phy_payload = nbytes_mac_data_frame_overhead + nbytes_mac_payload
csma = csma_unslotted(collision_probability)

# FIXME: Is it enough to calculate the probabilities over the payload? PHY carries other binary information, too
fail_prob_data_frame = 1 - (1 - bit_error_ratio)**(8*nbytes_phy_payload)
fail_prob_ack_frame = 1 - (1 - bit_error_ratio)**(8*macNumBytesAckFrame)
success_prob_transmission = (1 - fail_prob_ack_frame)*(1 - fail_prob_data_frame)
print success_prob_transmission

def tx_successful():
    randnum = np.random.randint(0,1e9)
    if randnum < success_prob_transmission*1e9:
        return True
    else:
        return False

if __name__ == "__main__":
    total_sym_elapsed = 0
    total_bits_transmitted = 0

    while total_sym_elapsed*phySymbolDurationSec < t_max and total_bits_transmitted < bits_to_transmit:
        # initialize latency for this frame
        latency = 0

        # run CSMA algorithm until the frame can be sent
        success = False
        while(success == False):
            (success, delay) = csma.run()
            latency += delay

        # for a successful transmission, both data frame and ACK frame have to be received correctly
        # FIXME: add latencies below!
        if tx_successful():
            total_bits_transmitted += nbytes_phy_payload
        total_sym_elapsed += latency*phySymbolDurationSec

