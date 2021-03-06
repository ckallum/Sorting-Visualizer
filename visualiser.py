import PySimpleGUI as sg
import random

GRAPH_SIZE = (700, 500)
BAR_SPACING, BAR_WIDTH = 6, 5
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
                             bottom_right=(i * BAR_SPACING + BAR_WIDTH, 0), fill_color='snow')


def merge(array, left, right, start):
    i = 0
    j = 0
    while j < len(right) and i < len(left):
        if left[i] < right[j]:
            array[i + j + start] = left[i]
            i += 1
        else:
            array[i + j + start] = right[j]
            j += 1
        yield array

    while i < len(left):
        array[i + j + start] = left[i]
        i += 1
        yield array
    while j < len(right):
        array[i + j + start] = right[j]
        j += 1
        yield array


def merge_sort(array, split, start):
    if split > 1:
        middle = (split + 1) // 2
        yield from merge_sort(array, middle, start)
        yield from merge_sort(array, middle, start + middle)
        yield from merge(array, array[start:start + middle], array[start + middle:start + split], start)
    yield array


def partition(array, begin, end, pivot):
    pivot_idx = begin
    for i in range(begin + 1, end + 1):
        if array[i] <= array[begin]:
            pivot_idx += 1
            array[i], array[pivot_idx] = array[pivot_idx], array[i]
            yield array
    array[pivot_idx], array[begin] = array[begin], array[pivot_idx]
    pivot.append(pivot_idx)
    yield array


def quick_sort_recursion(array, begin, end):
    if begin >= end:
        return
    pivot = []
    yield from partition(array, begin, end, pivot)
    pivot_idx = pivot.pop()
    yield from quick_sort_recursion(array, begin, pivot_idx - 1)
    yield from quick_sort_recursion(array, pivot_idx + 1, end)
    yield array


def quick_sort(array, begin=0, end=None):
    if not end:
        end = len(array) - 1
    yield from quick_sort_recursion(array, begin, end)


def bubble_sort(array):
    def swap(i, j):
        array[i], array[j] = array[j], array[i]

    for i in range(len(array) - 1):
        for j in range(i + 1, len(array)):
            if array[j] < array[i]:
                swap(i, j)
                yield array
    yield array


def heapify(array, i, n):
    current = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and array[left] > array[current]:
        current = left
    if right < n and array[right] > array[current]:
        current = right
    if current != i:
        array[i], array[current] = array[current], array[i]
        yield array
        yield from heapify(array, current, n)
    yield array


def heap_sort(array):
    n = len(array)
    for i in range((n+1)//2, -1, -1):
        yield from heapify(array, i, n)
    for i in range(n - 1, 0, -1):
        array[i], array[0] = array[0], array[i]
        yield array
        yield from heapify(array, 0, i)
    yield array


def main():
    graph = sg.Graph(GRAPH_SIZE, (0, 0), GRAPH_SIZE)
    layout = [[graph]]

    window = sg.Window('Sorting Algorithm Visualizer', layout, finalize=True)
    while 1:
        array = [i * VALUES // BARS for i in range(1, BARS)]
        random.shuffle(array)
        draw(graph, array)
        layout2 = [[sg.T("Choose Algorithm")],
                   [sg.Listbox(["Merge", "Quick", "Heap", "Inserstion", "Bubble"], size=(8, 5))],
                   [sg.OK()]]
        window2 = sg.Window("Choose Algorithm", layout2)
        event, values = window.read(timeout=10)
        if event is None:
            break
        event2, values2 = window2()
        if not event2:
            break
        window2.close()
        if values2[0][0] == "Insertion":
            array_generator = insertion_sort(array)
        elif values2[0][0] == "Merge":
            array_generator = merge_sort(array, len(array), 0)
        elif values2[0][0] == "Bubble":
            array_generator = bubble_sort(array)
        elif values2[0][0] == "Heap":
            array_generator = heap_sort(array)
        else:
            array_generator = quick_sort(array)

        for g in array_generator:
            event, values = window.read(timeout=10)
            if event is None:
                break
            graph.Erase()
            draw(graph, g)
        sg.Popup("Sorting Done")
    window.close()


if __name__ == '__main__':
    main()
