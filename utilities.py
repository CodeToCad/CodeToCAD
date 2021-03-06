# utilities.py contains enums and helper functions for CodeToCAD python functionality.

from enum import Enum
import re
import math

class Point:
    x:float
    y:float
    z:float

class BoundaryAxis:
    min = None
    max = None
    center = None
    range = None
    def __init__(self, min=None, max=None, center=None, range=None):
        self.min = min
        self.max = max
        self.center = center
        self.range = range


class BoundaryBox:
    x = BoundaryAxis()
    y = BoundaryAxis()
    z = BoundaryAxis()
    def __init__(self, x:BoundaryAxis=BoundaryAxis(), y:BoundaryAxis=BoundaryAxis(), z:BoundaryAxis=BoundaryAxis()):
        self.x = x
        self.y = y
        self.z = z

# An enum that uses the enum type and value for comparison
class EquittableEnum(Enum):
    # define the == operator, otherwise we can't compare enums, thanks python
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

class Units(EquittableEnum):
    pass


class AngleUnit(Units):
    RADIANS = 0
    DEGREES = 1

    def toDegrees(va):
        return math.degrees()

    def fromString(fromString:str):
        aliases = {
            "radians": AngleUnit.RADIANS,
            "rad": AngleUnit.RADIANS,
            "rads": AngleUnit.RADIANS,
            "r": AngleUnit.RADIANS,
            "degrees": AngleUnit.DEGREES,
            "degree": AngleUnit.DEGREES,
            "degs": AngleUnit.DEGREES,
            "deg": AngleUnit.DEGREES,
            "d": AngleUnit.DEGREES
        }
        return aliases[fromString.lower()]


class Angle():

  def toRadians(self):
      if self.unit == AngleUnit.DEGREES:
          self.value = math.radians(self.value)

      return self

  def toDegrees(self):
      if self.unit == AngleUnit.RADIANS:
          self.value = math.degrees(self.value)
          
      return self

  # Default unit is radians if unit not passed
  def __init__(self, value:float, unit:AngleUnit = AngleUnit.RADIANS):
      self.value = value
      self.unit = unit

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is radians if unit not passed
  def __init__(self, fromString:str, unit:AngleUnit = AngleUnit.RADIANS):

      fromString = str(fromString) # safe-guard if a non-string is passed in

      fromString = fromString.replace(" ", "")

      unitInString = re.search('[A-Za-z]+$', fromString)

      if unitInString:
          value = fromString[0:-1*len(unitInString[0])]

          self.unit = AngleUnit.fromString(unitInString[0])
      else:
          value = fromString

          self.unit = unit or AngleUnit.RADIANS
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d]+", value):
          self.value = eval(value)
      else:
          self.value = None

def getAnglesFromString(anglesString):
    
    if type(anglesString) == list:
        anglesString = ",".join(
            map(
                lambda angle:str(angle),
                anglesString
            )
        )

    parsedAngles = None
    if anglesString != None and type(anglesString) == str and "," in anglesString:
        anglesArray = anglesString.split(',')

        # besides accepting a unit in the angle, e.g. 1deg,1rad,1,rad. we also
        # accept the last input as a default unit
        # e.g. 1,1,1,rad => default value radians
        defaultUnit = re.search('[A-Za-z]+$', anglesArray[-1].strip())
        # check if the last value contains only a unit:
        if defaultUnit and len(defaultUnit[0]) == len(anglesArray[-1].strip()):
            defaultUnit = anglesArray.pop().strip()
        else:
            defaultUnit = None

        defaultUnit = AngleUnit.fromString(defaultUnit) if defaultUnit else None
        
        parsedAngles = [Angle(angle, defaultUnit) for angle in anglesArray ]
    elif anglesString != None and (type(anglesString) == str or type(anglesString) == int):
        parsedAngles = [Angle(anglesString)]
    else:
        print("getAnglesFromString: ", anglesString, " is not a valid input. Cannot parse angles.")

    return parsedAngles

class LengthUnit(Units):
    #metric
    micrometer = 1 / 1000
    millimeter = 1
    centimeter = 10
    meter = 1000
    kilometer = 1000000

    #imperial
    thousandthInch = 25.4 / 1000
    inch = 25.4
    foot = 25.4 * 12
    mile = 25.4 * 63360

    def fromString(fromString:str):
        aliases = {
            #metric
            "millimeter": LengthUnit.millimeter,
            "millimeters": LengthUnit.millimeter,
            "centimeter": LengthUnit.centimeter,
            "centimeters": LengthUnit.centimeter,
            "meter": LengthUnit.meter,
            "meters": LengthUnit.meter,
            "mm": LengthUnit.millimeter,
            "cm": LengthUnit.centimeter,
            "m": LengthUnit.meter,
            "km": LengthUnit.kilometer,
            #imperial
            "thousandthInch": LengthUnit.thousandthInch,
            "thousandth": LengthUnit.thousandthInch,
            "inch": LengthUnit.inch,
            "inches": LengthUnit.inch,
            "foot": LengthUnit.foot,
            "feet": LengthUnit.foot,
            "mile": LengthUnit.mile,
            "miles": LengthUnit.mile,
            "thou": LengthUnit.thousandthInch,
            "in": LengthUnit.inch,
            "ft": LengthUnit.foot,
            "mi": LengthUnit.mile
        }

        fromString = fromString.lower()

        return aliases[fromString] if fromString in aliases else None

    
    


