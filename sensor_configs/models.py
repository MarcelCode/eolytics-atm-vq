from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from geodata.models import get_geodata_names
from django.utils.functional import lazy
import inspect
import sys


class Watertype(models.Model):
    ews_id = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["ews_id"]

    def __str__(self):
        return f"{self.name}"


def all_watertypes():
    return Watertype.objects.all().values_list("ews_id", "name")


# Add new sensor configs here
# Landsat 8 Settings
class ConfigLandsat8(models.Model):
    project = models.ForeignKey("projects.UserProject", on_delete=models.CASCADE)
    ews_ident = models.CharField(max_length=255, null=True, blank=True)

    config_name = models.CharField(max_length=200, unique=True, default="Default")
    default_config = models.BooleanField(default=False)

    # PRODUCTS #AOT,TUR,CHL,HAB,Z90,SDD,QUT,SST,EVA
    product_AOT = models.BooleanField(default=True, verbose_name=u"AOT")
    product_TUR = models.BooleanField(default=True, verbose_name=u"TUR")
    product_CHL = models.BooleanField(default=True, verbose_name=u"CHL")
    product_HAB = models.BooleanField(default=True, verbose_name=u"HAB")
    product_Z90 = models.BooleanField(default=True, verbose_name=u"Z90")
    product_SDD = models.BooleanField(default=True, verbose_name=u"SDD")
    product_QUT = models.BooleanField(default=True, verbose_name=u"QUT")
    product_SST = models.BooleanField(default=True, verbose_name=u"SST")
    product_EVA = models.BooleanField(default=True, verbose_name=u"EVA")

    # WSR CONFIG #
    main_watertype = models.IntegerField(default=4, choices=all_watertypes(),
                                         help_text="Original water type to be used for retrieval"
                                                   " of water constituents")

    coupled_wsr = models.BooleanField(help_text="Retrieve atmosphere and water constituents together.",
                                      default=True)
    use_slopy = models.BooleanField(default=False,
                                    help_text="Use aerosol-slope retrieval program instead of fixed global aerosol"
                                              " slope. Can not be used with"
                                              " coupled water_species_retrieval.")
    watertype_mixing = models.BooleanField(default=True,
                                           help_text="Use automatic retrieval of watertype instead of a fixed water"
                                                     " type.")

    # AOI PROCESSING #
    use_imagepart = models.BooleanField(default=True,
                                        help_text="Process only a portion of the full scene"
                                                  " (set path to Imgpart Shape)")
    mask_with_shape = models.BooleanField(default=False,
                                          help_text="Mask out regions that shall not be processed (set path to MASK_IMG"
                                                    "_SHAPE). This is different to USE"
                                                    "_IMAGEPART, because there is no clipping involved.")
    clip_aoi = models.BooleanField(default=False,
                                   help_text="Clip AOI at the end (set path to CLIPAOI_SHAPE).")
    polygonstatistics = models.BooleanField(default=True,
                                            help_text="Calculate basic statistics within a pre-defined polygon"
                                                      " shapefile (set path to POLYGONSTATISTICS"
                                                      "_SHAPE and adjust PRODUCTLIST_POLYSTATS).")

    # SPECIAL PRODUCTS #
    calculate_rrs = models.BooleanField(default=True, help_text="Calculate Reflectance products.")

    rrs_RRS = models.BooleanField(default=True, verbose_name=u"RRS")
    rrs_RRA = models.BooleanField(default=True, verbose_name=u"RRA")
    rrs_RRW = models.BooleanField(default=True, verbose_name=u"RRW")
    rrs_SSR = models.BooleanField(default=True, verbose_name=u"SSR")

    calculate_sst = models.BooleanField(default=True, help_text="Calculate water surface temperature.")
    calculate_evaporation = models.BooleanField(default=True, help_text="Calculate evaporation rate based on SST.")

    # OTHER SETTINGS
    project_name = models.CharField(max_length=200, help_text="Detailed description", blank=True)
    create_gmask = models.BooleanField(default=True,
                                       help_text="Creation an initial land-water-mask on the fly based on Landsat archive (not the actual scene!).")
    minimum_water_percentage = models.IntegerField(default=10,
                                                   validators=[MaxValueValidator(100), MinValueValidator(0)],
                                                   help_text="Compares the land-water-mask derived from the actual scene with the initial land-water-mask and"
                                                             " declares the actual image as empty, if the detected water area is below the given threshold value"
                                                             " compared to the gmask. Set to 0 if this shall not be used!")

    scaled_workflow = models.BooleanField(default=False, help_text="Run the whole processing chain at 90m resolution.")
    pan_sharpening = models.BooleanField(default=False, help_text="Processs at 15m resolution using pan-sharpening.")
    gleasy = models.BooleanField(default=True, help_text="Run glint correction.")
    use_static_mask_shape = models.BooleanField(default=False,
                                                help_text="Use pre-defined static shapes for product masking (e.g. shallow water areas; set path"
                                                          " to STATIC_MASK_SHAPE).")

    class Meta:
        unique_together = ("project", "ews_ident", "config_name")


