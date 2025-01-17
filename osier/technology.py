import unyt
from unyt import MW, hr
from unyt import unyt_quantity
from unyt.exceptions import UnitParseError, UnitConversionError


_dim_opts = {'time': hr,
             'power': MW,
             'energy': MW * hr,
             'spec_power': MW**-1,
             'spec_energy': (MW * hr)**-1}


def _validate_unit(value, dimension):
    """
    This function checks that a unit has the correct
    dimensions. Used in :class:`Technology` to set
    units.

    Parameters
    ----------
    value : string, float, int, or :class:`unyt.unit_object.Unit`
        The value being tested. Should be a unit symbol.
    dimension : string
        The expected dimensions of `value`.
        Currently accepts: ['time', 'energy', 'power', 'spec_power', 'spec_energy'].

    Returns
    -------
    valid_unit : :class:`unyt.unit_object.Unit`
        The validated unit.
    """
    try:
        exp_dim = _dim_opts[dimension]
    except KeyError:
        raise KeyError(f"Key <{dimension}> not accepted. Try: {_dim_opts}")

    valid_unit = None
    if isinstance(value, unyt.unit_object.Unit):
        assert value.same_dimensions_as(exp_dim)
        valid_unit = value
    elif isinstance(value, str):
        try:
            unit = unyt_quantity.from_string(value).units
            assert unit.same_dimensions_as(exp_dim)
            valid_unit = unit
        except UnitParseError:
            raise UnitParseError(f"Could not interpret <{value}>.")
        except AssertionError:
            raise AssertionError(f"{value} lacks units of {dimension}.")
    else:
        raise ValueError(f"Value of type <{type(value)}> passed.")

    return valid_unit


def _validate_quantity(value, dimension):
    """
    This function checks that a quantity has the correct
    dimensions. Used in :class:`Technology` to set
    data attributess.

    Parameters
    ----------
    value : string, float, int, or :class:`unyt.unyt_quantity`
        The value being tested. Should be something like
    
        >>> _validate_quantity("10 MW", dimension='power')
        unyt_quantity(10., 'MW')
        
    dimension : string
        The expected dimensions of `value`.
        Currently accepts: ['time', 'energy', 'power', 'spec_power', 'spec_energy'].

    Returns
    -------
    valid_quantity : :class:`unyt.unyt_quantity`
        The validated quantity.
    """
    try:
        exp_dim = _dim_opts[dimension]
    except KeyError:
        raise KeyError(f"Key <{dimension}> not accepted. Try: {_dim_opts}")

    valid_quantity = None
    if isinstance(value, unyt_quantity):
        try:
            valid_quantity = value.to(exp_dim)
        except UnitConversionError:
            raise TypeError(f"Cannot convert {value.units} to {exp_dim}")
    elif isinstance(value, float):
        valid_quantity = value * exp_dim
    elif isinstance(value, int):
        valid_quantity = value * exp_dim
    elif isinstance(value, str):
        try:
            valid_quantity = float(value) * exp_dim
        except ValueError:
            try:
                unyt_value = unyt_quantity.from_string(value)
                assert unyt_value.units.same_dimensions_as(exp_dim)
                valid_quantity = unyt_value
            except UnitParseError:
                raise UnitParseError(f"Could not interpret <{value}>.")
            except AssertionError:
                raise AssertionError(f"{value} lacks units of {dimension}.")
    else:
        raise ValueError(f"Value of type <{type(value)}> passed.")
    return valid_quantity


