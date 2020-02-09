import unittest
from functools import reduce

from functions import build_adder, add_two_ints
from functions import build_idiomatic_adder
from functional import seq

from when_to_use_example import Failure, Success, workflow, unit, bind
from objects import Car, Person

driving_age = 16


def person_is_of_age(x):
    person = x[0]
    if person.age < driving_age:
        return Failure(x, '{} is only {}, and needs to be at least {} to drive.'.format(person.name,
                                                                                        person.age,
                                                                                        driving_age))
    return Success(x, '{} is {}, which is of driving age, {}.'.format(person.name, person.age, driving_age))


def person_is_licensed(x):
    person = x[0]
    if person.licensed is False:
        return Failure(x, '{} is not licensed'.format(person.name))
    return Success(x, '{} is licensed'.format(person.name))


def car_has_wheels(x):
    person, car, _ = x
    msg = "{}'s {} {} has {} wheels".format(person.name,
                                            car.make,
                                            car.model,
                                            car.wheels)
    if car.wheels <= 0:
        return Failure(x, msg)
    return Success(x, msg)


def drive(x):
    person, car, distance = x
    car.fuel = max(car.fuel - distance, 0)
    if car.fuel == 0:
        return Failure(x, "{}'s {} {} ran out of fuel".format(person.name, car.make, car.model))
    return Success(x, '{} drove {} miles. Remaining fuel: {}'.format(person.name, distance, car.fuel))


class MyTestCase(unittest.TestCase):

    def test_workflow(self):
        person = Person('Sam', 20, True)
        car = Car('Honda', 'Civic')
        car.wheels = 4
        distance = 90
        result = workflow(unit((person, car, distance)),
                          person_is_of_age,
                          person_is_licensed,
                          car_has_wheels,
                          drive)
        self.assertIsInstance(result, Success)

    def test_without_workflow(self):
        person = Person('Sam', 20, True)
        car = Car('Honda', 'Civic')
        distance = 90
        result = \
            bind(
                bind(
                    bind(
                        bind(
                            unit((person, car, distance)),
                            person_is_of_age)
                        , person_is_licensed)
                    , car_has_wheels)
                , drive)
        self.assertIsInstance(result, Success)

    def test_without_bind(self):
        person = Person('Sam', 20, True)
        car = Car('Honda', 'Civic')
        distance = 90
        pair = (person, car, distance)
        age_check_result = person_is_of_age(pair)
        if isinstance(age_check_result, Success):
            print(age_check_result.msg)
            license_check_result = person_is_licensed(pair)
            if isinstance(license_check_result, Success):
                print(license_check_result.msg)
                wheel_check_result = car_has_wheels(pair)
                if isinstance(wheel_check_result, Success):
                    print(wheel_check_result.msg)
                    drive_result = drive(pair)
                    if isinstance(drive_result, Success):
                        print(drive_result.msg)
                        self.assertIsInstance(drive_result, Success)
                    else:
                        print(drive_result.msg)
                        self.assertIsInstance(drive_result, Success)
                else:
                    print(wheel_check_result.msg)
                    self.assertIsInstance(wheel_check_result, Success)
            else:
                print(license_check_result.msg)
                self.assertIsInstance(license_check_result, Success)
        else:
            print(age_check_result.msg)
            self.assertIsInstance(age_check_result, Success)

    def test_adding_works(self):
        self.assertEqual(3, add_two_ints(1, 2))

    # typical test structure: Arrange, Act, Assert (AKA Given, When, Then)
    def test_returning_functions(self):
        # arrange
        adder_a = build_adder(1)
        adder_b = build_idiomatic_adder(1)

        # act
        a = adder_a(2)
        b = adder_b(2)

        # assert
        self.assertEqual(a, b)

    # this is fine, too (some folks prefer it)
    def test_returning_functions_DRY(self):
        self.assertEqual(build_adder(1)(2), build_idiomatic_adder(1)(2))

    # this might be where you compromise with other developers
    def test_returning_functions_compromise(self):
        # get the values to debug here
        a = build_adder(1)(2)
        b = build_idiomatic_adder(1)(2)

        # set breakpoint here; examine a, b
        self.assertEqual(a, b)

    def test_using_lambdas(self):
        # this is not encouraged idiomatic Python
        strings = '0 1 2 3 4 5 6'.split()
        nums = map(lambda x: int(x), strings)
        filtered = filter(lambda x: x % 2 == 0, nums)
        reduced = reduce(lambda x, y: x + y, filtered)
        self.assertEqual(reduced, 12)

    def test_using_lib(self):
        # this is how you'd use lambdas in languages that encourage map, filter, reduce
        self.assertEqual(
            12,
            seq('0 1 2 3 4 5 6'.split())
                .map(lambda x: int(x))
                .filter(lambda x: x % 2 == 0)
                .reduce(lambda x, y: x + y)
        )

    def test_python(self):
        # this is how you'd do it in idiomatic Python
        self.assertEqual(
            12,
            # sum([int(x) for x in seq('0 1 2 3 4 5 6'.split()) if int(x) % 2 == 0])
            sum([x for x in range(7) if x % 2 == 0])
        )


if __name__ == '__main__':
    unittest.main()
