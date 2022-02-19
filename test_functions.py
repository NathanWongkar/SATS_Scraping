from Functions import (
    getting_stats,
    finding_the_best_meal
)

test_link = "https://satscampuseats.yale-nus.edu.sg/our-food?q=f2684700-6e97-11ec-bb8c-35aa48993d35"

# getting_stats(test_link)


def test_getting_stats():
    assert getting_stats(test_link) == ['Fried Tom Yum Mee Tai Mak, Wok Fried Chicken Basil, Baked Thai Fish Cake , Cabbage And Carrot Chap Chye', 444.0, 21.0, 22.0, 31.0, 4.954954954954955]


test_links = ['https://satscampuseats.yale-nus.edu.sg/our-food?q=7d69e8e0-6e98-11ec-bb8c-35aa48993d35', 
'https://satscampuseats.yale-nus.edu.sg/our-food?q=9abcedc0-6e98-11ec-bb8c-35aa48993d35', 
'https://satscampuseats.yale-nus.edu.sg/our-food?q=84a2dbc0-6e99-11ec-bb8c-35aa48993d35', 
'https://satscampuseats.yale-nus.edu.sg/our-food?q=a433e9c0-6e99-11ec-bb8c-35aa48993d35']

# finding_the_best_meal(test_links)


def test_finding_the_best_meal():
    assert finding_the_best_meal(test_links) == ['Pasta, Coconut Laska Sauce, Mixed Seafood, Hard Boiled Egg & Surimi Breaded Scallop', 481.0, 22.0, 39.0, 26.0, 8.108108108108109]
