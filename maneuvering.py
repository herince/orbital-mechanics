import numpy as np
import math

# constants
G = 6.67408 / (10 ** 11)
M = 5.972 * (10 ** 24)
MU = 3.986004418 * (10 ** 14)

# unit conversion
KM = 1000
H = 3600
DAY = 24

# vis-viva
def getVCircular(a):
    return np.sqrt(MU / a)

def getVElliptic(a, r):
    return np.sqrt(MU * (2 / r - 1 / a))

# orbital transfers
def hohmannTransfer(smaParking, smaTarget):
    print("---------Hohmann transfer----------")

    # Maneuver 1
    vParking = getVCircular(smaParking)
    smaTransfer = (smaParking + smaTarget) / 2
    vTransferPerigee = getVElliptic(smaTransfer, smaParking)
    deltaV1 = vTransferPerigee - vParking

    print("V parking: {0:.4f}km/s".format(vParking / KM))
    print("V transfer - perigee: {0:.4f}km/s".format(vTransferPerigee / KM))
    print("Delta V1: {0:.4f}km/s".format(deltaV1 / KM))

    # Maneuver 2
    vtransapogee = getVElliptic(smaTransfer, smaTarget)
    vtar = getVCircular(smaTarget)
    deltaV2 = vtar - vtransapogee

    print("V transfer - apogee: {0:.4f}km/s".format(vtransapogee / KM))
    print("V target: {0:.4f}km/s".format(vtar / KM))
    print("Delta V2: {0:.4f}km/s".format(deltaV2 / KM))

    deltaV = np.abs(deltaV1) + np.abs(deltaV2);
    print("Delta V: {0:.4f}km/s".format(deltaV / KM))

    print("-----------------------------------")

def biellipticTransfer(smaParking, smaTarget, f):
    print("--------Bi-elliptic transfer-------")

    # Maneuver 1
    vParking = getVCircular(smaParking)
    smaTrans1 = (smaTarget * f + smaParking) / 2
    vTrans1Perigee = getVElliptic(smaTrans1, smaParking)
    deltaV1 = vTrans1Perigee - vParking

    print("SMA parking: {0:.4f}km".format(smaParking / KM))
    print("SMA transfer 1: {0:.4f}km".format(smaTrans1 / KM))
    print("V transfer 1 - perigee: {0:.4f}km/s".format(vTrans1Perigee / KM))
    print("Delta V1: {0:.4f}km/s".format(deltaV1 / KM))

    # Maneuver 2
    vTrans1Apogee = getVElliptic(smaTrans1, 2 * smaTrans1 - smaParking)
    smaTrans2 = (2 * smaTrans1 - smaParking + smaTarget) / 2
    vTrans2Apogee = getVElliptic(smaTrans2, 2 * smaTrans1 - smaParking)
    deltaV2 = vTrans2Apogee - vTrans1Apogee

    print("SMA transfer 2: {0:.4f}km".format(smaTrans2 / KM))
    print("V transfer 1 - apogee: {0:.4f}km/s".format(vTrans1Apogee / KM))
    print("V transfer 2 - apogee: {0:.4f}km/s".format(vTrans2Apogee / KM))
    print("Delta V2: {0:.4f}km/s".format(deltaV2 / KM))

    # Maneuver 3
    vTrans2Perigee = getVElliptic(smaTrans2, smaTarget)
    vtar = getVCircular(smaTarget)
    deltaV3 = vtar - vTranP2perigee

    print("V transfer 2 - perigee: {0:.4f}km/s".format(vTrans2Perigee / KM))
    print("V target: {0:.4f}km/s".format(vtar / KM))
    print("Delta V3: {0:.4f}km/s".format(deltaV3 / KM)) 

    deltaV = np.abs(deltaV1) + np.abs(deltaV2) + np.abs(deltaV3);
    print("Delta V: {0:.4f}km/s".format(deltaV / KM))

    print("-----------------------------------")

def phaseTransfer(sma, gammaInit, gammaTar, n = 1):
    print("-----------Phase transfer----------")

    phase = gammaInit - gammaTar
    parkingPeriod = 2 * math.pi * np.sqrt((sma ** 3) / MU)
    transferTime = (phase / 360) * parkingPeriod
    phasePeriod = parkingPeriod + transferTime / n
    smaTransfer = (MU * ((phasePeriod / (2 * math.pi)) ** 2)) ** (1 / 3)

    print("Phase: {0:.4f}deg".format(phase))
    print("Parking period: {0:.4f}h".format(parkingPeriod / H))
    print("Transfer time: {0:.4f}h".format(transferTime / H))
    print("Phase period: {0:.4f}h".format(phasePeriod / H))
    print("SMA transfer: {0:.4f}km".format(smaTransfer / KM))

    # Calculate the velocities
    vParking = getVCircular(sma)
    vPhasePerigee = getVElliptic(smaTransfer, sma)

    print("Parking V: {0:.4f}km/s".format(vParking / KM))
    print("Phase transfer V - perigee: {0:.4f}km/s".format(vPhasePerigee / KM)) 

    # Delta V
    deltaV1 = vPhasePerigee - vParking
    deltaV2 = - deltaV1

    print("Delta V1: {0:.4f}km/s".format(deltaV1 / KM))
    print("Delta V2: {0:.4f}km/s".format(deltaV2 / KM)) 
    print("-----------------------------------")

def inclinationChange(sma, alpha):
    print("---------Inclination change--------")

    alphaInRadians = (alpha * np.pi) / 180

    # Speed in the parking orbit
    vParking = getVCircular(sma)

    # Velocities for the two impulsive burns
    deltaV1 = vParking * np.sin(alphaInRadians)
    deltaV2 = vParking * (1 - np.cos(alphaInRadians))

    print("V parking: {0:.4f}km/s".format(vParking / KM))
    print("+y component {0:.4f}km/s".format(deltaV1 / KM))
    print("-x component: {0:.4f}km/s".format(deltaV2 / KM))

    print("Delta V: {0:.4f}km/s".format(np.sqrt(deltaV1 ** 2 + deltaV2 ** 2) / KM))

    print("-----------------------------------")

if __name__ == "__main__":
    smaParking = 7000 * KM
    smaTarget = 35000 * KM
    hohmannTransfer(smaParking, smaTarget)

    smaParking2 = 7000 * KM
    smaTarget2 = 105000 * KM
    biellipticTransfer(smaParking2, smaTarget2, 2)
    hohmannTransfer(smaParking2, smaTarget2)
    biellipticTransfer(smaParking2, smaTarget2, 3)

    smaParking3 = 42164 * KM
    gammaInit = 285
    gammaTar = 145
    phaseTransfer(smaParking3, gammaInit, gammaTar)
    phaseTransfer(smaParking3, gammaInit, gammaTar, 2)
    phaseTransfer(smaParking3, gammaInit, gammaTar, 9)

    smaParking4 = 7200 * KM
    alpha = 30
    inclinationChange(smaParking4, alpha)

    smaParking5 = 30000 * KM
    inclinationChange(smaParking5, alpha)