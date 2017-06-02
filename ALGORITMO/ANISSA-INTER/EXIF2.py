#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
#
# VERSION 1.1.0
#
# To use this library call with:
#    f = open(path_name, 'rb')
#    tags = EXIF.process_file(f)
#
# Note that the dictionary keys are the IFD name followed by the
# tag name. For example:
# 'EXIF DateTimeOriginal', 'Image Orientation', 'MakerNote FocusMode'
#
# Copyright (c) 2002-2007 Gene Cash All rights reserved
# Copyright (c) 2007-2008 Ianaré Sévi All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#
#  3. Neither the name of the authors nor the names of its contributors
#     may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# ----- See 'changes.txt' file for all contributors and changes ----- #
#


# Don't throw an exception when given an out of range character.

"""
\package EXIF
\brief This module manages all the functionality related to extract EXIF information of a file.
"""
import re#paquete para el uso de expresiones regulares
import types#util para conocer tipos

def make_string(seq):
    """
    \brief Constructs a string from a sequence.
    \param seq (char sequence) Sequence of char.
    \return (str) String constructed by char sequence.
    """
    str = ""
    for c in seq:
        # Screen out non-printing characters
        if 32 <= c and c < 256:
            str += chr(c)
        else:                   #añadido 2011-09-18 Ana
            if c == 00:           #añadido 2011-09-18 Ana
                str += chr(32)  #añadido 2011-09-18 Ana
    # If no printing chars
    if not str:
        return seq
    return str

def make_string_uc(seq):
    """
    \brief Special version to deal with the code in the first 8 bytes of a user comment.
    \param seq (char sequence) Sequence of char.
    \return (str) First 8 bytes gives coding system e.g. ASCII vs. JIS vs Unicode.
    """
    code = seq[0:8]
    seq = seq[8:]
    # Of course, this is only correct if ASCII, and the standard explicitly
    # allows JIS and Unicode.
    return make_string(seq)

## Field type descriptions as (length, abbreviation, full name) tuples
FIELD_TYPES = (
    (0, 'X', 'Proprietary'), # no such type
    (1, 'B', 'Byte'),
    (1, 'A', 'ASCII'),
    (2, 'S', 'Short'),
    (4, 'L', 'Long'),
    (8, 'R', 'Ratio'),
    (1, 'SB', 'Signed Byte'),
    (1, 'U', 'Undefined'),
    (2, 'SS', 'Signed Short'),
    (4, 'SL', 'Signed Long'),
    (8, 'SR', 'Signed Ratio'),
    (4, 'SorL', 'Short or Long')
    )

## Dictionary of main EXIF tag names
## first element of tuple is tag name, optional second element is
## another dictionary giving names to values

