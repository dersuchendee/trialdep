import csv
from abc import ABC, abstractmethod
from typing import List, Dict


class UnitOfMeasures:
    MPG = 'mpg'
    CC = 'cc'
    HP = 'hp'
    KG = 'kg'
    SECONDS = 'secs'


class ModelCharacteristic(ABC):

    def __init__(self, value, unit_of_measure: UnitOfMeasures):
        self._value = value
        self._unit_of_measure: UnitOfMeasures = unit_of_measure

    def get_value(self):
        return self._value

    def get_unit_of_measure(self) -> UnitOfMeasures:
        return self._unit_of_measure

    @abstractmethod
    def get_meaningful_value(self) -> str:
        pass


class SimpleModelCharacteristic(ModelCharacteristic):

    def __init__(self, value):
        super().__init__(value, None)

    def get_meaningful_value(self) -> str:
        return self._value


class ComplexModelCharacteristic(ModelCharacteristic):

    def __init__(self, value, unit_of_measure: UnitOfMeasures):
        super().__init__(value, unit_of_measure)

    def get_meaningful_value(self) -> str:
        return f'{self._value} {self._unit_of_measure}'


class MilesPerGallon(ComplexModelCharacteristic):

    def __init__(self, value):
        super().__init__(value, UnitOfMeasures.MPG)


class NumberOfCylinders(SimpleModelCharacteristic):

    def __init__(self, value):
        super().__init__(value)


class Displacement(ComplexModelCharacteristic):

    def __init__(self, value):
        super().__init__(value, UnitOfMeasures.CC)


class HorsePower(ComplexModelCharacteristic):

    def __init__(self, value):
        super().__init__(value, UnitOfMeasures.HP)


class Weight(ComplexModelCharacteristic):

    def __init__(self, value):
        super().__init__(value, UnitOfMeasures.KG)


class Acceleration(ComplexModelCharacteristic):

    def __init__(self, value):
        super().__init__(value, UnitOfMeasures.SECONDS)


class Year(SimpleModelCharacteristic):

    def __init__(self, value):
        super().__init__(value)


class ModelCharacteristicBuilder():
    CHARACTERISTICS_DICT = {
        'mpg': MilesPerGallon,
        'cylinders': NumberOfCylinders,
        'displacement': Displacement,
        'horsepower': HorsePower,
        'weight': Weight,
        'acceleration': Acceleration,
        'year': Year
    }

    @staticmethod
    def build(characteristic_name: str, *args) -> ModelCharacteristic:

        characteristic = ModelCharacteristicBuilder.CHARACTERISTICS_DICT[characteristic_name]

        if characteristic:
            return characteristic(*args)
        else:
            return None


class Model:

    def __init__(self, manufacturer: 'Manufacturer', model_name, characteristics: List[ModelCharacteristic]):
        self.__model_name = model_name
        self.__manufacturer = manufacturer
        self.__characteristics = characteristics

    def get_model_name(self) -> str:
        return self.__model_name

    def get_manufacturer(self) -> 'Manufacturer':
        return self.__manufacturer

    def get_characteristics(self) -> List[ModelCharacteristic]:
        return self.__characteristics


class Manufacturer:

    def __init__(self, brand: str):
        self.__brand: str = brand
        self.__models: List[Model] = []

    def get_brand(self) -> str:
        return self.__brand

    def add_model(self, model: Model):
        self.__models.append(model)

    def get_all_models(self) -> List[Model]:
        return self.__models


class ModelBuilder:

    @staticmethod
    def build(registry, **kwargs):

        name_parts = kwargs['name'].split()
        brand = name_parts[0]
        model_name = ' '.join(name_parts[1:])

        if brand in registry:
            manufacturer = registry[brand]
        else:
            manufacturer = Manufacturer(brand)
            registry.update({brand: manufacturer})

        characteristics = []
        for key, value in kwargs.items():
            if key != 'name':
                characteristic = ModelCharacteristicBuilder.build(key, value)
                characteristics.append(characteristic)

        model = Model(manufacturer, model_name, characteristics)
        manufacturer.add_model(model)

        return registry


class DatasetReader:

    @staticmethod
    def read(data_path):

        registry = dict()

        with open(data_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            header = []
            for row in csv_reader:
                if line_count == 0:
                    header = row
                else:
                    item_count = 0
                    representation = dict()
                    for item in row:
                        print(item)
                        representation.update({header[item_count]: item})
                        item_count += 1

                    ModelBuilder.build(registry, **representation)

                line_count += 1

        return registry
