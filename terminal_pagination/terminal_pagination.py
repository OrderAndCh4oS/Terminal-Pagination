# coding=utf-8

from ansi_colours import AnsiColours as Colour
from terminal_table.table import Table

from input import Input
from underline import Underline


class Pagination:

    def __init__(self, arr, headers):
        self.arr = arr
        self.headers = headers

    def __call__(self, limit=5, find=None, find_by_id=None):
        self.limit = limit
        self.total = len(self.arr)
        self.page = 1
        return self.menu()

    def menu(self):
        result = False
        while not result:
            print(self.paginated_table())
            print(self.pagination_text())
            user_input = Input.get('\nEnter an %s, use %s and %s to navigate, or %s to go back: ' % (
                Colour.green("'id'"),
                Colour.green("<"),
                Colour.green(">"),
                Colour.green("b")
            ))
            if user_input == 'b':
                break
            if self.should_change_page(user_input):
                self.change_page(user_input)
                continue
            if user_input not in [str(x) for x in range(1, len(self.arr) + 1)]:
                continue
            result = self.arr[int(user_input) - 1]
            print("An item with that key was not found. Press any key to continue.")
        return result

    def paginated_table(self):
        arr_start = (self.page * self.limit) - self.limit
        arr_end = (self.page * self.limit)
        return Table.create(
            self.arr[arr_start:arr_end],
            self.headers
        )

    def pagination_text(self):
        text = ""
        if self.page > 1:
            text += "< previous | "
        text += "page %d" % self.page
        if self.page * self.limit < self.total:
            text += " | next >"
        output = Underline.create(text)
        output += "\n%s\n" % text
        output += Underline.create(text)

        return output

    def should_change_page(self, user_input):
        return user_input is '<' or user_input is '>'

    def change_page(self, user_input):
        if self.page is not 1 and user_input is '<':
            self.page -= 1
        elif self.page * self.limit < self.total and user_input is '>':
            self.page += 1


if __name__ == '__main__':
    Pagination((('1', 'col_two_cell'), ('2', 'col_two_cell')), ('id', 'col_two_header'))()
