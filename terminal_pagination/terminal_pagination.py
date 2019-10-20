# coding=utf-8

from ansi_colours import AnsiColours as Colour
from terminal_table import Table

from input import Input
from underline import Underline


class Pagination:

    def __init__(self, arr, headers):
        self.arr = tuple((i+1, *a) for (i, a) in enumerate(arr))
        self.headers = ('', *headers)

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
                print('\n')
                continue
            if user_input not in [str(x) for x in range(1, len(self.arr) + 1)]:
                Input.get("\n%s\nPress any key to continue.\n" % Colour.red("The row number entered was not found."))
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
            self.headers,
            column_colours=(Colour.green,)
        )

    def pagination_text(self):
        text = ""
        length = 0
        if self.page > 1:
            text += f"{Colour.green('<')} previous | "
            length += 11
        text += "%d" % self.page
        if self.page * self.limit < self.total:
            text += f" | next {Colour.green('>')}"
            length += 11

        return f"{Underline.create(len(text) - length)}\n{text}\n{Underline.create(len(text) - length)}"

    def display_pagination_instructions(self):
        return '\nChoose a \'%s\' to select a row, use %s and %s to navigate, or %s to go back: ' % (
            Colour.green("number"),
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
    long_text = 'Zombie ipsum brains reversus ab cerebellum viral inferno, brein nam rick mend grimes malum cerveau cerebro.'

    arr = (
        ('Name One', long_text[:30]),
        ('Name Two', long_text[:21]),
        ('Name Three', long_text[:35]),
        ('Name Four', long_text[:45]),
        ('Name Five', long_text[:32]),
        ('Name Six', long_text[:20]),
    )
    pick = Pagination(arr, ('Name', 'Value'))(2)
    if type(pick) is not bool:
        print('You chose: %s' % pick[1])


