from tkinter import *
import csv
import datetime


window = Tk()

today = []
protein, fat, carb, ccal = 0, 0, 0, 0
with open('data/temp.csv', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for i in reader:
        try:
            if i[-1] == f'{datetime.date.today()}':
                today.append(i[0:-1])
        except:
            pass
for i in today:
    protein += round(float(i[1]))
    fat += round(float(i[2]))
    carb += round(float(i[3]))
    ccal += round(float(i[4]))

def get_calories():
    warning.place(x=50, y=20)
    info.delete(0, END)
    info.place(x=400, y=170, anchor='n')
    product = productField.get()
    try:
        weight = float(weightField.get())/100
    except:
        weight = 0

    temp_results = []
    results = []
    with open('data/products_all.csv', encoding='utf-8-sig') as file:
        database = csv.reader(file)
        for row in database:
            if product == '':
                pass
            elif product in row[0].lower():
                results.append(f'{row[0]}: белки: {round(float(row[1])*weight)} г, жиры: {round(float(row[2])*weight)} г, углеводы: {round(float(row[3])*weight)} г, ккал: {round(float(row[4])*weight)}')
                temp_results.append([row[0], round(float(row[1])*weight, 2), round(float(row[2])*weight, 2), round(float(row[3])*weight, 2), round(float(row[4])*weight, 2)])
    for res in results:
        info.insert(END, res)
    if temp_results:
        get.config(state=NORMAL)
    else:
        get.config(state=DISABLED)
    return temp_results

def get_product():
    try:
        selected_temp = info.selection_get()
        temp_results = get_calories()
        for i in temp_results:
            if selected_temp.split(':')[0] == i[0]:
                with open('data/temp.csv', 'a', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file)
                    i.append(f'{datetime.date.today()}')
                    writer.writerow(i)
                    today.append(i[:-1])
                    global protein
                    global fat
                    global carb
                    global ccal
                    protein += round(float(i[1]))
                    fat += round(float(i[2]))
                    carb += round(float(i[3]))
                    ccal += round(float(i[4]))
                    todays_statistics = Label(frame,
                                              text=f'Сегодня:\n Белки: {protein}\nЖиры: {fat}\nУглеводы: {carb}\nКкал: {ccal}',
                                              bg='pink')
                    todays_statistics.place(x=550, y=5)
    except:
        print('Выберете продукт для добавления')

def get_menu():
    get.config(state=DISABLED)
    info.place(x=400, y=170, anchor='n')
    info.delete(0, END)
    for i in today:
        text = f'{i[0]}: белки: {i[1]}, жиры: {i[2]}, углеводы: {i[3]}, ккал: {i[4]}.'
        info.insert(END, text)


window.title('Calorizator')
window.geometry('800x400')

window.resizable(width=False, height=False)

canvas = Canvas(window, height=400, width=800)
canvas.pack()

frame = Frame(window, bg='pink')
frame.place(relheight=1, relwidth=1)
productField = Entry(frame, bg='white')
weightField = Entry(frame, bg='white')
productText = Label(frame, text='Введите название продукта', bg='pink')
weightText = Label(frame, text='Введите вес продукта в граммах', bg='pink')
btn = Button(frame, text='Рассчитать', bg='yellow', command=get_calories)
info = Listbox(frame, bg='pink', selectmode=SINGLE, width=95, height=10)
get = Button(frame, text='Добавить в нажранное', command=get_product, state=DISABLED)
get_menu = Button(frame, text='Нажрато за сегодня', command=get_menu)
todays_statistics = Label(frame, text=f'Сегодня:\n Белки: {protein}\nЖиры: {fat}\nУглеводы: {carb}\nКкал: {ccal}', bg='pink')
warning = Label(frame, text='Будте внимательны\n при добавлении продуктов!\n Из нажратого удалить нельзя!', bg='pink')

productText.pack()
productField.pack()
weightText.pack()
weightField.pack()
todays_statistics.place(x=550, y=5)
btn.place(x=227, y=150, anchor='s')
get.place(x=350, y=150, anchor='s')
get_menu.place(x=500, y=150, anchor='s')

window.mainloop()
