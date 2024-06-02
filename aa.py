# # def create_unique_number():
# #     number = generate_number()
# #     with open("card_number.txt", 'r') as file:
# #         if not number in file.read().replace(" ", "").split("\n"):
# #             with open("card_number.txt", "a") as write_file:
# #                 write_file.write(f"{number}\n")
# #             return number
# #     return create_unique_number()
# from base.helper import generate_number
#
# number = "5614 5677 7153 5315"
# with open("card_number.txt", 'r') as file:
#     a = file.read().split("\n")
#     print(a)
#     if not number in a:
#         with open("card_number.txt", "a") as write_file:
#             write_file.write(f"{number}\n")
#         print(number)


