import numpy as np

# constants
G = 6.67408 / (10 ** 11)
M = 5.972 * (10 ** 24)
MU = 3.986004418 * (10 ** 14)

# unit conversion
KM = 1000
H = 3600

# vis-viva
def getVCircular(a):
    return np.sqrt(MU / a)

def getVElliptic(a, r):
    return np.sqrt(MU * (2 / r - 1 / a))

# orbital transfers
def hohmannTransfer(apar, atar):
    print("-------Hohmann transfer-------")

    # Maneuver 1
    vpar = getVCircular(apar)
    atrans = (apar + atar) / 2
    vtransperigee = getVElliptic(atrans, apar)
    deltaV1 = vtransperigee - vpar

    print("V parking: {0:.2f}km".format(vpar / KM))
    print("V transfer - perigee: {0:.2f}km/s".format(vtransperigee / KM))
    print("Delta V1: {0:.2f}km/s".format(deltaV1 / KM))

    # Maneuver 2
    vtransapogee = getVElliptic(atrans, atar)
    vtar = getVCircular(atar)
    deltaV2 = vtar - vtransapogee

    print("V transfer - apogee: {0:.2f}km/s".format(vtransapogee / KM))
    print("V target: {0:.2f}km/s".format(vtar / KM))
    print("Delta V2: {0:.2f}km/s".format(deltaV2 / KM))

    print("-----------------------------")

def biellipticTransfer(apar, atar, f):
    print("-------Bi-elliptic transfer-------")

    # Maneuver 1
    vpar = getVCircular(apar)
    atrans1 = (atar * f + apar) / 2
    vtrans1perigee = getVElliptic(atrans1, apar)
    deltaV1 = vtrans1perigee - vpar

    print("SMA parking: {0:.2f}km".format(apar / KM))
    print("SMA transfer 1: {0:.2f}km".format(atrans1 / KM))
    print("V transfer 1 - perigee: {0:.2f}km/s".format(vtrans1perigee / KM))
    print("Delta V1: {0:.2f}km/s".format(deltaV1 / KM))

    # Maneuver 2
    vtrans1apogee = getVElliptic(atrans1, 2 * atrans1 - apar)
    atrans2 = (2 * atrans1 - apar + atar) / 2
    vtrans2apogee = getVElliptic(atrans2, 2 * atrans1 - apar)
    deltaV2 = vtrans2apogee - vtrans1apogee

    print("SMA transfer 2: {0:.2f}km".format(atrans2 / KM))
    print("V transfer 1 - apogee: {0:.2f}km/s".format(vtrans1apogee / KM))
    print("V transfer 2 - apogee: {0:.2f}km/s".format(vtrans2apogee / KM))
    print("Delta V2: {0:.2f}km/s".format(deltaV2 / KM))

    # Maneuver 3
    vtrans2perigee = getVElliptic(atrans2, atar)
    vtar = getVCircular(atar)
    deltaV3 = vtar - vtrans2perigee

    print("V transfer 2 - perigee: {0:.2f}km".format(vtrans2perigee / KM))
    print("V target: {0:.2f}km/s".format(vtar / KM))
    print("Delta V3: {0:.2f}km/s".format(deltaV3 / KM)) 

    print("-----------------------------")

if __name__ == "__main__":
    apar = 7000 * KM
    atar = 30000 * KM
    hohmannTransfer(apar, atar)

    apar2 = 7000 * KM
    atar2 = 105000 * KM
    biellipticTransfer(apar2, atar2, 2)