# Sentinel 2 Settings
class ConfigSentinel2(models.Model):
    project = models.ForeignKey("projects.UserProject", on_delete=models.CASCADE)
    ews_ident = models.CharField(max_length=255, null=True, blank=True)

    config_name = models.CharField(max_length=200, default="Default")
    default_config = models.BooleanField(default=False)

    # PRODUCTS #AOT,TUR,CHL,HAB,Z90,SDD,QUT,SST,EVA
    product_AOT = models.BooleanField(default=True, verbose_name=u"AOT")
    product_TUR = models.BooleanField(default=True, verbose_name=u"TUR")
    product_CHL = models.BooleanField(default=True, verbose_name=u"CHL")
    product_HAB = models.BooleanField(default=True, verbose_name=u"HAB")
    product_Z90 = models.BooleanField(default=True, verbose_name=u"Z90")
    product_SDD = models.BooleanField(default=True, verbose_name=u"SDD")
    product_QUT = models.BooleanField(default=True, verbose_name=u"QUT")
    product_SST = models.BooleanField(default=True, verbose_name=u"SST")
    product_EVA = models.BooleanField(default=True, verbose_name=u"EVA")

    # WSR CONFIG #
    main_watertype = models.IntegerField(default=4, choices=all_watertypes(),
                                         help_text="Original water type to be used for retrieval"
                                                   " of water constituents")

    coupled_wsr = models.BooleanField(help_text="Retrieve atmosphere and water constituents together.",
                                      default=True)
    use_slopy = models.BooleanField(default=False,
                                    help_text="Use aerosol-slope retrieval program instead of fixed global aerosol"
                                              " slope. Can not be used with"
                                              " coupled water_species_retrieval.")
    watertype_mixing = models.BooleanField(default=True,
                                           help_text="Use automatic retrieval of watertype instead of a fixed water"
                                                     " type.")

    # AOI PROCESSING #
    use_imagepart = models.BooleanField(default=True,
                                        help_text="Process only a portion of the full scene"
                                                  " (set path to Imgpart Shape)")
    mask_with_shape = models.BooleanField(default=False,
                                          help_text="Mask out regions that shall not be processed (set path to MASK_IMG"
                                                    "_SHAPE). This is different to USE"
                                                    "_IMAGEPART, because there is no clipping involved.")
    clip_aoi = models.BooleanField(default=False,
                                   help_text="Clip AOI at the end (set path to CLIPAOI_SHAPE).")
    polygonstatistics = models.BooleanField(default=True,
                                            help_text="Calculate basic statistics within a pre-defined polygon"
                                                      " shapefile (set path to POLYGONSTATISTICS"
                                                      "_SHAPE and adjust PRODUCTLIST_POLYSTATS).")

    # SPECIAL PRODUCTS #
    calculate_rrs = models.BooleanField(default=True, help_text="Calculate Reflectance products.")

    rrs_RRS = models.BooleanField(default=True, verbose_name=u"RRS")
    rrs_RRA = models.BooleanField(default=True, verbose_name=u"RRA")
    rrs_RRW = models.BooleanField(default=True, verbose_name=u"RRW")
    rrs_SSR = models.BooleanField(default=True, verbose_name=u"SSR")

    calculate_sst = models.BooleanField(default=True, help_text="Calculate water surface temperature.")
    calculate_evaporation = models.BooleanField(default=True, help_text="Calculate evaporation rate based on SST.")

    # OTHER SETTINGS
    project_name = models.CharField(max_length=200, help_text="Detailed description", blank=True, null=True)
    create_gmask = models.BooleanField(default=True,
                                       help_text="Creation an initial land-water-mask on the fly based on Landsat archive (not the actual scene!).")
    minimum_water_percentage = models.IntegerField(default=10,
                                                   validators=[MaxValueValidator(100), MinValueValidator(0)],
                                                   help_text="Compares the land-water-mask derived from the actual scene with the initial land-water-mask and"
                                                             " declares the actual image as empty, if the detected water area is below the given threshold value"
                                                             " compared to the gmask. Set to 0 if this shall not be used!")

    scaled_workflow = models.BooleanField(default=False, help_text="Run the whole processing chain at 90m resolution.")
    pan_sharpening = models.BooleanField(default=False, help_text="Processs at 15m resolution using pan-sharpening.")
    gleasy = models.BooleanField(default=True, help_text="Run glint correction.")
    use_static_mask_shape = models.BooleanField(default=False,
                                                help_text="Use pre-defined static shapes for product masking (e.g. shallow water areas; set path"
                                                          " to STATIC_MASK_SHAPE).")

    class Meta:
        unique_together = ("project", "ews_ident", "config_name")


def get_config_model_names():
    names = [name for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isclass(obj) and
             name.startswith("Config")]

    return names


config_model_names = get_config_model_names()
CONFIG_CHOICES = zip(config_model_names, config_model_names)

geodata_model_names = get_geodata_names()
GEODATA_CHOICES = zip(geodata_model_names, geodata_model_names)


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=100)
    ews_id = models.IntegerField()
    geodata_model = models.CharField(max_length=50, choices=GEODATA_CHOICES)
    config_model = models.CharField(max_length=50, choices=CONFIG_CHOICES)

    def __str__(self):
        return f'{self.sensor_name}'
