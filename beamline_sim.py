# using miniconda3 to get access to Shadow3 library
import Shadow
import numpy


def sim():
    # write (1) or not (0) SHADOW files start.xx end.xx star.xx
    iwrite = 0

    #  O.E. positions in mm and ccw,deg initialization
    #  plane mirror
    class P1:
        x = 0
        y = 0
        z = 0
        xrot = 0
        yrot = 0
        zrot = 0

    #  plane mirror
    class P2:
        x = 0
        y = 0
        z = 0
        xrot = 0
        yrot = 0
        zrot = 0

    #  plane mirror
    class P3:
        x = 0
        y = 0
        z = 0
        xrot = 0
        yrot = 0
        zrot = 0

    #  plane grating
    class P4:
        x = 0
        y = 0
        z = 0
        xrot = 0
        yrot = 0
        zrot = 0

    #  ellipsoid mirror
    class P5:
        x = 0
        y = 0
        z = 0
        xrot = 0
        yrot = 0
        zrot = 0

    #  ellipsoid mirror
    class P6:
        x = 0
        y = 0
        z = 0
        xrot = 0
        yrot = 0
        zrot = 0

    #
    # Start the beam simulation
    # initialize shadow3 source (oe0) and beam
    #
    beam = Shadow.Beam()
    oe0 = Shadow.Source()
    oe1 = Shadow.OE()
    oe2 = Shadow.OE()
    oe3 = Shadow.OE()
    oe4 = Shadow.OE()
    oe5 = Shadow.OE()
    oe6 = Shadow.OE()

    #
    # Define variables. See meaning of variables in:
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/source.nml
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/oe.nml
    #

    #  undulator
    oe0.FDISTR = 3
    oe0.F_COLOR = 3
    oe0.F_PHOT = 0
    oe0.HDIV1 = 0.5
    oe0.HDIV2 = 0.5
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.NPOINT = 100000
    oe0.NTOTALPOINT = 20000
    oe0.PH1 = 499.97
    oe0.PH2 = 500.03
    oe0.SIGDIX = 1.964e-05
    oe0.SIGDIZ = 1.6349401e-05
    oe0.SIGMAX = 0.27609399
    oe0.SIGMAZ = 0.0261531994
    oe0.VDIV1 = 0.5
    oe0.VDIV2 = 0.5

    #  plane mirror
    oe1.ALPHA = 90.0
    oe1.DUMMY = 0.1
    oe1.FHIT_C = 1
    oe1.FWRITE = 3
    oe1.F_MOVE = 1
    oe1.OFFX = P1.x
    oe1.OFFY = P1.y
    oe1.OFFZ = P1.z
    oe1.RLEN1 = 260.0
    oe1.RLEN2 = 260.0
    oe1.RWIDX1 = 20.0
    oe1.RWIDX2 = 20.0
    oe1.T_IMAGE = 0.0
    oe1.T_INCIDENCE = 89.599998
    oe1.T_REFLECTION = 89.599998
    oe1.T_SOURCE = 30800.0
    oe1.X_ROT = P1.xrot
    oe1.Y_ROT = P1.yrot
    oe1.Z_ROT = P1.zrot
    #  when taking into account reflectivity
    #oe1.FILE_REFL = b"C:/cygwin64/Oasys/Si.dat"
    #oe1.F_REFLEC = 1

    #  plane mirror
    oe2.DUMMY = 0.1
    oe2.FHIT_C = 1
    oe2.FWRITE = 3
    oe2.F_MOVE = 1
    oe2.OFFX = P2.x
    oe2.OFFY = P2.y
    oe2.OFFZ = P2.z
    oe2.RLEN1 = 75.0
    oe2.RLEN2 = 75.0
    oe2.RWIDX1 = 22.5
    oe2.RWIDX2 = 22.5
    oe2.T_IMAGE = 0.0
    oe2.T_INCIDENCE = 88.5
    oe2.T_REFLECTION = 88.5
    oe2.T_SOURCE = 500.0
    oe2.X_ROT = P2.xrot
    oe2.Y_ROT = P2.yrot
    oe2.Z_ROT = P2.zrot
    #  reflect
    #oe2.FILE_REFL = b"C:/cygwin64/Oasys/Si.dat"
    #oe2.F_REFLEC = 1

    #  plane mirror
    oe3.ALPHA = 90.0
    oe3.DUMMY = 0.1
    oe3.FHIT_C = 1
    oe3.FWRITE = 3
    oe3.F_MOVE = 1
    oe3.OFFX = P3.x
    oe3.OFFY = P3.y
    oe3.OFFZ = P3.z
    oe3.RLEN1 = 190.0
    oe3.RLEN2 = 190.0
    oe3.RWIDX1 = 15.0
    oe3.RWIDX2 = 15.0
    oe3.T_IMAGE = 0.0
    oe3.T_INCIDENCE = 86.810772
    oe3.T_REFLECTION = 86.810772
    oe3.T_SOURCE = 8265.8165
    oe3.X_ROT = P3.xrot
    oe3.Y_ROT = P3.yrot
    oe3.Z_ROT = P3.zrot
    #  reflect
    #oe3.FILE_REFL = b"C:/cygwin64/Oasys/Si.dat"
    #oe3.F_REFLEC = 1

    #  plane grating
    oe4.ALPHA = 180.0
    oe4.DUMMY = 0.1
    oe4.FHIT_C = 1
    oe4.FWRITE = 2
    oe4.F_GRATING = 1
    oe4.F_MOVE = 1
    oe4.F_RULING = 5
    oe4.F_RUL_ABS = 1
    oe4.OFFX = P4.x
    oe4.OFFY = P4.y
    oe4.OFFZ = P4.z
    oe4.RLEN1 = 57.5
    oe4.RLEN2 = 57.5
    oe4.RULING = 1199.22002
    oe4.RUL_A1 = 0.165491998
    oe4.RUL_A2 = 1.0793e-05
    oe4.RUL_A3 = 1.99999999e-06
    oe4.RWIDX1 = 12.5
    oe4.RWIDX2 = 12.5
    oe4.T_IMAGE = 2000.0
    oe4.T_INCIDENCE = 87.771697
    oe4.T_REFLECTION = 85.049847
    oe4.T_SOURCE = 135.0
    oe4.X_ROT = P4.xrot
    oe4.Y_ROT = P4.yrot
    oe4.Z_ROT = P4.zrot

    #  ellipsoid mirror oe6 -> oe5 after removing slit
    oe5.ALPHA = 90.0
    oe5.AXMAJ = 33150.0
    oe5.AXMIN = 296.85199
    oe5.DUMMY = 0.1
    oe5.ELL_THE = 0.186719999
    oe5.FCYL = 1
    oe5.FHIT_C = 1
    oe5.FMIRR = 2
    oe5.FWRITE = 3
    oe5.F_EXT = 1
    oe5.F_MOVE = 1
    oe5.OFFX = P5.x
    oe5.OFFY = P5.y
    oe5.OFFZ = P5.z
    oe5.RLEN1 = 140.0
    oe5.RLEN2 = 140.0
    oe5.RWIDX1 = 7.5
    oe5.RWIDX2 = 7.5
    oe5.T_IMAGE = 0.0
    oe5.T_INCIDENCE = 88.5
    oe5.T_REFLECTION = 88.5
    oe5.T_SOURCE = 4600.0
    oe5.X_ROT = P5.xrot
    oe5.Y_ROT = P5.yrot
    oe5.Z_ROT = P5.zrot
    #  reflect
    #oe6.FILE_REFL = b"C:/cygwin64/Oasys/Si.dat"
    #oe6.F_REFLEC = 1

    #  ellipsoid mirror oe7 -> oe6 after removing slit
    oe6.ALPHA = 90.0
    oe6.AXMAJ = 3300.0
    oe6.AXMIN = 66.6355972
    oe6.DUMMY = 0.1
    oe6.ELL_THE = 1.40167999
    oe6.FCYL = 1
    oe6.FHIT_C = 1
    oe6.FMIRR = 2
    oe6.FWRITE = 3
    oe6.F_EXT = 1
    oe6.F_MOVE = 1
    oe6.OFFX = P6.x
    oe6.OFFY = P6.y
    oe6.OFFZ = P6.z
    oe6.RLEN1 = 35.0
    oe6.RLEN2 = 35.0
    oe6.RWIDX1 = 10.0
    oe6.RWIDX2 = 10.0
    oe6.T_IMAGE = 1200.0
    oe6.T_INCIDENCE = 88.5
    oe6.T_REFLECTION = 88.5
    oe6.T_SOURCE = 800.0
    oe6.X_ROT = P6.xrot
    oe6.Y_ROT = P6.yrot
    oe6.Z_ROT = P6.zrot
    #  reflect
    #oe6.FILE_REFL = b"C:/cygwin64/Oasys/Si.dat"
    #oe6.F_REFLEC = 1

    # Run SHADOW to create the source
    if iwrite:
        oe0.write("start.00")

    beam.genSource(oe0)

    if iwrite:
        oe0.write("end.00")
        beam.write("begin.dat")

    #
    # run optical element 1
    #
    print("    Running optical element: %d" % (1))
    if iwrite:
        oe1.write("start.01")

    beam.traceOE(oe1, 1)

    if iwrite:
        oe1.write("end.01")
        beam.write("star.01")

    #
    # run optical element 2
    #
    print("    Running optical element: %d" % (2))
    if iwrite:
        oe2.write("start.02")

    beam.traceOE(oe2, 2)

    if iwrite:
        oe2.write("end.02")
        beam.write("star.02")

    #
    # run optical element 3
    #
    print("    Running optical element: %d" % (3))
    if iwrite:
        oe3.write("start.03")

    beam.traceOE(oe3, 3)

    if iwrite:
        oe3.write("end.03")
        beam.write("star.03")

    #
    # run optical element 4
    #
    print("    Running optical element: %d" % (4))
    if iwrite:
        oe4.write("start.04")

    beam.traceOE(oe4, 4)

    if iwrite:
        oe4.write("end.04")
        beam.write("star.04")

    #
    # run optical element 5
    #
    print("    Running optical element: %d" % (5))
    if iwrite:
        oe5.write("start.05")

    beam.traceOE(oe5, 5)

    if iwrite:
        oe5.write("end.05")
        beam.write("star.05")

    #
    # run optical element 6
    #
    print("    Running optical element: %d" % (6))
    if iwrite:
        oe6.write("start.06")

    beam.traceOE(oe6, 6)

    if iwrite:
        oe6.write("end.06")
        beam.write("star.06")

    # return the number of good rays
    # print(str(beam.nrays(nolost=1)))
    return beam.nrays(nolost=1)


if __name__ == "__main__":
    sim()