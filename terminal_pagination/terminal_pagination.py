# coding=utf-8

from ansi_colours import AnsiColours as Colour
from terminal_table.table import Table

from input import Input
from underline import Underline


class Pagination:

    def __init__(self, arr, headers):
        self.arr = tuple((i+1, *a) for (i, a) in enumerate(arr))
        self.headers = ('Key', *headers)

    def __call__(self, limit=5, find=None, find_by_id=None):
        self.limit = limit
        self.total = len(self.arr)
        self.page = 1
        return self.pagination()

    def pagination(self):
        result = False
        while not result:
            self.display_pagination()
            user_input = Input.get(self.display_pagination_instructions())
            if user_input == 'b':
                break
            if self.should_change_page(user_input):
                self.change_page(user_input)
                continue
            if user_input not in [str(x) for x in range(1, len(self.arr) + 1)]:
                Input.get("\n%s\nPress any key to continue.\n" % Colour.red("The Key entered was not found."))
                continue
            result = self.arr[int(user_input) - 1]
        return result

    def display_pagination(self):
        print(self.paginated_table())
        print(self.pagination_text())

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

    def display_pagination_instructions(self):
        return '\nChoose a \'%s\' to select a row, use %s and %s to navigate, or %s to go back: ' % (
            Colour.green("Key"),
            Colour.green("<"),
            Colour.green(">"),
            Colour.green("b")
        )

    def should_change_page(self, user_input):
        return user_input is '<' or user_input is '>'

    def change_page(self, user_input):
        if self.page is not 1 and user_input is '<':
            self.page -= 1
        elif self.page * self.limit < self.total and user_input is '>':
            self.page += 1


if __name__ == '__main__':
    arr = (
        ('Name One', 'Value One'),
        ('Name Two', 'Value Two'),
        ('Name Three', 'Value Three'),
        ('Name Four', 'Value Four'),
        ('Name Five', 'Value Five'),
        ('Name Six', 'Value Six'),
    )
    pick = Pagination(arr, ('Name', 'Value'))(3)
    if type(pick) is not bool:
        print('You chose: %s' % pick[1])
