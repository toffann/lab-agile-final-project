import factory
from factory.fuzzy import FuzzyChoice
from service.models import Product, Category

class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.fuzzy.FuzzyChoice(choices=["Laptop", "Smartphone", "Keyboard", "Mouse", "Monitor"])
    description = factory.Faker("text")
    price = factory.fuzzy.FuzzyFloat(9.99, 499.99)
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(choices=[
        Category.UNKNOWN, 
        Category.CLOTHES, 
        Category.FOOD, 
        Category.HOUSEWARES, 
        Category.AUTOMOTIVE, 
        Category.TOOLS
    ])