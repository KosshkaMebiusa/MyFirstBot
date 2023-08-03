def custom_filter(l: list) -> bool:
    filtered_list = filter(lambda x: (type(x) is int) and x % 7 == 0, l)
    return sum(_ for _ in filtered_list ) <= 83

# some_list = [7, 14, 28, 32, 32, 56]
# print(custom_filter(some_list))


anonymous_filter = lambda s: s.lower().count('я') >= 23
print(anonymous_filter('яяяяяяяяяяяяяяяяяяяяяяяя, яяяяяяяяяяяяяяяя и яяяяяяяя тоже!'))