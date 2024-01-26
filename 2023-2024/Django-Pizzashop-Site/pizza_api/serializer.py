from rest_framework import serializers
from django.db.models import F
from backend.models import Customer, Order, Pizza


class PizzaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    price = serializers.FloatField()

    class Meta:
        model = Pizza

    def get_all_pizza(self):
        return Pizza.objects.all().values('name', 'price')

    def create(self, validated_data):
        return Pizza.objects.create(**validated_data)

    def exists(self, validated_data):
        return Pizza.objects.filter(name=validated_data['name']).exists()


class UserSerializer(serializers.Serializer):
    firstname = serializers.CharField(max_length=100)
    lastname = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    postcode = serializers.IntegerField()
    city = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)

    class Meta:
        model = Customer

    def get_with_username(self, username):
        return Customer.objects.get(username=username)

    def get_with_email(self, email):
        return Customer.objects.get(email=email)

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def exists(self, validated_data):
        return Customer.objects.filter(email=validated_data['email']).exists()


class OrderSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    time = serializers.TimeField()
    pizzas = serializers.ListField()

    class Meta:
        model = Order

    def get_all_orders(self):
        return Order.objects.annotate(pizza_name=F('pizzas__name')).values('customer', 'pizza_name', 'amount',
                                                                           'total_price', 'date', 'time')


    def create(self, validated_data):
        user = Customer.objects.get(email=validated_data['email'])
        pizzas = [(list(pizza.keys())[0], int(list(pizza.values())[0])) for pizza in validated_data['pizzas']]
        for pizza_name, amount in pizzas:
            pizza = Pizza.objects.get(name=pizza_name)

            order = user.order_set.create(amount=amount, total_price=round(pizza.price * amount, 2),
                                          time=validated_data['time'])
            order.pizzas.set([pizza])
            order.save()

    def customer_exists(self, validated_data):
        return Customer.objects.filter(email=validated_data['email']).exists()


class OrderDeleteSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    date = serializers.DateField()
    time = serializers.TimeField()

    class Meta:
        model = Order

    def delete(self, validated_data):
        user = Customer.objects.get(email=validated_data['email'])
        Order.objects.filter(customer=user, date=validated_data['date'],
                             time=validated_data['time']).delete()

    def order_exists(self, validated_data):
        user = Customer.objects.get(email=validated_data['email'])
        return Order.objects.filter(customer=user, date=validated_data['date'],
                                    time=validated_data['time']).exists()

    def customer_exists(self, validated_data):
        return Customer.objects.filter(email=validated_data['email']).exists()
