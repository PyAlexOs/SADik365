from typing import Any
import random
import re


class OntologyObject():
    shown_field = 'name'

    def __str__(self) -> str:
        if isinstance(self, Product):
            self.shown_field = 'model'
        return getattr(self, self.shown_field)


class Product(OntologyObject):
    instances = []

    def __init__(self, brand: str, model: str, color: str, price: int, size: float) -> None:
        self.brand = brand
        self.model = model
        self.color = color
        self.price = price
        self.size = size
        Product.instances.append(self)


class User(OntologyObject):
    instances = []

    def __init__(self, name: str, is_active: bool):
        self.name = name
        self.is_active = is_active
        User.instances.append(self)


class Shoes(Product):
    instances = []

    def __init__(self, brand: str, model: str, color: str, price: int, size: float, heel_height: str):
        super().__init__(brand, model, color, price, size)
        self.heel_height = heel_height
        Shoes.instances.append(self)


class Pants(Product):
    instances = []

    def __init__(self, brand: str, model: str, color: str, price: int, size: float, fit_type: str, fits_well: list[Shoes]):
        super().__init__(brand, model, color, price, size)
        self.fit_type = fit_type
        self.fits_well = fits_well
        Pants.instances.append(self)


class Shirt(Product):
    instances = []

    def __init__(self, brand: str, model: str, color: str, price: int, size: float, buttons: int, fits_style: list[Pants]):
        super().__init__(brand, model, color, price, size)
        self.buttons = buttons
        self.fits_style = fits_style
        Shirt.instances.append(self)


class Seller(User):
    instances = []

    def __init__(self, name: str, is_active: bool, products: list[Product]):
        super().__init__(name, is_active)
        self.products = products
        Seller.instances.append(self)


class Customer(User):
    instances = []

    def __init__(self, name: str, is_active: bool, redemption: int, shopping_list: list[Product]):
        super().__init__(name, is_active)
        self.redemption = redemption
        self.shopping_list = shopping_list
        Customer.instances.append(self)


def find_related_objects_by_value(cls: OntologyObject.__class__,
                                  lookup_field: str, value: Any):
    instances = cls.instances
    result = []
    for instance in instances:
        if isinstance(getattr(instance, lookup_field), OntologyObject):
            if not isinstance(value, OntologyObject):
                value = find_object_by_name(
                    getattr(instance, lookup_field).__class__, value)
                if value is None:
                    return None

        if isinstance(getattr(instance, lookup_field), bool):
            value = bool(value)
        elif isinstance(getattr(instance, lookup_field), int):
            value = int(value)
        elif isinstance(getattr(instance, lookup_field), float):
            value = float(value)

        if isinstance(getattr(instance, lookup_field), list):
            for subfield in getattr(instance, lookup_field):
                if subfield == value:
                    result.append((instance, type(instance).__name__))
        else:
            if getattr(instance, lookup_field) == value:
                result.append((instance, type(instance).__name__))
    return result


def find_object_by_name(cls: OntologyObject.__class__, name: str):
    instances = cls.instances
    for instance in instances:
        if instance.name == name:
            return instance

    return None


def get_class(class_name: str):
    classes = {
        'shirt': Shirt,
        'pants': Pants,
        'shoes': Shoes,
        'seller': Seller,
        'customer': Customer
    }

    class_name = class_name.lower().strip()
    if class_name in classes:
        return classes[class_name]
    else:
        return None


def get_random_class_instance(cls: OntologyObject.__class__):
    instances = cls.instances
    return random.choice(instances)


def get_related_class(obj: OntologyObject):
    classes = [Shirt, Pants, Shoes, Seller, Customer]
    class_types = set()
    for cls in classes:
        cls_instances = cls.instances
        for instance in cls_instances:
            fields = [
                key for key in instance.__dict__.keys()
                if not re.match(r"__\w*__", key)
            ]
            for field in fields:
                field_value = getattr(instance, field)
                if field_value == obj:
                    class_types.add((cls, field))
                elif isinstance(field_value, list):
                    for subfield_value in field_value:
                        if subfield_value == obj:
                            class_types.add((cls, field))

    return list(class_types)


