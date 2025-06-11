# utils/unit_converter.py
class UnitConverter:
    """Handles unit conversions between domains"""
    
    @staticmethod
    def permeability_to_md(value, input_unit):
        """Convert various permeability units to millidarcies"""
        conversions = {
            'm²': value * 1.01325e15,  # square meters to mD
            'darcy': value * 1000,
            'mD': value
        }
        return conversions.get(input_unit, value)
    
    @staticmethod
    def porosity_to_fraction(value, input_unit):
        """Convert porosity to fraction (0-1)"""
        if input_unit == 'percentage':
            return value / 100
        return value
