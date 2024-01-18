import numpy as np
import thumbstack
# WIP
def test_make_stack():
    """Test the procedure to create a 3D array representing
    the stack of cutout stamps.
    """
    from thumbstack.catalog import Catalog
    from thumbstack.thumbstack import Thumbstack
    from thumbstack.universe import Universe
    from thumbstack.mass_conversion import massConversionKravtsov14

    catpath = 'data/test_gal_cat.txt'
    u = Universe()
    massConv = massConversionKravtsov14()

    galcat = Catalog(u, massConv, name='test_gal_cat', pathInCatalog=catpath)

    # set up flat map
    cmb_map = # blah
    boxMask = # blah

    # make thumbstack
    ts = Thumbstack(u, galcat, cmb_map, boxMask, cmbHit=None, name='test_gal_cat', nameLong=None, save=save, nProc=nProc, filterTypes='taudiskring', doStackedMap=False, doMBins=False, test=False, doBootstrap=bootstrap)

    stack_arr = ts.build_stack()

    # check shape of stack_arr: should match length of galcat, and specified shape of cutouts
    np.testing.assert_equal(stack_arr.shape, (len(galcat), stamp_x, stamp_y))

    # apply filters to stack
    stamp_filter_profiles = ts.apply_AP_filter(filterType='diskring', n_apertures=10, r_min=1, r_max=6)
    # calculate stacked profile from filter values
    stacked_profile = ts.computeStackedProfile() 
