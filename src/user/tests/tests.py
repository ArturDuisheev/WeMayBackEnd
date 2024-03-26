# # def to_camel_case(text):
# #     return text[:1] + text.title()[1:].replace('_', '').replace('-', '')



# from collections import Counter

# # def find_dup(arr: list):
# #     a = 0
# #     for i in arr:
# #         if arr[i]:
# #             a = arr[i - 1]
            
           


# #     return a 

# def find_dup(arr: list):
#     a = 0
#     for i in arr:
#         for j in arr:
#             if i in arr and j in arr:
#                 if i == j:
#                     c = arr[i], arr[j]
#                     if c.coun) >= 2:
#                         a = c
            
            
           


#     return a           


# print(find_dup([35, 44, 7, 38, 20, 12, 46, 21, 13, 31, 10, 50, 52, 4, 32, 42, 37, 30, 24, 5, 17, 48, 12, 1, 18, 47, 8, 36, 53, 51, 14, 45, 19, 43, 16, 28, 23, 39, 6, 11, 29, 34, 2, 3, 33, 49, 22, 41, 40, 25, 15, 26, 27, 9]))