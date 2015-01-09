import numpy as np

NB0 = 0 # start value for number of backoffs
CW0 = 2 # start value for contention window length
macMinBE = 3 # default value in the standard
macMaxBE = 5 # default value in the standard
macMaxCSMABackoffs = 4 # default value in the standard
aUnitBackoffPeriod = 20 # number of symbols per backoff period

SEND_SUCCESS = True
SEND_FAILURE = False

class csma_unslotted:
    def medium_busy(self, p_col):
        fac = 1e12
        tmp = np.random.randint(0,fac)
        if tmp < p_col*fac:
            # print "\tMedium busy"
            return True
        else:
            # print "\tMedium idle"
            return False

    def run(self, p_col):
        # reset everything
        NB = NB0
        BE = macMinBE
        backoff_units_elapsed = 0

        while NB <= macMaxCSMABackoffs:
            # random backoff
            backoff_units_elapsed += np.random.randint(0,2**BE)

            # CCA
            if self.medium_busy(p_col):
                NB += 1
                BE = min(BE+1, macMaxBE)
                if NB > macMaxCSMABackoffs:
                    return (SEND_FAILURE, backoff_units_elapsed*aUnitBackoffPeriod)
            else:
                return (SEND_SUCCESS, backoff_units_elapsed*aUnitBackoffPeriod)


