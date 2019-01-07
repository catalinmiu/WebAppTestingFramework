import unittest


class Employee:
    """A sample Employee class"""

    def __init__(self, first, last, age):
        self.first = first
        self.last = last
        self.age = age

        print('Created Employee: {} - {}'.format(self.fullname, self.email))

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)


class TestEmployee(unittest.TestCase):
    emp_1 = Employee('John', 'Smith', 22)
    emp_2 = Employee('Corey', 'Schafer', 33)
    emp_3 = Employee('Jane', 'Doe', 44)

    def test_first_names(self):
        """Testing employees first name
        """
        self.assertEqual(self.emp_1.first, 'John')
        self.assertEqual(self.emp_2.first, 'Corey')
        self.assertEqual(self.emp_3.first, 'Jane')

    def test_last_names(self):
        """Testing employees last name
        """
        self.assertEqual(self.emp_1.last, 'Smith')
        self.assertEqual(self.emp_2.last, 'Schafer')
        self.assertEqual(self.emp_3.last, 'Doe')

    def test_employee_ages(self):
        """Testing employees age
        """
        self.assertEqual(self.emp_1.age, 22)
        self.assertEqual(self.emp_2.age, 33)
        self.assertEqual(self.emp_3.age, 44)

    def test_employee_functions(self):
        """Testing employees functions
        """
        self.skipTest('Function attribute not implemented yet')