class Technology(object):
    """
    Parameters
    ----------
    technology_name : string
        The name identifier of the technology.
    technology_type : string
        The string identifier for the type of technology.
    capital_cost : float or :class:`unyt.array.unyt_quantity`
        Specifies the capital cost. If float,
        the default unit is $/MW.
    om_cost_fixed : float or :class:`unyt.array.unyt_quantity`
        Specifies the fixed operating costs.
        If float, the default unit is $/MW.
    om_cost_variable : float or :class:`unyt.array.unyt_quantity`
        Specifies the variable operating costs.
        If float, the default unit is $/MWh.
    fuel_cost : float or :class:`unyt.array.unyt_quantity`
        Specifies the fuel costs.
        If float, the default unit is $/MWh.
    capacity : float or :class:`unyt.array.unyt_quantity`
        Specifies the technology capacity.
        If float, the default unit is MW
    default_power_units : str or :class:`unyt.unit_object.Unit`
        An optional parameter, specifies the units
        for power. Default is megawatts [MW].
    default_time_units : str or :class:`unyt.unit_object.Unit`
        An optional parameter, specifies the units
        for time. Default is hours [hr].
    default_energy_units : str or :class:`unyt.unit_object.Unit`
        An optional parameter, specifies the units
        for energy. Default is megawatt-hours [MWh]
        Currently, `default_energy_units` is derived from the
        time and power units.

    Notes
    -----
    Cost values are listed in the docs as [$ / physical unit]. However,
    :class:`osier` does not currently have a currency handler, therefore the
    units are technically [1 / physical unit].

    The :class:`unyt` library may not be able to interpret strings for
    inverse units. For example:

    >>> my_unit = "10 / MW"
    >>> my_unit = unyt_quantity.from_string(my_unit)
    ValueError: Received invalid quantity expression '10/MW'.

    Instead, try the more explicit approach:

    >>> my_unit = "10 MW**-1"
    >>> my_unit = unyt_quantity.from_string(my_unit)
    unyt_quantity(10., '1/MW')

    However, inverse MWh cannot be converted from a string.
    """

    def __init__(self,
                 technology_name,
                 technology_type='base',
                 capital_cost=0.0,
                 om_cost_fixed=0.0,
                 om_cost_variable=0.0,
                 fuel_cost=0.0,
                 capacity=0.0,
                 default_power_units=MW,
                 default_time_units=hr,
                 default_energy_units=None) -> None:

        self.technology_name = technology_name
        self.technology_type = technology_type

        self.unit_power = default_power_units
        self.unit_time = default_time_units
        self.unit_energy = default_energy_units

        self.capacity = capacity
        self.capital_cost = capital_cost
        self.om_cost_fixed = om_cost_fixed
        self.om_cost_variable = om_cost_variable
        self.fuel_cost = fuel_cost

    @property
    def unit_power(self):
        return self._unit_power

    @unit_power.setter
    def unit_power(self, value):
        self._unit_power = _validate_unit(value, dimension="power")

    @property
    def unit_time(self):
        return self._unit_time

    @unit_time.setter
    def unit_time(self, value):
        self._unit_time = _validate_unit(value, dimension="time")

    @property
    def unit_energy(self):
        return self._unit_power*self._unit_time

    @unit_energy.setter
    def unit_energy(self, value):
        self._unit_energy = self._unit_power * self._unit_time

    @property
    def capacity(self):
        return self._capacity.to(self._unit_power)

    @capacity.setter
    def capacity(self, value):
        valid_quantity = _validate_quantity(value, dimension="power")
        self._capacity = valid_quantity.to(self._unit_power)

    @property
    def capital_cost(self):
        return self._capital_cost.to(self._unit_power**-1)

    @capital_cost.setter
    def capital_cost(self, value):
        self._capital_cost = _validate_quantity(value, dimension="spec_power")

    @property
    def om_cost_fixed(self):
        return self._om_cost_fixed.to(self._unit_power**-1)

    @om_cost_fixed.setter
    def om_cost_fixed(self, value):
        self._om_cost_fixed = _validate_quantity(value, dimension="spec_power")

    @property
    def om_cost_variable(self):
        return self._om_cost_variable.to(self.unit_energy**-1)

    @om_cost_variable.setter
    def om_cost_variable(self, value):
        self._om_cost_variable = _validate_quantity(
            value, dimension="spec_energy")

    @property
    def fuel_cost(self):
        return self._fuel_cost.to(self.unit_energy**-1)

    @fuel_cost.setter
    def fuel_cost(self, value):
        self._fuel_cost = _validate_quantity(value, dimension="spec_energy")
