from tkinter import *
from tkinter.tix import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from mainCate import insertAll, insert, main
import pandas as pd

root = Tk()
root.title("Bundle Set Grocery Generator")
root.geometry('+%d+%d'%(50, 25)) # place GUI at x=350, y=10

check_but_array = []  # save category checkboxes
check_but_place = []  # save category checkboxes location
cate_list = []  # save all category from table

widgets = []  # contains all widgets on app

# === HOME AREA - logo & browse button ===
home_area = Frame(root, width=800, height=550, bg="white")
home_area.grid(columnspan=3, rowspan=3)
widgets.append(home_area)

# display logo
img = Image.open("assets/logo.png")
img = img.resize((int(img.size[0]/1.05), int(img.size[1]/1.05))) #resize image
img = ImageTk.PhotoImage(img)
img_label = Label(image=img, bg="white")
img_label.image = img
img_label.grid(columnspan=3, column=0, row=0, pady=(50, 0))
widgets.append(img_label)

# instructions
instructions = Label(root, text="Hello there!\nSelect an Excel file on your computer.", font=("Raleway", 14), bg="white")
instructions.grid(columnspan=3, column=0, row=1, sticky=S)
widgets.append(instructions)

# browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font=("Raleway", 14), bg="#20bebe", fg="white", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(columnspan=3, column=0, row=2, sticky=N, pady=(20, 0))
widgets.append(browse_btn)

# place a table content on the pages
def display_table(content, row, col, root):
    table_content = Text(root, height=10, width=75, padx=10, pady=10)
    table_content.insert(1.0, content)
    table_content.tag_configure("center", justify="center")
    table_content.tag_add("center", 1.0, "end")
    table_content.grid(columnspan=3, column=col, row=row, padx=25, pady=25)
    widgets.append(table_content)

# place list of category on the pages
def display_categories(df, root, row):
    # title
    cat_title = Label(root, text="Select Category", font=("Raleway", 14), bg="#ffffff")
    cat_title.grid(column=1, row=row)
    widgets.append(cat_title)
    
    # get category from table
    for i in range(len(df)):
        category = df["category"][i]
        if not cate_list.__contains__(category):
            cate_list.append(category)
    
    # create "all" checkbox
    check_but_array.append("")
    check_but_array[0] = IntVar()
    check_but_place.append(Checkbutton(root, text = "All", 
                        variable = check_but_array[0],
                        onvalue = 1,
                        offvalue = 0,
                        height = 2,
                        width = 10, 
                        bg="white"))

    # create list of category checkbox
    count = 1
    for i in cate_list:
        check_but_array.append("")
        check_but_array[count] = IntVar()
        temp = Checkbutton(root, text = i, 
                        variable = check_but_array[count],
                        onvalue = 1,
                        offvalue = 0,
                        height = 2,
                        width = 10,
                        bg="white")
        check_but_place.append(temp)
        count+=1

    # display category checkbox on specific grid
    curr_row = row + 1
    curr_col = 0
    for checkbox in check_but_place:
        if curr_col < 3:
            checkbox.grid(column=curr_col, row=curr_row)
        else:
            curr_row += 1
            curr_col = 0
            checkbox.grid(column=curr_col, row=curr_row)
        widgets.append(checkbox)
        curr_col += 1

def open_file():
    browse_text.set("loading...")
    file = askopenfile(parent=root, mode='rb', filetypes=[("Excel files", ".xlsx .xls")])

    if file:
        # clear all widgets
        for widget in widgets:
            widget.grid_forget()

        # read excel file
        df = pd.read_excel(file)

        # === TABLE CONTENT AREA === 
        table_area = Frame(root, width=800, height=235, bg="#20bebe")
        table_area.grid(columnspan=3, rowspan=2, row=0)
        widgets.append(table_area)

        # show text box on row 0 col 0
        display_table(df, 0, 0, root)

        # === LIST OF CATEGORY AREA ===
        cat_area = Frame(root, width=800, height=240, bg="#ffffff")
        cat_area.grid(columnspan=3, rowspan=4, row=2)
        widgets.append(cat_area)

        display_categories(df, root, 2)

        # === INPUT AREA ===
        input_area = Frame(root, width=800, height=75, bg="#c8c8c8")
        input_area.grid(columnspan=3, rowspan=1, row=6)
        widgets.append(input_area)

        # input label
        input_label = Label(root, text="Input Max Price : ", font=("Raleway", 14), bg="#c8c8c8")
        input_label.grid(column=0, row=6, sticky=E)
        widgets.append(input_label)

        # input field
        input_field = Text(root, height=1, width=40, pady=10)
        input_field.grid(column=1, row=6, sticky=W)
        widgets.append(input_field)

        # generate button
        global generate_text
        generate_text = StringVar()
        generate_btn = Button(root, textvariable=generate_text, command=lambda:generate_bundle(df, input_field.get("1.0", "end-1c")), font=("Raleway", 14), bg="#20bebe", fg="white", height=1, width=15)
        generate_text.set("Generate")
        generate_btn.grid(column=2, row=6, sticky=W)
        widgets.append(generate_btn)

def generate_bundle(df, input):
    # check_cat = all(cat == 0 for cat in check_but_array)

    generate_text.set("loading...")
        
    if input != "":
        max_price = int(input) # get max price from input field

        # clear all widgets
        for widget in widgets:
            widget.grid_forget()

        # get selected category
        if check_but_array[0].get() == 1:
            sem = insertAll(df) 
        else :
            cate_pil = []
            for i in range (1, len(check_but_array)):
                if check_but_array[i].get() == 1:
                    cate_pil.append(cate_list[i-1])
            sem = insert(df, cate_pil)

        # === OUTPUT AREA ===
        output = Frame(root, width=800, height=550, bg="#c8c8c8")
        output.grid(columnspan=3, rowspan=3)
        widgets.append(output)

        result = main(sem, max_price)

        # label 1
        output_label_1 = Label(root, text="GROCERY BUNDLE", font=("Raleway", 16), bg="#c8c8c8")
        output_label_1.grid(column=0, row=0, padx=50, sticky=S)
        widgets.append(output_label_1)

        # label 2
        output_label_2 = Label(root, text="CALCULATION DETAILS", font=("Raleway", 16), bg="#c8c8c8")
        output_label_2.grid(column=2, row=0, padx=50, sticky=S)
        widgets.append(output_label_2)

        # output grocery bundle
        output_bundle = Text(root, height=20, width=35, padx=10, pady=10)
        output_bundle.insert(1.0, result[0])
        output_bundle.grid(columnspan=1, column=0, row=1, padx=25, pady=25, sticky=E)
        widgets.append(output_bundle)

        # output details calculation
        output_details = Text(root, height=20, width=35, padx=10, pady=10)
        output_details.insert(1.0, result[1])
        output_details.grid(columnspan=1, column=2, row=1, padx=25, pady=25, sticky=W)
        widgets.append(output_details)
    else:
        print("Enter your max price!")

root.mainloop()
