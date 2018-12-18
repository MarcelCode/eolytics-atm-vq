###############################################################################################################
###############################################################################################################
### DEFINE YOUR JOB SETTINGS HERE ###
###############################################################################################################
###############################################################################################################

### PRODUCTS ###

PRODUCTLIST = 'AOT,TUR,CHL,HAB,Z90,SDD,QUT,SST,EVA'           # Product list for processing and for which polygonstatistics shall be calculated.

### SETTINGS ###

# WSR CONFIG #
MAIN_WATERTYPE = '4'                      # Original water type to be used for retrieval of water constituents (one of 4, 42, 82).
COUPLED_WSR = True                        # Retrieve atmosphere and water constituents together.
USE_SLOPY = False                         # Use aerosol-slope retreival program instead of fixed global aerosol slope. Can not be used with coupled water_species_retrieval.
WATERTYPE_MIXING = True                   # Use automatic retrieval of watertype instead of a fixed water type.

# AOI PROCESSING #
USE_IMAGEPART = True                      # Process only a portion of the full scene (either create imagepart.txt or set path to IMGPART_SHAPE).
# IMAGEPART_BUFFER = 10                     # Buffer for imagepart clipping in km (recommendation: at least 10km)
MASK_WITH_SHAPE = False                   # Mask out regions that shall not be processed (set path to MASK_IMG_SHAPE). This is different to USE_IMAGEPART, because there is no clipping involved.
CLIP_AOI = False                          # Clip AOI at the end (set path to CLIPAOI_SHAPE).
POLYGONSTATISTICS = True                  # Calculate basic statistics within a pre-defined polygon shapefile (set path to POLYGONSTATISTICS_SHAPE and adjust PRODUCTLIST_POLYSTATS).
# SHAPETORASTER_MINPERCENT = 1            # Minimum percentage of valid water pixels in shapefile after polyonstatistics

# SPECIAL PRODUCTS #
CALCULATE_RRS = True                      # Calculate Reflectance products.
RRS_CONFIG = ('rrs', 'rra', 'rrw', 'ssr') # Specification of RRS calculation (see http://172.28.1.204/projects/eowiki/wiki/WQproducts_RRS).
CALCULATE_SST = True                      # Calculate water surface temperature.
CALCULATE_EVAPORATION = True              # Calculate evaporation rate based on SST.

# OTHER SETTINGS #
ER_SETZMICH = 'er-setzmich'               # Region code for product naming. Convention it 2-digit country code, followed by a more detailed description, separated by '-' (e.g. br-riodoce).
CREATE_GMASK = True                       # Creation an initial land-water-mask on the fly based on Landsat archive (not the actual scene!).
MINIMUM_WATER_PERCENTAGE = 10.            # Compares the land-water-mask derived from the actual scene with the initial land-water-mask and declares the actual image as empty, if the detected water area is below the given threshold value compared to the gmask. Set to None if this shall not be used!
SCALED_WORKFLOW = False                   # Run the whole processing chain at 90m resolution.
PAN_SHARPENING = False                    # Processs at 15m resolution using pan-sharpening.
GLEASY = True                             # Run glint correction.
USE_STATIC_MASK_SHAPES = False            # Use pre-defined static shapes for product masking (e.g. shallow water areas; set path to STATIC_MASK_SHAPE).
# CLOUDSHADOW_DETECTION = False           # Run cloud shadow detection algorithm (might take a lot of time).
# CREATE_DATAEHEET = True                 # Create PDF with metadata and overview for each product
# DELETE_IF_EMPTY = True                  # Delete mission if an empty image is detected (either because it is totally black after clipping / masking or because the detected water area is below the threshold given in MINIMUM_WATER_PERCENTAGE).
# DELETE_MISSION = True                   # Remove mission after successful processing.

# SHAPEFILE PATHS #
IMGPART_SHAPE = os.path.join(self.missionpath, 'imagedata', 'aoi', '???.shp')                   # Shapefile from which the extent is read. Only this part of the scene will be processed. Is only used if USE_IMAGEPART is True.
MASK_IMG_SHAPE = os.path.join(self.missionpath, 'imagedata', 'aoi', '???.shp')                  # Shapefile containing the exact regions of interest. All pixels outside these polygons will be masked out during processing (speeds up the whole process). Is only used if MASK_WITH_SHAPE is True.
CLIPAOI_SHAPE = os.path.join(self.missionpath, 'imagedata', 'aoi', '???.shp')                   # Shapefile containing the exact regions of interest. At the end of the processing chain, the products will be clipped to these polygons. Also results in masking of regions out the given polygons. Only used if CLIP_AOI is True.
STATIC_MASK_SHAPE = os.path.join(self.missionpath, 'imagedata', 'mask_shapes', '???.shp')       # Shapefile containing polygons that shall be masked out, e.g. known shallow water areas. Is only used if USE_STATIC_MASK_SHAPES is True.
POLYGONSTATS_SHAPE = os.path.join(self.missionpath, 'imagedata', 'aoi', '???.shp')              # Shapefile containing the exact regions of interest. Within these polygons, basic statistics are calculated. Is only used if POLYGONSTATISTICS is True. PRODUCTLIST_POLYSTATS has to be defined as well.

# COLORBAR DEFINITION #
CB_DICT = {'TUR': 'i1_log_C1S4/TUR/TUR_i1_log75_C1S4_F2_NTU.tif',
        'CDM': 'i1_lin_C1S5/CDM/CDM_i1_lin10_C1S5_F2.tif',
        'ABS': 'i1_lin_C1S5/ABS/ABS_i1_lin10_C1S5_F2.tif',
        'SIA': 'i1_lin_C1S5/SIA/SIA_i1_lin10_C1S5_F2.tif',
        'CHL': 'i1_log_C2S8/CHL/CHL_i1_log75_C2S8_F2.tif',
        'SOA': 'i1_lin_C1S5/SOA/SOA_i1_lin10_C1S5_F2.tif',
        'DIV': 'i1_lin_C1S5/DIV/DIV_i1_lin10_C1S5_F2.tif',
        'Z90': 'Z90/Z90.tif',
        'SDD': 'SDD/SDD_F2.tif',
        'SST': 'SST/SST_F2.tif',
        'HAB': 'HAB/hab_v3_F2.tif',
        'AOT': 'AOT/aot.tif',
        'QUT': 'QUT/QUT_Legend.tif',
        'QUC': 'QUC/QUC_Legend.tif'}