def main():
    shoes = [
        Shoes('Gucci', 'Ace Sneakers', 'black', 4390, 42., 'low'),
        Shoes('Manolo Blahnik', 'BB Pumps', 'black', 5290, 40., 'flat'),
        Shoes('Jimmy Choo', 'Lockett Petite Boots', 'pink', 4890, 42., 'high'),
        Shoes('Gucci', 'Princetown Loafers', 'brown', 5290, 44., 'flat')
        ]
    pants = [
        Pants('Tommy Hilfiger', 'Athletic Fit Pants', 'blue', 4990, 56., 'slim', [shoes[0], shoes[1]]),
        Pants('Tommy Hilfiger', 'Classic Fit Chinos', 'black', 3890, 58., 'regular', [shoes[0], shoes[3]]),
        Pants('Armani', 'Collezioni Trousers', 'black', 4590, 50., 'regular', [shoes[0], shoes[1], shoes[2], shoes[3]]),
        Pants('Calvin Klein', 'Modern Cotton', 'brown', 2990, 52., 'slim', [shoes[3]])
        ]
    shirts = [
        Shirt('Brooks Brothers', 'Non-Iron Dress', 'white', 2590, 54., 10, [pants[1], pants[2]]),
        Shirt('Hugo Boss', 'The Boss Green Shirt', 'white', 2690, 56., 10, [pants[0], pants[1], pants[2], pants[3]]),
        Shirt('Hugo Boss', 'The Boss Selection Shirt', 'black', 3290, 54., 12, [pants[0], pants[3]]),
        Shirt('Thomas Pink', 'The Oxford', 'pink', 2290, 58., 12, [pants[3]])
        ]
    sellers = [
        Seller('best wear', True, [pants[0], pants[1], pants[2], pants[3], shoes[0], shoes[3]]),
        Seller('gentle', True, [shoes[0], shoes[2], shoes[3]]),
        Seller('your shop', False, [shirts[0], shirts[1], shirts[2], shoes[1]]),
        ]
    customers = [
        Customer('Bob', False, 54, [pants[0], pants[1]]),
        Customer('Carl', True, 79, [shoes[0], shoes[3]]),
        Customer('Liam', True, 98, [shoes[0], shirts[2], pants[1]]),
        Customer('Susan', True, 97, [pants[0], pants[2], shirts[2]]),
        ]

    while True:
        while True:
            class_name = input('Введите класс получаемых объектов: ')
            cls: OntologyObject.__class__ | None = get_class(class_name)
            if cls is None:
                print('Такого класса не существует\n\n')
            else:
                break

        while True:
            instance = get_random_class_instance(cls)
            available_fields = [
                key for key in instance.__dict__.keys()
                if not re.match(r"__\w*__", key)
            ]
            field = input(
                f'Введите требуемое поле ( {", ".join(available_fields)} ): ')
            try:
                getattr(instance, field)
                break
            except Exception:
                print('Такого поля в классе не существует\n\n')

        value = input('Введите значение поля: ')
        res = find_related_objects_by_value(cls, field, value)

        while True:
            flag = False
            if res is None or len(res) == 0:
                print('Объекты по введённому запросу не найдены')
                while True:
                    _type = input(
                        '1 - повторить ввод запроса\nq - завершить выполнение программы\n'
                    )
                    if _type == '1':
                        break
                    elif _type == 'q':
                        exit(0)
            else:
                str_objects = [
                    "\033[32m" + str(obj) + "\033[0m (\033[33m" +
                    str(obj_type) + "\033[0m)" for obj, obj_type in res
                ]
                print(f'Полученные объекты: {", ".join(str_objects)}')
                while True:
                    _type = input('1 - повторить ввод запроса\n'
                                  '2 - посмотреть связанные объекты\n'
                                  'q - завершить выполнение программы\n')
                    if _type == '1':
                        flag = False
                        break
                    elif _type == '2':
                        flag = True
                        break
                    elif _type == 'q':
                        exit(0)

                if flag:
                    if len(res) == 1:
                        obj_number = 1
                    else:
                        while True:
                            obj_number = int(
                                input(
                                    f'Выберите номер нужного объекта (1-{len(res)}): '
                                ))
                            if obj_number not in range(1, len(res) + 1):
                                print('Введён неправильный номер')
                            else:
                                break

                    instance = res[obj_number - 1][0]
                    related_classes = get_related_class(instance)
                    res = []
                    for rel_class, field_name in related_classes:
                        res.extend(
                            find_related_objects_by_value(
                                rel_class, field_name, instance))
                else:
                    break
            if not flag:
                break


if __name__ == "__main__":
    main()
