# -*- coding: utf-8 -*-
"""
Desc: 
Created on 27.01.22 08:55
@author: malle
"""


from datetime import datetime
from pycrown import PyCrown

if __name__ == '__main__':

    TSTART = datetime.now()

    site = 'BDM_1'  # which site to run for? [BDM_1, BDM_2, or BDM_3? Must run raster_prep.py beforehand...

    F_CHM = '/home/malle/pycrown/experiment_sites_select/'+site+'/data/CHM.tif'
    F_DTM = '/home/malle/pycrown/experiment_sites_select/'+site+'/data/DTM.tif'
    F_DSM = '/home/malle/pycrown/experiment_sites_select/'+site+'/data/DSM.tif'
    F_LAS = ''

    PC = PyCrown(F_CHM, F_DTM, F_DSM, outpath='/home/malle/pycrown/experiment_sites_select/BDM_3/lme_tmax/dalponteCIRC_numba_12mrad_ws3_chm3_thseed01_thcrown01')

    # Cut off edges
    # PC.clip_data_to_bbox((1802200, 1802400, 5467250, 5467450))

    # Smooth CHM with 5m median filter
    PC.filter_chm(3, ws_in_pixels=True)

    # Tree Detection with local maximum filter
    PC.tree_detection(PC.chm, ws=3, ws_in_pixels=True, hmin=1.5)

    # Clip trees to bounding box (no trees on image edge)
    # original extent: 1802140, 1802418, 5467295, 5467490
    # PC.clip_trees_to_bbox(bbox=(1802150, 1802408, 5467305, 5467480))
    # PC.clip_trees_to_bbox(bbox=(1802160, 1802400, 5467315, 5467470))
    # PC.clip_trees_to_bbox(inbuf=0.1)  # inward buffer of 11 metre

    # Crown Delineation
    PC.crown_delineation(algorithm='dalponteCIRC_numba', th_tree=1.5,
                         th_seed=0.1, th_crown=0.1, max_crown=12.)

    # Correct tree tops on steep terrain
    PC.correct_tree_tops()

    # Calculate tree height and elevation
    PC.get_tree_height_elevation(loc='top')
    PC.get_tree_height_elevation(loc='top_cor')

    # Screen small trees
    PC.screen_small_trees(hmin=1.5, loc='top')

    # Convert raster crowns to polygons
    PC.crowns_to_polys_raster()
    # PC.crowns_to_polys_smooth(store_las=False)

    # Check that all geometries are valid
    PC.quality_control()

    # Export results
    PC.export_raster(PC.chm, PC.outpath / 'chm.tif', 'CHM')
    PC.export_tree_locations(loc='top')
    PC.export_tree_locations(loc='top_cor')
    PC.export_tree_crowns(crowntype='crown_poly_raster')
    # PC.export_tree_crowns(crowntype='crown_poly_smooth')

    TEND = datetime.now()

    print(f"Number of trees detected: {len(PC.trees)}")
    print(f'Processing time: {TEND-TSTART} [HH:MM:SS]')
