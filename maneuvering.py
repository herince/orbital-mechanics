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
def hohmannTransfer(apar, atar):
    print("---------Hohmann transfer----------")

    # Maneuver 1
    vpar = getVCircular(apar)
    atrans = (apar + atar) / 2
    vtransperigee = getVElliptic(atrans, apar)
    deltaV1 = vtransperigee - vpar

    print("V parking: {0:.4f}km/s".format(vpar / KM))
    print("V transfer - perigee: {0:.4f}km/s".format(vtransperigee / KM))
    print("Delta V1: {0:.4f}km/s".format(deltaV1 / KM))

    # Maneuver 2
    vtransapogee = getVElliptic(atrans, atar)
    vtar = getVCircular(atar)
    deltaV2 = vtar - vtransapogee

    print("V transfer - apogee: {0:.4f}km/s".format(vtransapogee / KM))
    print("V target: {0:.4f}km/s".format(vtar / KM))
    print("Delta V2: {0:.4f}km/s".format(deltaV2 / KM))

    deltaV = np.abs(deltaV1) + np.abs(deltaV2);
    print("Delta V: {0:.4f}km/s".format(deltaV / KM))

    print("-----------------------------------")

def biellipticTransfer(apar, atar, f):
    print("--------Bi-elliptic transfer-------")

    # Maneuver 1
    vpar = getVCircular(apar)
    atrans1 = (atar * f + apar) / 2
    vtrans1perigee = getVElliptic(atrans1, apar)
    deltaV1 = vtrans1perigee - vpar

    print("SMA parking: {0:.4f}km".format(apar / KM))
    print("SMA transfer 1: {0:.4f}km".format(atrans1 / KM))
    print("V transfer 1 - perigee: {0:.4f}km/s".format(vtrans1perigee / KM))
    print("Delta V1: {0:.4f}km/s".format(deltaV1 / KM))

    # Maneuver 2
    vtrans1apogee = getVElliptic(atrans1, 2 * atrans1 - apar)
    atrans2 = (2 * atrans1 - apar + atar) / 2
    vtrans2apogee = getVElliptic(atrans2, 2 * atrans1 - apar)
    deltaV2 = vtrans2apogee - vtrans1apogee

    print("SMA transfer 2: {0:.4f}km".format(atrans2 / KM))
    print("V transfer 1 - apogee: {0:.4f}km/s".format(vtrans1apogee / KM))
    print("V transfer 2 - apogee: {0:.4f}km/s".format(vtrans2apogee / KM))
    print("Delta V2: {0:.4f}km/s".format(deltaV2 / KM))

    # Maneuver 3
    vtrans2perigee = getVElliptic(atrans2, atar)
    vtar = getVCircular(atar)
    deltaV3 = vtar - vtrans2perigee

    print("V transfer 2 - perigee: {0:.4f}km/s".format(vtrans2perigee / KM))
    print("V target: {0:.4f}km/s".format(vtar / KM))
    print("Delta V3: {0:.4f}km/s".format(deltaV3 / KM)) 

    deltaV = np.abs(deltaV1) + np.abs(deltaV2) + np.abs(deltaV3);
    print("Delta V: {0:.4f}km/s".format(deltaV / KM))

    print("-----------------------------------")

def phaseTransfer(a, gammaInit, gammaTar, n = 1):
    print("-----------Phase transfer----------")

    phase = gammaInit - gammaTar
    parkingPeriod = 2 * math.pi * np.sqrt((a ** 3) / MU)
    transferTime = (phase / 360) * parkingPeriod
    phasePeriod = parkingPeriod + transferTime / n
    aTransfer = (MU * ((phasePeriod / (2 * math.pi)) ** 2)) ** (1 / 3)

    print("Phase: {0:.4f}deg".format(phase))
    print("Parking period: {0:.4f}h".format(parkingPeriod / H))
    print("Transfer time: {0:.4f}h".format(transferTime / H))
    print("Phase period: {0:.4f}h".format(phasePeriod / H))
    print("SMA transfer: {0:.4f}km".format(aTransfer / KM))

    # Calculate the velocities
    vParking = getVCircular(a)
    vPhasePerigee = getVElliptic(aTransfer, a)

    print("Parking V: {0:.4f}km/s".format(vParking / KM))
    print("Phase transfer V - perigee: {0:.4f}km/s".format(vPhasePerigee / KM)) 

    # Delta V
    deltaV1 = vPhasePerigee - vParking
    deltaV2 = - deltaV1

    print("Delta V1: {0:.4f}km/s".format(deltaV1 / KM))
    print("Delta V2: {0:.4f}km/s".format(deltaV2 / KM)) 
    print("-----------------------------------")

def inclinationChange(a, alpha):
    print("---------Inclination change--------")

    alphaInRadians = (alpha * np.pi) / 180

    # Speed in the parking orbit
    vParking = getVCircular(a)

    # Velocities for the two impulsive burns
    deltaV1 = vParking * np.sin(alphaInRadians)
    deltaV2 = vParking * (1 - np.cos(alphaInRadians))

    print("V parking: {0:.4f}km/s".format(vParking / KM))
    print("+y component {0:.4f}km/s".format(deltaV1 / KM))
    print("-x component: {0:.4f}km/s".format(deltaV2 / KM))

    print("Delta V: {0:.4f}km/s".format(np.sqrt(deltaV1 ** 2 + deltaV2 ** 2) / KM))

    print("-----------------------------------")

if __name__ == "__main__":
    apar = 7000 * KM
    atar = 35000 * KM
    hohmannTransfer(apar, atar)

    apar2 = 7000 * KM
    atar2 = 105000 * KM
    biellipticTransfer(apar2, atar2, 2)
    hohmannTransfer(apar2, atar2)
    biellipticTransfer(apar2, atar2, 3)

    apar3 = 42164 * KM
    gammaInit = 285
    gammaTar = 145
    phaseTransfer(apar3, gammaInit, gammaTar)
    phaseTransfer(apar3, gammaInit, gammaTar, 2)
    phaseTransfer(apar3, gammaInit, gammaTar, 9)

    apar4 = 7200 * KM
    alpha = 30
    inclinationChange(apar4, alpha)

    apar5 = 30000 * KM
    inclinationChange(apar5, alpha)