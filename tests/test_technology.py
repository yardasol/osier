import pytest
import unyt
from unyt import kW, MW, hr, BTU, Horsepower, day
from osier import Technology
from osier.technology import _validate_unit, _validate_quantity
from unyt.exceptions import UnitParseError

TECH_NAME = "PlanetExpress"
energy_unyt = 10.0 * MW * hr
other_energy_unyt = 10.0 * BTU
spec_energy_unyt = 10.0 * (MW * hr)**-1
power_unyt = 10.0 * MW
spec_power_unyt = 10.0 * MW**-1
other_power_unyt = Horsepower
time_unyt = 1 * hr
float_val = 10.0
int_val = 10
str_val = "10"
energy_str = "10 MW*hr"
spec_energy_str = "10 (MW*hr)**-1"
power_str = "10 MW"
spec_power_str = "10 MW**-1"
time_str = "10 hr"
unknown_str = "10 fortnights"
dict_type = {"value": 10,
             "unit": MW}

@pytest.fixture
def advanced_tech():
    PLANET_EXPRESS = Technology(TECH_NAME)
    return PLANET_EXPRESS

def test_validate_unit():
    assert _validate_unit("MW", 'power').same_dimensions_as(Horsepower)
    assert _validate_unit("BTU", 'energy').same_dimensions_as(MW * hr)
    assert _validate_unit("day", 'time').same_dimensions_as(hr)
    assert _validate_unit(
        "Horsepower**-1",
        'spec_power').same_dimensions_as(
        MW**-1)
    assert _validate_unit(
        (Horsepower * day)**-1,
        'spec_energy').same_dimensions_as(
        (MW * hr)**-1)

    with pytest.raises(UnitParseError) as e:
        _validate_unit("darkmatter", "energy")

    with pytest.raises(KeyError) as e:
        _validate_unit("darkmatter", "fuel")


def test_validate_quantity():
    assert _validate_quantity(power_unyt, 'power') == 10 * (MW)
    assert _validate_quantity(energy_unyt, 'energy') == 10 * (MW * hr)
    assert _validate_quantity(time_unyt, 'time') == 1 * (hr)
    assert _validate_quantity("10 Horsepower**-1",
                              'spec_power') == 10 * (Horsepower**-1)
    assert _validate_quantity(10 * (Horsepower * day)**-1,
                              'spec_energy') == 10 * ((Horsepower * day)**-1)

    with pytest.raises(TypeError) as e:
        _validate_quantity(10 * MW, "energy")
    with pytest.raises(UnitParseError) as e:
        _validate_quantity("10 darkmatter", "energy")

    with pytest.raises(KeyError) as e:
        _validate_quantity("10 darkmatter", "fuel")


def test_initialize(advanced_tech):
    assert advanced_tech.technology_name == TECH_NAME
    assert advanced_tech.technology_type == 'base'
    assert advanced_tech.capacity == 0.0
    assert advanced_tech.capital_cost == 0.0
    assert advanced_tech.om_cost_fixed == 0.0
    assert advanced_tech.om_cost_variable == 0.0
    assert advanced_tech.fuel_cost == 0.0
    assert advanced_tech.unit_power == MW
    assert advanced_tech.unit_time == hr
    assert advanced_tech.unit_energy == MW * hr


def test_attribute_types(advanced_tech):
    assert isinstance(advanced_tech.capacity, unyt.array.unyt_quantity)
    assert isinstance(advanced_tech.capital_cost, unyt.array.unyt_quantity)
    assert isinstance(advanced_tech.om_cost_fixed, unyt.array.unyt_quantity)
    assert isinstance(advanced_tech.om_cost_variable, unyt.array.unyt_quantity)
    assert isinstance(advanced_tech.fuel_cost, unyt.array.unyt_quantity)
    assert isinstance(advanced_tech.unit_power, unyt.unit_object.Unit)
    assert isinstance(advanced_tech.unit_energy, unyt.unit_object.Unit)
    assert isinstance(advanced_tech.unit_time, unyt.unit_object.Unit)


