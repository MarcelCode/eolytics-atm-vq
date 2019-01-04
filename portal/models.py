from django.db import models
from geodata import models as geomodels
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from geodata.models import get_geometry_objects
import inspect
import sys

geodata_models = get_geometry_objects().keys()
GEODATA_CHOICES = zip(geodata_models, geodata_models)


class Sensor(models.Model):
    sensor = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    geodata_model = models.CharField(max_length=30, choices=GEODATA_CHOICES)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sensor)
        super(Sensor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.sensor}'


# Landsat Settings
class Products(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class RrsConfig(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


def all_products():
    return Products.objects.all()


def all_rrs_config():
    return RrsConfig.objects.all()


class Landsat8(models.Model):
    WATERTYPE_CHOICES = (
        ("4", "4"),
        ("42", "42"),
        ("82", "82"),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    config_name = models.CharField(max_length=200, unique=True)
    default_config = models.BooleanField(default=False)

    # PRODUCTS #
    product_list = models.ManyToManyField(Products,
                                          help_text="Product list for processing and for which polygon statistics"
                                                    " shall be calculated.", default=all_products)

    # WSR CONFIG #
    main_watertype = models.CharField(max_length=50, choices=WATERTYPE_CHOICES, default="4",
                                      help_text="Original water type to be used for retrieval of water constituents")
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
    rrs_config = models.ManyToManyField(RrsConfig, default=all_rrs_config, help_text="Specification of RRS calculation")
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

    def __str__(self):
        return f"{self.user}_{self.pk}"


# Sentinel Settings
class Sentinel2(models.Model):
    WATERTYPE_CHOICES = (
        ("4", "4"),
        ("42", "42"),
        ("82", "82"),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    config_name = models.CharField(max_length=200, unique=True)
    default_config = models.BooleanField(default=False)

    # PRODUCTS #
    product_list = models.ManyToManyField(Products,
                                          help_text="Product list for processing and for which polygon statistics"
                                                    " shall be calculated.", default=all_products)

    # WSR CONFIG #
    main_watertype = models.CharField(max_length=50, choices=WATERTYPE_CHOICES, default="4",
                                      help_text="Original water type to be used for retrieval of water constituents")
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
    rrs_config = models.ManyToManyField(RrsConfig, default=all_rrs_config, help_text="Specification of RRS calculation")
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

    def __str__(self):
        return f"{self.user}_{self.pk}"


def get_model_objects():
    classes = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes[name] = obj

    return classes