##EL SEGUNDO ELEMENTO PASA A SER EL CUARTO AL SER OPCIONAL, 
##EN EL SEGUNDO LUGAR QUEDA EL TIPO FIJO DEL TAG Y EN EL TERCERO EL NUMERO DE ELEMENTOS FIJO(SI NO LO HAY SERA 0)
##SOLO HAY UN CASO DE DOBLE TIPO, SHORT Y LONG REPRESENTADO POR "11"
EXIF_TAGS = {
    0x0100: ('ImageWidth', 11, 1,),
    0x0101: ('ImageLength', 11, 1,),
    0x0102: ('BitsPerSample', 3, 3,),
    0x0103: ('Compression', 3, 1,
             {1: 'Uncompressed',
              2: 'CCITT 1D',
              3: 'T4/Group 3 Fax',
              4: 'T6/Group 4 Fax',
              5: 'LZW',
              6: 'JPEG (old-style)',
              7: 'JPEG',
              8: 'Adobe Deflate',
              9: 'JBIG B&W',
              10: 'JBIG Color',
              32766: 'Next',
              32769: 'Epson ERF Compressed',
              32771: 'CCIRLEW',
              32773: 'PackBits',
              32809: 'Thunderscan',
              32895: 'IT8CTPAD',
              32896: 'IT8LW',
              32897: 'IT8MP',
              32898: 'IT8BL',
              32908: 'PixarFilm',
              32909: 'PixarLog',
              32946: 'Deflate',
              32947: 'DCS',
              34661: 'JBIG',
              34676: 'SGILog',
              34677: 'SGILog24',
              34712: 'JPEG 2000',
              34713: 'Nikon NEF Compressed',
              65000: 'Kodak DCR Compressed',
              65535: 'Pentax PEF Compressed'}),
    0x0106: ('PhotometricInterpretation', 3, 1,),
    0x0107: ('Thresholding',),
    0x010A: ('FillOrder',),
    0x010D: ('DocumentName',),
    0x010E: ('ImageDescription', 2, 0,),
    0x010F: ('Make', 2, 0,),
    0x0110: ('Model', 2, 0,),
    0x0111: ('StripOffsets', 11, 0,),
    0x0112: ('Orientation', 3, 1,
             {1: 'Horizontal (normal)',
              2: 'Mirrored horizontal',
              3: 'Rotated 180',
              4: 'Mirrored vertical',
              5: 'Mirrored horizontal then rotated 90 CCW',
              6: 'Rotated 90 CW',
              7: 'Mirrored horizontal then rotated 90 CW',
              8: 'Rotated 90 CCW'}),
    0x0115: ('SamplesPerPixel', 3, 1,),
    0x0116: ('RowsPerStrip', 11, 1,),
    0x0117: ('StripByteCounts', 11, 1,),
    0x011A: ('XResolution', 5, 1,),
    0x011B: ('YResolution', 5, 1,),
    0x011C: ('PlanarConfiguration', 3, 1,),
    0x011D: ('PageName', make_string),
    0x0128: ('ResolutionUnit', 3, 1,
             {1: 'Not Absolute',
              2: 'Pixels/Inch',
              3: 'Pixels/Centimeter'}),
    0x012D: ('TransferFunction', 3, 3 * 256,),
    0x0131: ('Software', 2, 0,),
    0x0132: ('DateTime', 2, 20,),
    0x013B: ('Artist', 2, 0,),
    0x013E: ('WhitePoint', 5, 2,),
    0x013F: ('PrimaryChromaticities', 5, 6,),
    0x0156: ('TransferRange',),
    0x0200: ('JPEGProc',),
    0x0201: ('JPEGInterchangeFormat', 4, 1,),
    0x0202: ('JPEGInterchangeFormatLength', 4, 1,),
    0x0211: ('YCbCrCoefficients', 5, 3,),
    0x0212: ('YCbCrSubSampling', 3, 2,),
    0x0213: ('YCbCrPositioning', 3, 1,
             {1: 'Centered',
              2: 'Co-sited'}),
    0x0214: ('ReferenceBlackWhite', 5, 6,),
    
    0x4746: ('Rating',),
    
    0x828D: ('CFARepeatPatternDim',),
    0x828E: ('CVAPattern',),
    0x828F: ('BatteryLevel',),
    0x8298: ('Copyright', 2, 0,),
    0x829A: ('ExposureTime', 5, 1,),
    0x829D: ('FNumber', 5, 1,),
    0x83BB: ('IPTC/NAA',),
    0x8769: ('ExifOffset',),
    0x8773: ('InterColorProfile',),
    0x8822: ('ExposureProgram', 3, 1,
             {0: 'Unidentified',
              1: 'Manual',
              2: 'Program Normal',
              3: 'Aperture Priority',
              4: 'Shutter Priority',
              5: 'Program Creative',
              6: 'Program Action',
              7: 'Portrait Mode',
              8: 'Landscape Mode'}),
    0x8824: ('SpectralSensitivity', 2, 0,),
    0x8825: ('GPSInfo',),
    0x8827: ('PhotographicSensitivity', 3, 0,), #0x8827: ('ISOSpeedRatings', ), FIXME ANA
    0x8828: ('OECF', 7, 0,),
    0x8830: ('SensitivityType', 3, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x8831: ('StandardOutputSensitivity', 4, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x8832: ('RecommendedExposureIndex', 4, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x8833: ('ISOSpeed', 4, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x8834: ('ISOSpeedLatitudeyyy', 4, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x8835: ('ISOSpeedLatitudezzz', 4, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x9000: ('ExifVersion', 7, 4, make_string),
    0x9003: ('DateTimeOriginal', 2, 20,),
    0x9004: ('DateTimeDigitized', 2, 20,),
    0x9101: ('ComponentsConfiguration', 7, 4,
             {0: '',
              1: 'Y',
              2: 'Cb',
              3: 'Cr',
              4: 'Red',
              5: 'Green',
              6: 'Blue'}),
    0x9102: ('CompressedBitsPerPixel', 5, 1,),
    0x9201: ('ShutterSpeedValue', 10, 1,),
    0x9202: ('ApertureValue', 5, 1,),
    0x9203: ('BrightnessValue', 10, 1,),
    0x9204: ('ExposureBiasValue', 10, 1,),
    0x9205: ('MaxApertureValue', 5, 1,),
    0x9206: ('SubjectDistance', 5, 1,),
    0x9207: ('MeteringMode', 3, 1,
             {0: 'Unidentified',
              1: 'Average',
              2: 'CenterWeightedAverage',
              3: 'Spot',
              4: 'MultiSpot',
              5: 'Pattern'}),
    0x9208: ('LightSource', 3, 1,
             {0: 'Unknown',
              1: 'Daylight',
              2: 'Fluorescent',
              3: 'Tungsten',
              9: 'Fine Weather',
              10: 'Flash',
              11: 'Shade',
              12: 'Daylight Fluorescent',
              13: 'Day White Fluorescent',
              14: 'Cool White Fluorescent',
              15: 'White Fluorescent',
              17: 'Standard Light A',
              18: 'Standard Light B',
              19: 'Standard Light C',
              20: 'D55',
              21: 'D65',
              22: 'D75',
              255: 'Other'}),
    0x9209: ('Flash', 3, 1,
             {0: 'No',
              1: 'Fired',
              5: 'Fired (?)', # no return sensed
              7: 'Fired (!)', # return sensed
              9: 'Fill Fired',
              13: 'Fill Fired (?)',
              15: 'Fill Fired (!)',
              16: 'Off',
              24: 'Auto Off',
              25: 'Auto Fired',
              29: 'Auto Fired (?)',
              31: 'Auto Fired (!)',
              32: 'Not Available'}),
    0x920A: ('FocalLength', 5, 1,),
    0x9214: ('SubjectArea', 3, [2, 3, 4],),
    0x927C: ('MakerNote', 7, 0,),
    #0x9286: ('UserComment',7, 0, make_string_uc),
    0x9286: ('UserComment', 7, 0,),
    0x9290: ('SubSecTime', 2, 0,),
    0x9291: ('SubSecTimeOriginal', 2, 0,),
    0x9292: ('SubSecTimeDigitized', 2, 0,),
    
    # used by Windows Explorer
    0x9C9B: ('XPTitle',),
    0x9C9C: ('XPComment',),
    0x9C9D: ('XPAuthor',), #(ignored by Windows Explorer if Artist exists)
    0x9C9E: ('XPKeywords',),
    0x9C9F: ('XPSubject',),

    0xA000: ('FlashPixVersion', 7, 4, make_string),
    0xA001: ('ColorSpace', 3, 1,
             {1: 'sRGB',
              2: 'Adobe RGB',
              65535: 'Uncalibrated'}),
    0xA002: ('PixelXDimension', 11, 1,), # 0xA002: ('ExifImageWidth', ), FIXME ANA
    0xA003: ('PixelYDimension', 11, 1,), #0xA003: ('ExifImageLength', ), FIXME ANA
    0xA004: ('RelatedSoundFile', 2, 13,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA005: ('InteroperabilityOffset',),
    0xA20B: ('FlashEnergy', 5, 1,), # 0x920B in TIFF/EP
    0xA20C: ('SpatialFrequencyResponse', 7, 0,), # 0x920C
    0xA20E: ('FocalPlaneXResolution', 5, 1,), # 0x920E
    0xA20F: ('FocalPlaneYResolution', 5, 1,), # 0x920F
    0xA210: ('FocalPlaneResolutionUnit', 3, 1,), # 0x9210
    0xA214: ('SubjectLocation', 3, 2,), # 0x9214
    0xA215: ('ExposureIndex', 5, 1,), # 0x9215
    0xA217: ('SensingMethod', 3, 1, # 0x9217
             {1: 'Not defined',
              2: 'One-chip color area',
              3: 'Two-chip color area',
              4: 'Three-chip color area',
              5: 'Color sequential area',
              7: 'Trilinear',
              8: 'Color sequential linear'}),
    0xA300: ('FileSource', 7, 1,
             {1: 'Film Scanner',
              2: 'Reflection Print Scanner',
              3: 'Digital Camera'}),
    0xA301: ('SceneType', 3, 1,
             {1: 'Directly Photographed'}),
    0xA302: ('CFAPattern', 3, 0,),
    0xA401: ('CustomRendered', 3, 1,
             {0: 'Normal',
              1: 'Custom'}),
    0xA402: ('ExposureMode', 3, 1,
             {0: 'Auto Exposure',
              1: 'Manual Exposure',
              2: 'Auto Bracket'}),
    0xA403: ('WhiteBalance', 3, 1,
             {0: 'Auto',
              1: 'Manual'}),
    0xA404: ('DigitalZoomRatio', 5, 1,),
    0xA405: ('FocalLengthIn35mmFilm', 3, 1,),
    0xA406: ('SceneCaptureType', 3, 1,
             {0: 'Standard',
              1: 'Landscape',
              2: 'Portrait',
              3: 'Night)'}),
    0xA407: ('GainControl', 5, 1,
             {0: 'None',
              1: 'Low gain up',
              2: 'High gain up',
              3: 'Low gain down',
              4: 'High gain down'}),
    0xA408: ('Contrast', 3, 1,
             {0: 'Normal',
              1: 'Soft',
              2: 'Hard'}),
    0xA409: ('Saturation', 3, 1,
             {0: 'Normal',
              1: 'Soft',
              2: 'Hard'}),
    0xA40A: ('Sharpness', 3, 1,
             {0: 'Normal',
              1: 'Soft',
              2: 'Hard'}),
    0xA40B: ('DeviceSettingDescription', 7, 0,),
    0xA40C: ('SubjectDistanceRange', 3, 1,),
    0xA420: ('ImageUniqueID', 2, 33,), #Adicionado por standard exif 2.2 y 2.3 FIXME ANA
    0xA430: ('CameraOwnerName', 2, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA431: ('BodySerialNumber', 2, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA432: ('LensSpecification', 5, 4,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA433: ('LensMake', 2, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA434: ('LensModel', 2, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA435: ('LensSerialNumber', 2, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0xA500: ('Gamma', 5, 1,),
    0xC4A5: ('PrintIM',),
    0xEA1C:	('Padding',),
    0xEA1D: ('OffsetSchema',), #Adicionado por Microsoft  para almacenar el MarkerNotes original FIXME ANA
    }

## Interoperability tags
INTR_TAGS = {
    0x0001: ('InteroperabilityIndex', 2, 0,),
    0x0002: ('InteroperabilityVersion',),
    0x1000: ('RelatedImageFileFormat',),
    0x1001: ('RelatedImageWidth',),
    0x1002: ('RelatedImageLength',),
    }

## GPS tags.
GPS_TAGS = {
    0x0000: ('GPSVersionID', 1, 4,),
    0x0001: ('GPSLatitudeRef', 2, 2,),
    0x0002: ('GPSLatitude', 5, 3,),
    0x0003: ('GPSLongitudeRef', 2, 2,),
    0x0004: ('GPSLongitude', 5, 3,),
    0x0005: ('GPSAltitudeRef', 1, 1,),
    0x0006: ('GPSAltitude', 5, 1,),
    0x0007: ('GPSTimeStamp', 5, 3,),
    0x0008: ('GPSSatellites', 2, 0,),
    0x0009: ('GPSStatus', 2, 2,),
    0x000A: ('GPSMeasureMode', 2, 2,),
    0x000B: ('GPSDOP', 5, 1,),
    0x000C: ('GPSSpeedRef', 2, 2,),
    0x000D: ('GPSSpeed', 5, 1,),
    0x000E: ('GPSTrackRef', 2, 2,),
    0x000F: ('GPSTrack', 5, 1,),
    0x0010: ('GPSImgDirectionRef', 2, 2,),
    0x0011: ('GPSImgDirection', 5, 1,),
    0x0012: ('GPSMapDatum', 2, 0,),
    0x0013: ('GPSDestLatitudeRef', 2, 2,),
    0x0014: ('GPSDestLatitude', 5, 3,),
    0x0015: ('GPSDestLongitudeRef', 2, 2,),
    0x0016: ('GPSDestLongitude', 5, 3,),
    0x0017: ('GPSDestBearingRef', 2, 2,),
    0x0018: ('GPSDestBearing', 5, 1,),
    0x0019: ('GPSDestDistanceRef', 2, 2,),
    0x001A: ('GPSDestDistance', 5, 1,),
    0x001B: ('GPSProcessingMethod', 7, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0x001C: ('GPSAreaInformation', 7, 0,), #Adicionado por standard exif 2.3 FIXME ANA
    0x001D: ('GPSDateStamp', 2, 11,), #0x001D: ('GPSDate', ), FIXME ANA
    0x001E: ('GPSDifferential', 3, 1,), #Adicionado por standard exif 2.3 FIXME ANA
    0x001F: ('GPSHPositioningError', 5, 1,), #Adicionado por standard exif 2.3 FIXME ANA

    }

## Ignore these tags when quick processing
## 0x927C is MakerNote Tags
## 0x9286 is user comment
IGNORE_TAGS = (0x9286, 0x927C)

##Tags que siempre deben estar, 4 tipos: TagCh chunky, TagPl planar, TagYCC y TagCompressed para comprimidos
TagChImage = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'XResolution', 'YResolution', 'ResolutionUnit', 'ExifOffset', 'ExifVersion', 'FlashPixVersion', 'ColorSpace']
TagChThumbnail = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'XResolution', 'YResolution', 'ResolutionUnit']

TagPlImage = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'XResolution', 'YResolution', 'ResolutionUnit', 'ExifOffset', 'ExifVersion', 'FlashPixVersion', 'ColorSpace']
TagPlThumbnail = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'XResolution', 'YResolution', 'PlanarConfiguration', 'ResolutionUnit']

TagYCCImage = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'XResolution', 'YResolution', 'ResolutionUnit', 'YCbCrSubSampling', 'YCbCrPositioning', 'ExifOffset', 'ExifVersion', 'FlashPixVersion', 'ColorSpace']
TagYCCThumbnail = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'XResolution', 'YResolution', 'ResolutionUnit', 'YCbCrSubSampling']

TagCompressedImage = ['XResolution', 'YResolution', 'ResolutionUnit', 'YCbCrPositioning', 'ExifOffset', 'ExifVersion', 'ComponentsConfiguration', 'FlashPixVersion', 'ColorSpace', 'PixelXDimension', 'PixelYDimension']
TagCompressedThumbnail = ['Compression', 'XResolution', 'YResolution', 'ResolutionUnit', 'JPEGInterchangeFormat', 'JPEGInterchangeFormatLength']


##Tags que NO deben estar
notTagChImage = ['JPEGInterchangeFormat', 'JPEGInterchangeFormatLength', 'YCbCrCoefficients', 'YCbCrSubSampling', 'YCbCrPositioning', 'ComponentsConfiguration', 'CompressedBitsPerPixel', 'PixelXDimension', 'PixelYDimension', 'InteroperabilityOffset']
notTagChInteroperability = ['InteroperabilityIndex']
notTagChThumbnail = ['JPEGInterchangeFormat', 'JPEGInterchangeFormatLength', 'YCbCrCoefficients', 'YCbCrSubSampling', 'YCbCrPositioning']

notTagPlImage = ['JPEGInterchangeFormat', 'JPEGInterchangeFormatLength', 'YCbCrCoefficients', 'YCbCrSubSampling', 'YCbCrPositioning', 'ComponentsConfiguration', 'CompressedBitsPerPixel', 'PixelXDimension', 'PixelYDimension', 'InteroperabilityOffset']
notTagPlInteroperability = ['InteroperabilityIndex']
notTagPlThumbnail = ['JPEGInterchangeFormat', 'JPEGInterchangeFormatLength', 'YCbCrCoefficients', 'YCbCrSubSampling', 'YCbCrPositioning']

notTagYCCImage = ['JPEGInterchangeFormat', 'JPEGInterchangeFormatLength', 'ComponentsConfiguration', 'CompressedBitsPerPixel', 'PixelXDimension', 'PixelYDimension', 'InteroperabilityOffset']
notTagYCCInteroperability = ['InteroperabilityIndex'] 
notTagYCCThumbnail = ['JPEGInterchangeFormat', 'JPEGInterchangeFormatLength']

notTagCompressedImage = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'Compression', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'PlanarConfiguration', 'JPEGInterchangeFormat', 'JPEGInterchangeFormatLength', 'YCbCrSubSampling']
notTagCompressedThumbnail = ['ImageWidth', 'ImageLength', 'BitsPerSample', 'PhotometricInterpretation', 'StripOffsets', 'SamplesPerPixel', 'RowsPerStrip', 'StripByteCounts', 'PlanarConfiguration', 'YCbCrSubSampling']


def s2n_motorola(str):
    """
     \brief Extract multibyte integer in Motorola format (little endian)
    """
    x = 0
    for c in str:
        x = (x << 8) | ord(c)
    return x


def s2n_intel(str):
    """
     \brief Extract multibyte integer in Intel format (big endian)
    """
    x = 0
    y = 0L
    for c in str:
        x = x | (ord(c) << y)
        y = y + 8
    return x


def gcd(a, b):
    """
     \brief ratio object that eventually will be able to reduce itself to lowest
        common denominator for printing
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

class Ratio:
    """ 
    \brief Class that manages Ratio type.   
    """ 
    
    def __init__(self, num, den):
        """
        \brief Initialize all the components of Ratio class.
        \param self (EXIF::Ratio).
        \param num (float) Numerator.
        \param den (float) Denominator.       
        \return No return.
         """
        ## Ratio numerator.
        self.num = num
        ## Ratio denominator.
        self.den = den

    def __repr__(self):
        """
        \brief This method show de information of Ratio Class as string.
        \param self (EXIF::Ratio).
        \return (str) String with Ratio type information.
         """
        self.reduce()
        if self.den == 1:
            return str(self.num)
        return '%d/%d' % (self.num, self.den)

    def reduce(self):
        """
        \brief This method reduce Ratio type.
        \param self (EXIF::Ratio).
        \return No return.
         """
        div = gcd(self.num, self.den)
        if div > 1:
            self.num = self.num / div
            self.den = self.den / div

# 
class IFD_Tag:
    """ 
    \brief Class for ease of dealing with tags.  
    """ 
    def __init__(self, printable, tag, field_type, values, field_offset,
                 field_length):
        """
        \brief Initialize all the components IFD_Tag class.
        \param self (EXIF::IFD_Tag). 
        \param printable (str) String value to print.
        \param tag Tag value.    
        \param field_type Field type.
        \param values List of tag values. 
        \param field_offset Field tag offset.
        \param field_length Field tag length.
        \return No return.
        """
        # Si el valor está vacío se presenta un error
        if(len(printable) > 0):          #Agregado Ana Sandoval
            ## (str) Printable version of data
            self.printable = printable
        else:                       #Agregado Ana Sandoval
            self.printable = ""        #Agregado Ana Sandoval
        ## (int) Tag ID number
        self.tag = tag
        ## (int) Field type as index into FIELD_TYPES
        self.field_type = field_type
        ## (int) Offset of start of field in bytes from beginning of IFD
        self.field_offset = field_offset
        ## (int) Length of data field in bytes
        self.field_length = field_length
        
        # Si el valor está vacío se presenta un error
        if(len(values) > 0):          #Agregado Ana Sandoval
            ## (str) Either a string or array of data items
            self.values = values
        else:                       #Agregado Ana Sandoval
            self.values = ""        #Agregado Ana Sandoval

    
    def __str__(self):
        """
        \brief Method to obtain string printable. 
        \param self (EXIF::IFD_Tag). 
        \return String printable information.
        """
        return self.printable

    def __repr__(self):
        """
        \brief Method to obtain string printable (0xTag Field Type=Tag Value Offset).
        \param self (EXIF::IFD_Tag). 
        \return String printable information.
        """
        return '(0x%04X) %s=%s @ %d' % (self.tag,
                                        FIELD_TYPES[self.field_type][2],
                                        self.printable,
                                        self.field_offset)


class EXIF_header:
    """
    \brief Class that handles an EXIF header
    """
    
    def __init__(self, file, endian, offset, fake_exif, strict, detecErr, debug=0):
        """
        \brief Initialize all the components IFD_Tag class.
        \param self (EXIF::EXIF_header). 
        \param file (str) File.
        \param endian (str) Endian.    
        \param offset (int) Offset.
        \param fake_exif (int) Fake exif. 
        \param strict (bool) True to return an error on invalid tags, False in other case.
        \param debug (bool) Debug (default 0).
        \return No return.
        """
        ## (str) File to be treated
        self.file = file
        ## (str) Type of endian Motorola or Intel
        self.endian = endian
        ## (str) Initial offset.
        self.offset = offset
        ## (int) Fake exif.
        self.fake_exif = fake_exif
        ## (bool) True to return an error on invalid tags, False in other case.
        self.strict = strict
        ## (bool) Debug.
        self.debug = debug
        ## (dictionary) Tags will be a dictionary mapping names of EXIF tags to their values in the file named by path_name.
        self.tags = {}
        ## (bool) deteccion errores
        self.detecErr = detecErr
        ## (dictionary) Tags con error(clave), tipo de error(valor)
        self.errors = {}

    def s2n(self, offset, length, signed=0):
        """
        \brief Convert slice to integer, based on sign and endian flags
         usually this offset is assumed to be relative to the beginning of the
         start of the EXIF information.  For some cameras that use relative tags,
         this offset may be relative to some other starting point.
        \param self (EXIF::EXIF_header).
        \param offset (int) Offset.
        \param length (int) Length.
        \param signed (int) Signed (default 0).
        \return (int).
        """
        self.file.seek(self.offset + offset)
        slice = self.file.read(length)
        if self.endian == 'I':
            val = s2n_intel(slice)
        else:
            val = s2n_motorola(slice)
        # Sign extension ?
        if signed:
            msb = 1L << (8 * length - 1)
            if val & msb:
                val = val - (msb << 1)
        return val


    def n2s(self, offset, length):
        """
        \brief Convert offset to string.
        \param self (EXIF::EXIF_header).
        \param offset (int) Offset.
        \param length (int) Length.
        \return (str).
        """
        s = ''
        for dummy in range(length):
            if self.endian == 'I':
                s = s + chr(offset & 0xFF)
            else:
                s = chr(offset & 0xFF) + s
            offset = offset >> 8
        return s

    def first_IFD(self):
        """
        \brief Return first IFD.
        \param self (EXIF::EXIF_header).
        \return (int).
        """
        return self.s2n(4, 4)

    def next_IFD(self, ifd):
        """
        \brief Return pointer to next IFD.
        \param self (EXIF::EXIF_header).
        \param ifd (int) IFD.
        \return (int).
        """
        entries = self.s2n(ifd, 2)
        return self.s2n(ifd + 2 + 12 * entries, 4)

    def list_IFDs(self):
        """
        \brief Return list of IFDs in header.
        \param self (EXIF::EXIF_header).
        \return (list).
        """
        i = self.first_IFD()
        a = []
        while i:
            a.append(i)
            i = self.next_IFD(i)
        return a


    def dump_IFD(self, ifd, ifd_name, dict=EXIF_TAGS, relative=0, stop_tag='UNDEF'):
        """
        \brief Return list of entries in this IFD.
        \param self (EXIF::EXIF_header).
        \param ifd Ifd.
        \param ifd_name Ifd name.
        \param dict (dictionary) Dictionary (default EXIF_TAGS).
        \param relative (int) Relative (default 0).
        \param stop_tag (str) Tag to stop scanning (default 'UNDEF'). 
        \return No return.
        """
        entries = self.s2n(ifd, 2)
        print ifd_name
        for i in range(entries):
            # entry is index of start of this IFD in the file
            entry = ifd + 2 + 12 * i
            tag = self.s2n(entry, 2)
            doubleValue = False#iniciamos el valor doble a falso
            # get tag name early to avoid errors, help debug
            tag_entry = dict.get(tag)  
            print tag_entry
            if tag_entry:
                tag_name = tag_entry[0]
            else:
                tag_name = 'Tag 0x%04X' % tag
            # ignore certain tags for faster processing
            if not (not detailed and tag in IGNORE_TAGS) and tag_entry:
                field_type = self.s2n(entry + 2, 2)
                
                # unknown field type
                if not 0 < field_type < len(FIELD_TYPES):
                    if not self.strict:
                        continue
                    else:
                        raise ValueError('unknown type %d in tag 0x%04X' % (field_type, tag))
                typelen = FIELD_TYPES[field_type][0]
                count = self.s2n(entry + 4, 4)
                size = count * typelen#con esto nos evitamos la multiplicacion
                if(self.detecErr and tag_entry and len(tag_entry) > 1):
                    '''Si sabemos que un campo tiene datos de tipo y longitud prefijados lo comprobamos, 
                    si no lo tenemos, no comprobamos nada tanto en caso de no estar en la lista como de no tener esos datos
                    '''
                    if tag_entry[1] != field_type and tag_entry[1] != 11 and tag_entry[1] != 7:#Casos especiales, tipo doble "11" y tipo "undefined" 
                        if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                        self.errors[ifd_name][tag_name] = [(1, tag_entry[1], int(field_type),str(FIELD_TYPES[tag_entry[1]][2]),str(FIELD_TYPES[field_type][2]))]##Salida error
                        if self.debug : 
                            print " error:   Tag " + tag_name + " Tipo no coincide, esperado: " + str(FIELD_TYPES[tag_entry[1]][2]) + " dado: " + str(FIELD_TYPES[field_type][2])
                            
                    elif tag_entry[1] == 11:
                        if field_type != 3 and field_type != 4:
                            if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                            self.errors[ifd_name][tag_name] = [(1, 11, int(field_type),"Short o Long",str(field_type))]
                            if self.debug : 
                                print " error:   Tag " + tag_name + " Tipo no coincide, esperado: Short o Long dado: " + str(field_type)
                                
                    if tag_entry[2] != count and tag_entry[2] != 0 and not(type(tag_entry[2]) is list and count in tag_entry[2]):
                        if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                        if not self.errors[ifd_name].has_key(tag_name):
                            self.errors[ifd_name][tag_name] = []
                        self.errors[ifd_name][tag_name].append((2, tag_entry[2], int(count),str(tag_entry[2]),str(count)))
                        if self.debug : 
                            print " error:   Tag " + tag_name + " Numero de elementos diferentes, esperado: " + str(tag_entry[2]) + " dado: " + str(count)  
                        
                        #Si esperamos un numero de bytes >4 y tenemos el caso contrario, tenemos un valor doble
                        #ahora los valores son listas
                        pp=self.s2n(entry + 8, 4) 
                        py=FIELD_TYPES[tag_entry[1]][0]
                        print self.file.__sizeof__()
                        
                        if (count * typelen <= 4 and FIELD_TYPES[tag_entry[1]][0] * tag_entry[2] > 4 and self.s2n(entry + 8, 4) > self.file.__sizeof__()):#Precalculamos el offset
                            doubleValue = True
                            count = [count, tag_entry[2]]
                            field_type = [field_type, tag_entry[1]]
                            typelen = [typelen, FIELD_TYPES[tag_entry[1]][0]]
                            size = [field_type[0] * typelen[0], field_type[1] * typelen[1]]
                    
                # Adjust for tag id/type/count (2+2+4 bytes)
                # Now we point at either the data or the 2nd level offset
                if doubleValue: offset = [entry + 8]#adaptado para valor 
                else: offset = entry + 8

                # If the value fits in 4 bytes, it is inlined, else we
                # need to jump ahead again.
                if doubleValue or count * typelen > 4 :#cambiado para coger el valor doble
                    # offset is not the value; it's a pointer to the value
                    # if relative we set things up so s2n will seek to the right
                    # place when it adds self.offset.  Note that this 'relative'
                    # is for the Nikon type 3 makernote.  Other cameras may use
                    # other relative offsets, which would have to be computed here
                    # slightly differently.
                    if relative:
                        tmp_offset = self.s2n(offset, 4)
                        offset = tmp_offset + ifd - 8
                        if self.fake_exif:
                            offset = offset + 18
                    else:
                        if doubleValue : offset.append(self.s2n(offset[0], 4))
                        else: offset = self.s2n(offset, 4)
                if doubleValue: field_offset = offset[0]
                else: field_offset = offset    
                
                if not doubleValue and field_type == 2:#Si no es valor doble hacemos analisis normal
                    # special case: null-terminated ASCII string
                    # XXX investigate
                    # sometimes gets too big to fit in int value
                    
                    if count != 0 and count < (2 ** 31):
                        self.file.seek(self.offset + offset)
                        values = self.file.read(count)
                        #-------------------
                        values = values.replace("\x00", "\x3B")
                        if (values and values[-1:] == "\x3B"):#Si hemos cambiado el ultimo restauramos
                            values = values[0:-1]
                        
                        elif(self.detecErr and tag_entry and len(tag_entry) > 1 and tag_entry[1] != 7):#Si no lo hemos cambiado significa que no acaba en nulo -> error, si es "undefined" en la especificacion no tiene porque acabar en nulo aun siendo ascii
                            if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                            if not self.errors[ifd_name].has_key(tag_name):
                                self.errors[ifd_name][tag_name] = []
                            self.errors[ifd_name][tag_name].append((0, None, None,"None","None"))
                            if self.debug : 
                                print " error:   Tag " + tag_name + " con tipo ASCII, no acaba en caracter nulo"
                                
                        if(self.detecErr and tag in (0x0132, 0x9003, 0x9004, 0x001D)):#formato de fecha erroneo, YYYY:MM:DD, tags con fecha
                            if(tag == 0x001D):
                                if not re.match("(([1-2][0-9][0-9][0-9]):([0-1][0-9]):([0-3][0-9]))|    :  :  ", values):
                                    if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                                    if not self.errors[ifd_name].has_key(tag_name):
                                        self.errors[ifd_name][tag_name] = []
                                    self.errors[ifd_name][tag_name].append((5, None, None,"None","None"))
                                    if self.debug : 
                                        print " error en el formato de la fecha"                                   
                                        
                            elif not re.match("(([1-2][0-9][0-9][0-9]):([0-1][0-9]):([0-3][0-9]) ([0-2][0-9]):([0-5][0-9]):([0-5][0-9]))|    :  :     :  :  ", values):
                                if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                                if not self.errors[ifd_name].has_key(tag_name):
                                    self.errors[ifd_name][tag_name] = []
                                self.errors[ifd_name][tag_name].append((5, None, None,"None","None"))
                                if self.debug : 
                                    print " error en el formato de la fecha y hora"
                                                                   
                        #-------
                    else:
                        values = ''
                elif(not doubleValue):#Si no es valor doble 
                    values = []
                    signed = (field_type in [6, 8, 9, 10])
                    
                    # XXX investigate
                    # some entries get too big to handle could be malformed
                    # file or problem with self.s2n
                    if count < 1000:
                        for dummy in range(count):
                            if field_type in (5, 10):
                                # a ratio
                                value = Ratio(self.s2n(offset, 4, signed),
                                              self.s2n(offset + 4, 4, signed))
                            else:
                                value = self.s2n(offset, typelen, signed)
                            values.append(value)
                            offset = offset + typelen
                    # The test above causes problems with tags that are 
                    # supposed to have long values!  Fix up one important case.
                    elif tag_name == 'MakerNote' :
                        for dummy in range(count):
                            value = self.s2n(offset, typelen, signed)
                            values.append(value)
                            offset = offset + typelen
                    #else :
                    #    print "Warning: dropping large tag:", tag, tag_name
                elif(doubleValue):#Caso valor doble
                    valuesDouble = []
                    values = []
                    for i in (0, 1):
                        signed = (field_type[i] in [6, 8, 9, 10])
                    
                        # XXX investigate
                        # some entries get too big to handle could be malformed
                        # file or problem with self.s2n
                        if count[i] < 1000:
                            for dummy in range(count[i]):
                                if field_type[i] in (5, 10):
                                    # a ratio
                                    value = Ratio(self.s2n(offset[i], 4, signed),
                                              self.s2n(offset[i] + 4, 4, signed))
                                else:
                                    value = self.s2n(offset[i], typelen[i], signed)
                                values.append(value)
                                offset[i] = offset[i] + typelen[i]
                            valuesDouble.append(values)
                            values = []
                            
                    field_type = field_type[0]
                    values = valuesDouble
                # now 'values' is either a string or an array
                if not doubleValue and count == 1 and field_type != 2:
                    printable = str(values[0])
                elif not doubleValue and count > 50 and len(values) > 20 : 
                    #printable=str( values[0:20] )[0:-1] + ", ... ]"
                    printable = str(values)[0:-1] + "]" #David Arenas
                else:
                    printable = str(values)

                # compute printable version of values
                if not doubleValue and tag_entry:
                    if len(tag_entry) > 3:
                        # optional 2nd tag element is present
                        if callable(tag_entry[3]):
                            # call mapping function
                            printable = tag_entry[3](values)
                        else:
                            printable = ''
                            for i in values:
                                # use lookup table for this tag
                                printable += tag_entry[3].get(i, repr(i))
                                
                if (not self.tags.has_key(ifd_name)):self.tags[ifd_name] = {}#diccionario de diccionarios
                #Control repetidos
                if(self.tags[ifd_name].has_key(tag_name)):#Control repetidos
                    if self.debug:
                        print " error tag " + str(tag_name) + " repetido"                    
                                          
                    if (not self.errors.has_key(ifd_name)):self.errors[ifd_name] = {}#diccionario de diccionarios
                    if not self.errors[ifd_name].has_key(tag_name):
                        self.errors[ifd_name][tag_name] = []
                    self.errors[ifd_name][tag_name].append((4, None, None,"None","None"))
                    
                self.tags[ifd_name][tag_name] = IFD_Tag(printable, tag,
                                                          field_type,
                                                          values, field_offset,
                                                          size)
                
                if self.debug:
                    print ' debug:   %s: %s' % (tag_name,
                                                repr(self.tags[ifd_name][tag_name]))
            if tag_name == stop_tag:
                break
            
    def extract_TIFF_thumbnail(self, thumb_ifd):
        """
        \brief Extract uncompressed TIFF thumbnail (like pulling teeth).
        We take advantage of the pre-existing layout in the thumbnail IFD as much as possible.
        \param self (EXIF::EXIF_header).
        \param thumb_ifd (int) Thumbnail IFD.
        \return No return.
        """
        entries = self.s2n(thumb_ifd, 2)
        # this is header plus offset to IFD ...
        if self.endian == 'M':
            tiff = 'MM\x00*\x00\x00\x00\x08'
        else:
            tiff = 'II*\x00\x08\x00\x00\x00'
        # ... plus thumbnail IFD data plus a null "next IFD" pointer
        self.file.seek(self.offset + thumb_ifd)
        tiff += self.file.read(entries * 12 + 2) + '\x00\x00\x00\x00'

        # fix up large value offset pointers into data area
        for i in range(entries):
            entry = thumb_ifd + 2 + 12 * i
            tag = self.s2n(entry, 2)
            field_type = self.s2n(entry + 2, 2)
            typelen = FIELD_TYPES[field_type][0]
            count = self.s2n(entry + 4, 4)
            oldoff = self.s2n(entry + 8, 4)
            # start of the 4-byte pointer area in entry
            ptr = i * 12 + 18
            # remember strip offsets location
            if tag == 0x0111:
                strip_off = ptr
                strip_len = count * typelen
            # is it in the data area?
            if count * typelen > 4:
                # update offset pointer (nasty "strings are immutable" crap)
                # should be able to say "tiff[ptr:ptr+4]=newoff"
                newoff = len(tiff)
                tiff = tiff[:ptr] + self.n2s(newoff, 4) + tiff[ptr + 4:]
                # remember strip offsets location
                if tag == 0x0111:
                    strip_off = newoff
                    strip_len = 4
                # get original data and store it
                self.file.seek(self.offset + oldoff)
                tiff += self.file.read(count * typelen)

        # add pixel strips and update strip offset info
        old_offsets = self.tags['Thumbnail']['StripOffsets'].values
        old_counts = self.tags['Thumbnail']['StripByteCounts'].values
        for i in range(len(old_offsets)):
            # update offset pointer (more nasty "strings are immutable" crap)
            offset = self.n2s(len(tiff), strip_len)
            tiff = tiff[:strip_off] + offset + tiff[strip_off + strip_len:]
            strip_off += strip_len
            # add pixel strip to end
            self.file.seek(self.offset + old_offsets[i])
            tiff += self.file.read(old_counts[i])

        self.tags['TIFFThumbnail'] = tiff

    def decode_maker_note(self):
        """
        \brief Decode all the camera-specific MakerNote formats.
        Note is the data that comprises this MakerNote.  The MakerNote will
        likely have pointers in it that point to other parts of the file.  We'll
        use self.offset as the starting point for most of those pointers, since
        they are relative to the beginning of the file.
        
        If the MakerNote is in a newer format, it may use relative addressing
        within the MakerNote.  In that case we'll use relative addresses for the
        pointers.
        
        As an aside: it's not just to be annoying that the manufacturers use
        relative offsets.  It's so that if the makernote has to be moved by the
        picture software all of the offsets don't have to be adjusted.  Overall,
        this is probably the right strategy for makernotes, though the spec is
        ambiguous.  (The spec does not appear to imagine that makernotes would
        follow EXIF format internally.  Once they did, it's ambiguous whether
        the offsets should be from the header at the start of all the EXIF info,
        or from the header at the start of the makernote.)
        \param self (EXIF::EXIF_header).
        \return No return.
        """
        note = self.tags['EXIF']['MakerNote']
        
        # Some apps use MakerNote tags but do not use a format for which we
        # have a description, so just do a raw dump for these.
        #if self.tags.has_key('Image Make'):
        make = self.tags['Image']['Make'].printable

# 
def process_file(f, stop_tag='UNDEF', details=True, strict=False, debug=False, detecErr=False):
    """
    \brief To use this library call with:
    \brief    f = open(path_name, 'rb')
    \brief   tags = EXIF.process_file(f)
    
    \brief To ignore MakerNote tags: tags = EXIF.process_file(f, details=False)
    \brief To stop processing after a certain tag is retrieved: tags = EXIF.process_file(f, stop_tag='TAG')
     where TAG is a valid tag name, ex 'DateTimeOriginal'.
    \brief These 2 are useful when you are retrieving a large list of images
    \brief To return an error on invalid tags: tags = EXIF.process_file(f, strict=True). Otherwise these tags will be ignored
    
    \param f (str) Filename to process (must include the full path).
    \param stop_tag (str) To stop processing after a certain tag (default 'UNDEF').
    \param details (bool) False to ignore MakerNote tag and True in other case (default False).
    \param strict (bool) True to return an error on invalid tags, False in other case (default False).
    \param debug (bool) Debug.
    \return (dictionary) Returned tags will be a dictionary mapping names of EXIF tags to their
    values in the file named by path_name.  You can process the tags as you wish.  In particular, you can iterate through all the tags with:
    The tags dictionary will include keys for all of the usual EXIF tags, and will also include keys for Makernotes used by some
    cameras, for which we have a good specification. Note that the dictionary keys are the IFD name followed by the
    tag name. For example: 'EXIF DateTimeOriginal', 'Image Orientation', 'MakerNote FocusMode'of the EXIF standard
    """
    ## False to ignore MakerNote tag and True in other case. 
    global detailed
    detailed = details

    # by default do not fake an EXIF beginning
    fake_exif = 0

    # determine whether it's a JPEG or TIFF
    data = f.read(12)
    if data[0:4] in ['II*\x00', 'MM\x00*']:
        # it's a TIFF file
        f.seek(0)
        endian = f.read(1)
        f.read(1)
        offset = 0
    elif data[0:2] == '\xFF\xD8':
        # it's a JPEG file
        while data[2] == '\xFF' and data[6:10] in ('JFIF', 'JFXX', 'OLYM', 'Phot'):
            length = ord(data[4]) * 256 + ord(data[5])
            f.read(length - 8)
            # fake an EXIF beginning of file
            data = '\xFF\x00' + f.read(10)
            fake_exif = 1
        if data[2] == '\xFF' and data[6:10] == 'Exif':
            # detected EXIF header
            offset = f.tell()
            endian = f.read(1)
        else:
            # no EXIF information
            
            return [{}, {"EXIF":{"EXIF":[(8, 0, data[6:10])]}}]
    else:
        # file format not recognized
        return [{}, {"EXIF":{"EXIF":[(8, 1, None)]}}]

    # deal with the EXIF info we found
    if debug:
        print {'I': 'Intel', 'M': 'Motorola'}[endian], 'format'
    hdr = EXIF_header(f, endian, offset, fake_exif, strict, detecErr , debug)
    ifd_list = hdr.list_IFDs()
    ctr = 0
    for i in ifd_list:
        if ctr == 0:
            IFD_name = 'Image'
        elif ctr == 1:
            IFD_name = 'Thumbnail'
            thumb_ifd = i
        else:
            IFD_name = 'IFD %d' % ctr
        if debug:
            print ' IFD %d (%s) at offset %d:' % (ctr, IFD_name, i)
        hdr.dump_IFD(i, IFD_name, stop_tag=stop_tag)
        # EXIF IFD
        exif_off = hdr.tags.get(IFD_name) and hdr.tags[IFD_name].get('ExifOffset')
        if exif_off:
            if debug:
                print ' EXIF SubIFD at offset %d:' % exif_off.values[0]
            hdr.dump_IFD(exif_off.values[0], 'EXIF', stop_tag=stop_tag)
            # Interoperability IFD contained in EXIF IFD
            intr_off = hdr.tags.get('EXIF') and hdr.tags['EXIF'].get('InteroperabilityOffset')
            if intr_off:
                if debug:
                    print ' EXIF Interoperability SubSubIFD at offset %d:' \
                          % intr_off.values[0]
                hdr.dump_IFD(intr_off.values[0], 'EXIF Interoperability',dict=INTR_TAGS, stop_tag=stop_tag)
        # GPS IFD
        gps_off = hdr.tags.get(IFD_name) and hdr.tags[IFD_name].get('GPSInfo')
        if gps_off:
            if debug:
                print ' GPS SubIFD at offset %d:' % gps_off.values[0]
            hdr.dump_IFD(gps_off.values[0], 'GPS', dict=GPS_TAGS, stop_tag=stop_tag)
            #Buscamos los errores en el GPS
            if(not hdr.tags.get("GPS") or len(hdr.tags.get("GPS")) <= 0):#Sera cierto si tenemos el tag GPSInfo pero nada de informacion GPS
                hdr.errors["GPS"] = {}
                hdr.errors["GPS"]["GPSVersionID"] = [(9, 0, None,str(list(FIELD_TYPES[0])[2]),"None")]                  
                hdr.errors["GPS"]["GPSLatitude"] = [(9, 1, None,str(list(FIELD_TYPES[1])[2]),"None")]               
                hdr.errors["GPS"]["GPSLongitude"] = [(9, 1, None,str(list(FIELD_TYPES[1])[2]),"None")]
                
            else:
                if(not hdr.tags["GPS"].get("GPSVersionID")):
                    if(not hdr.errors.get("GPS")):
                        hdr.errors["GPS"] = {}
                    hdr.errors["GPS"]["GPSVersionID"] = [(9, 0, None,str(list(FIELD_TYPES[0])[2]),"None")]
                if(not hdr.tags["GPS"].get("GPSLatitude")):
                    if(not hdr.errors.get("GPS")):
                        hdr.errors["GPS"] = {}
                    hdr.errors["GPS"]["GPSLatitude"] = [(9, 1, None,str(list(FIELD_TYPES[1])[2]),"None")] 
                else:
                    val = hdr.tags["GPS"]["GPSLatitude"].values
                    if(val[0].num == 0 and val[0].den == 1 and val[1].num == 0 and val[1].den == 1 and val[2].num == 0 and val[2].den == 1):
                        if(not hdr.errors.get("GPS")):
                            hdr.errors["GPS"] = {}
                        if(not hdr.errors["GPS"].get("GPSLatitude")):
                            hdr.errors["GPS"]["GPSLatitude"] = []
                        hdr.errors["GPS"]["GPSLatitude"].append((9, 2, None,str(list(FIELD_TYPES[2])[2]),"None"))
                    
                if(not hdr.tags["GPS"].get("GPSLongitude")):
                    if(not hdr.errors.get("GPS")):
                        hdr.errors["GPS"] = {}
                    hdr.errors["GPS"]["GPSLongitude"] = [(9, 1, None,str(list(FIELD_TYPES[1])[2]),"None")]
                    
                else:
                    val = hdr.tags["GPS"]["GPSLongitude"].values
                    if(val[0].num == 0 and val[0].den == 1 and val[1].num == 0 and val[1].den == 1 and val[2].num == 0 and val[2].den == 1):
                        if(not hdr.errors.get("GPS")):
                            hdr.errors["GPS"] = {}
                        if(not hdr.errors["GPS"].get("GPSLongitude")):
                            hdr.errors["GPS"]["GPSLongitude"] = []
                        hdr.errors["GPS"]["GPSLongitude"].append((9, 2, None,str(list(FIELD_TYPES[2])[2]),"None")) 
        ctr += 1

    # extract uncompressed TIFF thumbnail
    thumb = hdr.tags.get('Thumbnail') and hdr.tags.get('Thumbnail').get('Compression')
    if thumb and thumb.printable == 'Uncompressed TIFF':
        hdr.extract_TIFF_thumbnail(thumb_ifd)

    # JPEG thumbnail (thankfully the JPEG data is stored as a unit)
    thumb_off = hdr.tags.get('Thumbnail') and hdr.tags['Thumbnail'].get('JPEGInterchangeFormat')
    if thumb_off:
        f.seek(offset + thumb_off.values[0])
        size = hdr.tags['Thumbnail']['JPEGInterchangeFormatLength'].values[0]
        hdr.tags['JPEGThumbnail'] = f.read(size)

    # deal with MakerNote contained in EXIF IFD
    # (Some apps use MakerNote tags but do not use a format for which we
    # have a description, do not process these).
    if 'EXIF' in hdr.tags and 'MakerNote' in hdr.tags['EXIF'] and 'Image' in hdr.tags and 'Make' in hdr.tags['Image'] and detailed:
        hdr.decode_maker_note()

    # Sometimes in a TIFF file, a JPEG thumbnail is hidden in the MakerNote
    # since it's not allowed in a uncompressed TIFF IFD
    if 'JPEGThumbnail' not in hdr.tags:
        thumb_off = hdr.tags.get('MakerNote') and hdr.tags['MakerNote'].get('JPEGThumbnail')
        if thumb_off:
            f.seek(offset + thumb_off.values[0])
            hdr.tags['JPEGThumbnail'] = file.read(thumb_off.field_length)
            if(detecErr):
                hdr.errors["IFD1"] = {"Thumbnail":[(3, 1, None,str(list(FIELD_TYPES[1])[2]),"None")]}
                if debug:
                    print" error:   Thumbnail encontrado en Maker Notes"                                           
                print "Thumbnail encontrado en Maker Notes"
        #####Nuevo control thumbnail
        elif(detecErr):
            hdr.errors["IFD1"] = {"Thumbnail":[(3, 0, None,str(list(FIELD_TYPES[0])[2]),"None")]}
            if debug:
                print" error:   No se encontro Thumbnail"                      
            
    #Control postprocesado para tags fijos      
    #Reconocemos el tipo de jpeg y le asignamos las listas de tags correspondientes
    imageTagList = []
    thumbnailTagList = []
    notImageTagList = []
    notInteroperabilityTagList = []
    notThumbnailTagList = []
    
    if hdr.tags.get("Image") and hdr.tags.get("Image").get(EXIF_TAGS[0x106][0]):     
        type = hdr.tags.get("Image").get(EXIF_TAGS[0x106][0]).values[0]
        
        if (type == 6):#2 RGB 6 YCrCb         
            imageTagList = list(TagYCCImage)
            thumbnailTagList = list(TagYCCThumbnail)
            notImageTagList = notTagYCCImage
            notInteroperabilityTagList = notTagYCCInteroperability
            notThumbnailTagList = notTagYCCThumbnail   
        elif (type == 2):
            if hdr.tags.get("Image") and hdr.tags.get("Image").get(EXIF_TAGS[0x11C][0]) and hdr.tags.get("Image").get(EXIF_TAGS[0x11C][0]).values[0] == 2:#1 chunky 2 plannar
                imageTagList = list(TagPlImage)
                thumbnailTagList = list(TagPlThumbnail)
                notImageTagList = notTagPlImage
                notInteroperabilityTagList = notTagPlInteroperability
                notThumbnailTagList = notTagPlThumbnail
            else:#chunky
                imageTagList = list(TagChImage)
                thumbnailTagList = list(TagChThumbnail)
                notImageTagList = notTagChImage
                notInteroperabilityTagList = notTagChInteroperability
                notThumbnailTagList = notTagChThumbnail                                                                                                       
        else:
            print "error valor de 0x106 incorrecto"                        
    else:#compressed
        imageTagList = list(TagCompressedImage)
        thumbnailTagList = list(TagCompressedThumbnail)
        notImageTagList = notTagCompressedImage
        notInteroperabilityTagList = []
        notThumbnailTagList = notTagCompressedThumbnail
        
    #Control de tags    
    if(hdr.tags.get("Image") and hdr.tags.get("EXIF")):
        imageTags = hdr.tags.get("Image").keys()
        imageTags.extend(hdr.tags.get("EXIF").keys())
        #print imageTags
        #print imageTagList
        for i in imageTags:
            try:
                imageTagList.remove(i)
            except:
                pass
            if(notImageTagList.count(i) > 0):
                if (not hdr.errors.has_key("EXIF")):hdr.errors["EXIF"] = {}#diccionario de diccionarios
                if not hdr.errors["EXIF"].has_key(i):
                    hdr.errors["EXIF"][i] = []
                hdr.errors["EXIF"][i].append((7, None, None,"None","None"))
        for i in imageTagList:# Si no esta vacia es que faltan tags
            if (not hdr.errors.has_key("EXIF")):hdr.errors["EXIF"] = {}#diccionario de diccionarios
            if not hdr.errors["EXIF"].has_key(i):
                hdr.errors["EXIF"][i] = []
            hdr.errors["EXIF"][i].append((6, None, None,"None","None"))                         
    if(hdr.tags.get("Thumbnail")):
        thumbnailTags = hdr.tags.get("Thumbnail").keys()
        for i in thumbnailTags:
            try:
                thumbnailTagList.remove(i)
            except:
                pass
            if(notThumbnailTagList.count(i) > 0):
                if (not hdr.errors.has_key("Thumbnail")):hdr.errors["Thumbnail"] = {}#diccionario de diccionarios
                if not hdr.errors["Thumbnail"].has_key(i):
                    hdr.errors["Thumbnail"][i] = []
                hdr.errors["Thumbnail"][i].append((7, None, None,"None","None"))
        for i in thumbnailTagList:# Si no esta vacia es que faltan tags
            if (not hdr.errors.has_key("Thumbnail")):hdr.errors["Thumbnail"] = {}#diccionario de diccionarios
            if not hdr.errors["Thumbnail"].has_key(i):
                hdr.errors["Thumbnail"][i] = []
            hdr.errors["Thumbnail"][i].append((6, None, None,"None","None"))                                
    if(hdr.tags.get("EXIF Interoperability")):
        if (notInteroperabilityTagList != [] and hdr.tags.get("EXIF Interoperability").get('InteroperabilityIndex')):#No es del tipo compressed, no deberia tener nada
            hdr.errors["EXIF Interoperability"] = {'InteroperabilityIndex':[(7, None, None,"None","None")]}        
            
    if "IFD1" in hdr.errors:
        del hdr.errors["IFD1"]
    if "IFD2" in hdr.errors:
        del hdr.errors["IFD2"]
    if "IFD 3" in hdr.errors:
        del hdr.errors["IFD 3"]
    print hdr.tags
    print hdr.errors
    return [hdr.tags, hdr.errors]

def usage(exit_status):
    """
    \brief Show command line usage.
    \param exit_status (int) Exit status.
    \return No return.
    """
    msg = 'Usage: EXIF.py [OPTIONS] file1 [file2 ...]\n'
    msg += 'Extract EXIF information from digital camera image files.\n\nOptions:\n'
    msg += '-q --quick   Do not process MakerNotes.\n'
    msg += '-t TAG --stop-tag TAG   Stop processing when this tag is retrieved.\n'
    msg += '-s --strict   Run in strict mode (stop on errors).\n'
    msg += '-d --debug   Run in debug mode (display extra info).\n'
    print msg
    sys.exit(exit_status)


