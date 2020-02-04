import PySimpleGUI as sg
import random

GRAPH_SIZE = (700, 500)
BAR_SPACING, BAR_WIDTH = 11, 10
BARS = GRAPH_SIZE[0] // (BAR_WIDTH + 1)
VALUES = GRAPH_SIZE[1]


def insertion_sort(array):
    for i in range(len(array)):
        current = array[i]
        position = i
        while position > 0 and current < array[position - 1]:
            array[position] = array[position - 1]
            position -= 1
            yield array
        array[position] = current
    yield array


def draw(graph, array):
    for i, item in enumerate(array):
        graph.draw_rectangle(top_left=(i * BAR_SPACING, item),
                             bottom_right=(i * BAR_SPACING + BAR_WIDTH, 0), fill_color='#76506d')


def merge(array, left, right):
    i = 0
    j = 0
    while j < len(right) and i < len(left):
        if left[i] < right[j]:
            array[i + j] = left[i]
            i += 1
        else:
            array[i + j] = right[j]
            j += 1
    while i < len(left):
        array[i + j] = left[i]
    while j < len(right):
        array[i + j] = right[j]
    yield array


def mergesort(array):
    if len(array) > 1:
        middle = len(array) // 2
        yield from mergesort(array[:middle])
        yield from mergesort(array[middle:])
        merge(array, array[:middle], array[middle:])
    yield array


def quicksort(array):
    pass


def main():
    sg.change_look_and_feel('LightGreen')
    graph = sg.Graph(GRAPH_SIZE, (0, 0), GRAPH_SIZE)
    layout = [[graph]]
    array = [j for _ in range(1, BARS) for j in range(1, VALUES)]
    random.shuffle(array)
    window = sg.Window('Sorting Algorithm Visualizer', layout, finalize=True)
    draw(graph, array)

    layout2 = [[sg.T("Choose Algorithm")], [sg.Listbox(["Insertion", "Merge", "Quick"], size=(8, 2))], [sg.OK()]]
    window2 = sg.Window("Choose Algorithm", layout2)
    event, values = window2()
    window2.close()
    if values[0][0] == "Insertion":
        array_generator = insertion_sort(array)
    elif values[0][0] == "Merge":
        array_generator = mergesort(array)
    else:
        array_generator = quicksort(array)

    for g in array_generator:
        event, values = window.read(timeout=10)
        if event is None:
            break
        graph.Erase()
        draw(graph, g)
    window.close()


main()