class Dimension():

  # Default unit is None (scale factor) if it's not passed in
  def __init__(self, value:float, unit:LengthUnit = None):
      self.value = value
      self.unit = unit

  # fromString: takes a string with a math operation and an optional unit of measurement
  # Default unit is None (scale factor) if it's not passed in
  # examples: "1m", "1.5ft", "3/8in", "1", "1-(3/4)cm" 
  def __init__(self, fromString:str, unit:LengthUnit = None):

      fromString = str(fromString) # safe-guard if a non-string is passed in

      fromString = fromString.replace(" ", "")

      unitInString = re.search('[A-Za-z]+$', fromString)

      if unitInString:
          value = fromString[0:-1*len(unitInString[0])]

          self.unit = LengthUnit.fromString(unitInString[0])
      else:
          value = fromString

          self.unit = unit or None
      
      # Make sure our value only contains math operations and numbers as a weak safety check before passing it to `eval`
      if re.match("[+\-*\/%\d\(\)]+", value):
          self.value = eval(value)
      else:
          self.value = None

def convertToLengthUnit(targetUnit:LengthUnit, value, unit:LengthUnit) -> float:
    # LengthUnit enum has conversions based on the millimeter, so multiplying by the enum value will always yield millimeters
    return value * (unit.value/targetUnit.value)

def getDimensionsFromString(dimensions, boundingBox:BoundaryBox=None):

    # This is a tech debt, we need to separate the logic for figuring out default units from being dependent on the input being a string.
    if type(dimensions) == list or type(dimensions) == tuple:
        dimensions = ",".join(
            map(
                lambda dimension:str(dimension),
                dimensions
            )
        )

    parsedDimensions = None
    if dimensions != None and type(dimensions) == str and "," in dimensions:
        dimensionsArray = dimensions.split(',')

        # besides accepting a unit in the dimension, e.g. 1m,1cm,1,m. we also
        # accept the last input as a default unit
        # e.g. 1,1,1,m => default value meter
        lastDimension = dimensionsArray[-1].strip()
        defaultUnit = None
        if lastDimension not in ["min", "max", "center"]:
            defaultUnit = re.search('[A-Za-z]+$', lastDimension)
            # check if the last value contains only a unit:
            if defaultUnit and len(defaultUnit[0]) == len(lastDimension):
                defaultUnit = dimensionsArray.pop().strip()
            else:
                defaultUnit = None

        defaultUnit = LengthUnit.fromString(defaultUnit) if defaultUnit else None

        parsedDimensions = []

        for index, dimension in enumerate(dimensionsArray):
            dimension = dimension.lower()
            if boundingBox != None and index < 3:
                boundary = getattr(boundingBox, "xyz"[index])
                if "min" in dimension:
                    dimension = dimension.replace("min","({})".format( convertToLengthUnit(defaultUnit or LengthUnit.meter, boundary.min, LengthUnit.meter) ))
                if "max" in dimension:
                    dimension = dimension.replace("max","({})".format( convertToLengthUnit(defaultUnit or LengthUnit.meter, boundary.max, LengthUnit.meter) ))
                if "center" in dimension:
                    dimension = dimension.replace("center","({})".format( convertToLengthUnit(defaultUnit or LengthUnit.meter, boundary.center, LengthUnit.meter) ))

            parsedDimensions.append(Dimension(dimension, defaultUnit))

    elif dimensions != None and (type(dimensions) == str or type(dimensions) == int):
        parsedDimensions = [Dimension(dimensions)]
    else:
        print("getDimensionsFromString: ", dimensions, " is not a valid input. Cannot parse dimensions.")

    return parsedDimensions

class Axis(EquittableEnum):
    X = 0
    Y = 1
    Z = 2

class CurvePrimitiveTypes(EquittableEnum):
    Point = 0
    LineTo = 1
    Line = 2
    Angle = 3
    Circle = 4
    Ellipse = 5
    Sector = 6
    Segment = 7
    Rectangle = 8
    Rhomb = 9
    Trapezoid = 10
    Polygon = 11
    Polygon_ab = 12
    Arc = 13

class CurveTypes(EquittableEnum):
    POLY = 0
    NURBS = 1
    BEZIER = 2
    

class ScalingMethods(Enum):
    toSpecificLength=0
    scaleFactor=1
    lockAspectRatio=2 # scale one dimension, the others scale with it

class ConstraintTypes(EquittableEnum):
    Translation = 0 # Translation locked between specified start and end points in all axes.
    Rotation = 1 # Rotation locked between specified start and end angles in all axes.
    Pivot = 2 # Rotation locked between specified start and end angles in all axes, but rotation origin is offset.
    Gear = 3 # Rotation of one object is a percentage of another's in a specified axis.