def test_capacity(advanced_tech):
    with pytest.raises(ValueError) as e:
        advanced_tech.capacity = dict_type
    with pytest.raises(UnitParseError) as e:
        advanced_tech.capacity = unknown_str
    with pytest.raises(AssertionError) as e:
        advanced_tech.capacity = energy_str

    advanced_tech.capacity = power_unyt
    assert advanced_tech.capacity.value == 10.0
    assert advanced_tech.capacity.units == MW

    advanced_tech.capacity = power_str
    assert advanced_tech.capacity.value == 10.0
    assert advanced_tech.capacity.units == MW

    advanced_tech.capacity = int_val
    assert advanced_tech.capacity.value == 10
    assert advanced_tech.capacity.units == MW

    advanced_tech.capacity = str_val
    assert advanced_tech.capacity.value == 10.0
    assert advanced_tech.capacity.units == MW

    advanced_tech.capacity = float_val * other_power_unyt
    assert advanced_tech.capacity.value == pytest.approx(0.007457, 0.005)
    assert advanced_tech.capacity.units == MW

    advanced_tech.unit_power = "kW"
    assert advanced_tech.capacity.units == kW


def test_capital_cost(advanced_tech):
    with pytest.raises(ValueError) as e:
        advanced_tech.capital_cost = dict_type
    with pytest.raises(UnitParseError) as e:
        advanced_tech.capital_cost = unknown_str
    with pytest.raises(AssertionError) as e:
        advanced_tech.capital_cost = energy_str

    advanced_tech.capital_cost = spec_power_unyt
    assert advanced_tech.capital_cost.value == 10.0
    assert advanced_tech.capital_cost.units == MW**-1

    advanced_tech.capital_cost = spec_power_str
    assert advanced_tech.capital_cost.value == 10.0
    assert advanced_tech.capital_cost.units == MW**-1

    advanced_tech.capital_cost = int_val
    assert advanced_tech.capital_cost.value == 10
    assert advanced_tech.capital_cost.units == MW**-1

    advanced_tech.capital_cost = str_val
    assert advanced_tech.capital_cost.value == 10.0
    assert advanced_tech.capital_cost.units == MW**-1

    advanced_tech.capital_cost = float_val / other_power_unyt
    assert advanced_tech.capital_cost.value == pytest.approx(13410.220, 0.005)
    assert advanced_tech.capital_cost.units == MW**-1

    advanced_tech.unit_power = "kW"
    assert advanced_tech.capital_cost.units == (kW)**-1


def test_om_cost_fixed(advanced_tech):
    with pytest.raises(ValueError) as e:
        advanced_tech.om_cost_fixed = dict_type
    with pytest.raises(UnitParseError) as e:
        advanced_tech.om_cost_fixed = unknown_str
    with pytest.raises(AssertionError) as e:
        advanced_tech.om_cost_fixed = energy_str

    advanced_tech.om_cost_fixed = spec_power_unyt
    assert advanced_tech.om_cost_fixed.value == 10.0
    assert advanced_tech.om_cost_fixed.units == MW**-1

    advanced_tech.om_cost_fixed = spec_power_str
    assert advanced_tech.om_cost_fixed.value == 10.0
    assert advanced_tech.om_cost_fixed.units == MW**-1

    advanced_tech.om_cost_fixed = int_val
    assert advanced_tech.om_cost_fixed.value == 10
    assert advanced_tech.om_cost_fixed.units == MW**-1

    advanced_tech.om_cost_fixed = str_val
    assert advanced_tech.om_cost_fixed.value == 10.0
    assert advanced_tech.om_cost_fixed.units == MW**-1

    advanced_tech.om_cost_fixed = float_val / other_power_unyt
    assert advanced_tech.om_cost_fixed.value == pytest.approx(13410.220, 0.005)
    assert advanced_tech.om_cost_fixed.units == MW**-1

    advanced_tech.unit_power = "kW"
    assert advanced_tech.om_cost_fixed.units == (kW)**-1


