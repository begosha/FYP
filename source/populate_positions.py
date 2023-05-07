#!/usr/bin/env python

import os
import random

import django
from calculator.models import Position

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'price_calculator.settings')
django.setup()


def main():
    # Replace 'dishes.txt' with the path to your text file
    with open('object_classification/classes.txt', 'r') as file:
        for line in file:
            # Remove leading/trailing whitespace and newline characters
            dish_name = line.strip()

            # Generate a random integer divisible by 10
            price = random.randint(1, 10) * 10

            # Create a new Position object with the dish name and random price
            position = Position(name=dish_name, price=price)

            # Save the Position object to the database
            position.save()

    print("Positions populated successfully.")


if __name__ == "__main__":
    main()