def test_om_cost_variable(advanced_tech):
    with pytest.raises(ValueError) as e:
        advanced_tech.om_cost_variable = dict_type
    with pytest.raises(UnitParseError) as e:
        advanced_tech.om_cost_variable = unknown_str
    with pytest.raises(AssertionError) as e:
        advanced_tech.om_cost_variable = power_str
    with pytest.raises(ValueError) as e:
        advanced_tech.om_cost_variable = spec_energy_str
    # assert advanced_tech.om_cost_variable.value == 10.0
    # assert advanced_tech.om_cost_variable.units == (MW*hr)**-1

    advanced_tech.om_cost_variable = spec_energy_unyt
    assert advanced_tech.om_cost_variable.value == 10.0
    assert advanced_tech.om_cost_variable.units == (MW * hr)**-1

    advanced_tech.om_cost_variable = int_val
    assert advanced_tech.om_cost_variable.value == 10
    assert advanced_tech.om_cost_variable.units == (MW * hr)**-1

    advanced_tech.om_cost_variable = str_val
    assert advanced_tech.om_cost_variable.value == 10.0
    assert advanced_tech.om_cost_variable.units == (MW * hr)**-1

    advanced_tech.om_cost_variable = float_val / other_energy_unyt
    assert advanced_tech.om_cost_variable.value == pytest.approx(
        3412141.5, 0.5)
    assert advanced_tech.om_cost_variable.units == (MW * hr)**-1

    advanced_tech.unit_power = "kW"
    advanced_tech.unit_time = "day"
    assert advanced_tech.om_cost_variable.units == (kW*day)**-1


def test_fuel_cost(advanced_tech):
    with pytest.raises(ValueError) as e:
        advanced_tech.fuel_cost = dict_type
    with pytest.raises(UnitParseError) as e:
        advanced_tech.fuel_cost = unknown_str
    with pytest.raises(AssertionError) as e:
        advanced_tech.fuel_cost = power_str
    with pytest.raises(ValueError) as e:
        advanced_tech.fuel_cost = spec_energy_str

    advanced_tech.fuel_cost = spec_energy_unyt
    assert advanced_tech.fuel_cost.value == 10.0
    assert advanced_tech.fuel_cost.units == (MW * hr)**-1

    advanced_tech.fuel_cost = int_val
    assert advanced_tech.fuel_cost.value == 10
    assert advanced_tech.fuel_cost.units == (MW * hr)**-1

    advanced_tech.fuel_cost = str_val
    assert advanced_tech.fuel_cost.value == 10.0
    assert advanced_tech.fuel_cost.units == (MW * hr)**-1

    advanced_tech.fuel_cost = float_val / other_energy_unyt
    assert advanced_tech.fuel_cost.value == pytest.approx(
        3412141.47989694, 0.5)
    assert advanced_tech.fuel_cost.units == (MW * hr)**-1
    
    advanced_tech.unit_power = "kW"
    advanced_tech.unit_time = "day"
    assert advanced_tech.fuel_cost.units == (kW*day)**-1


def test_unit_power(advanced_tech):
    with pytest.raises(UnitParseError) as e:
        advanced_tech.unit_power = "darkmatter"
    with pytest.raises(AssertionError) as e:
        advanced_tech.unit_power = BTU
    with pytest.raises(AssertionError) as e:
        advanced_tech.unit_power = "BTU"
    with pytest.raises(ValueError) as e:
        advanced_tech.unit_power = 10
    advanced_tech.unit_power = Horsepower
    assert advanced_tech.unit_power == Horsepower

    advanced_tech.unit_power = "Horsepower"
    assert advanced_tech.unit_power == Horsepower


def test_unit_time(advanced_tech):
    with pytest.raises(UnitParseError) as e:
        advanced_tech.unit_time = "darkmatter"
    with pytest.raises(AssertionError) as e:
        advanced_tech.unit_time = MW
    with pytest.raises(AssertionError) as e:
        advanced_tech.unit_time = "MW"
    with pytest.raises(ValueError) as e:
        advanced_tech.unit_time = 10
    advanced_tech.unit_time = day
    assert advanced_tech.unit_time == day

    advanced_tech.unit_time = "day"
    assert advanced_tech.unit_time == day


def test_unit_energy(advanced_tech):
    advanced_tech.unit_energy = "darkmatter"
    assert advanced_tech.unit_energy == MW*hr
    advanced_tech.unit_energy = BTU
    assert advanced_tech.unit_energy == MW*hr
    advanced_tech.unit_energy = "MW"
    assert advanced_tech.unit_energy == MW*hr
    advanced_tech.unit_energy = 10
    assert advanced_tech.unit_energy == MW*hr
    advanced_tech.unit_energy = Horsepower * day
    assert advanced_tech.unit_energy == MW*hr
    advanced_tech.unit_energy = "Horsepower*day"
    assert advanced_tech.unit_energy == MW*hr
