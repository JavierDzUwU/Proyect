import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

class ProductCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catálogo de Productos")

        self.products = []
        self.product_images = []  # Lista para almacenar las imágenes de los productos

        self.create_gui()


    def create_gui(self):  # Se crea la interfaz gráfica de usuario (GUI)
        self.label_title = tk.Label(self.root, text="Catálogo de Productos", font=("Arial", 16))
        self.label_title.pack(pady=10)

        self.product_frame = tk.Frame(self.root)
        self.product_frame.pack(padx=10, pady=10)

        self.label_code = tk.Label(self.product_frame, text="Código:")
        self.label_code.grid(row=0, column=0, sticky="w")

        self.entry_code = tk.Entry(self.product_frame)
        self.entry_code.grid(row=0, column=1, padx=10)

        self.label_name = tk.Label(self.product_frame, text="Nombre:")
        self.label_name.grid(row=1, column=0, sticky="w")

        self.entry_name = tk.Entry(self.product_frame)
        self.entry_name.grid(row=1, column=1, padx=10)

        self.label_description = tk.Label(self.product_frame, text="Descripción:")
        self.label_description.grid(row=2, column=0, sticky="w")

        self.entry_description = tk.Entry(self.product_frame)
        self.entry_description.grid(row=2, column=1, padx=10)

        self.label_price = tk.Label(self.product_frame, text="Precio:")
        self.label_price.grid(row=3, column=0, sticky="w")

        self.entry_price = tk.Entry(self.product_frame)
        self.entry_price.grid(row=3, column=1, padx=10)

        self.btn_browse = tk.Button(self.product_frame, text="Seleccionar Imagen", command=self.browse_image)
        self.btn_browse.grid(row=4, column=0, columnspan=2, pady=10)

        self.label_image = tk.Label(self.product_frame, image=None)
        self.label_image.grid(row=4, column=0, columnspan=2, pady=5)

        self.btn_add = tk.Button(self.product_frame, text="Agregar Producto", command=self.add_product)
        self.btn_add.grid(row=5, column=0, columnspan=2, pady=10)

        self.entry_edit_code = tk.Entry(self.root)
        self.entry_edit_code.pack()

        self.btn_edit = tk.Button(self.root, text="Editar Producto", command=self.edit_product)
        self.btn_edit.pack()

        self.entry_delete_code = tk.Entry(self.root)
        self.entry_delete_code.pack()

        self.btn_delete = tk.Button(self.root, text="Eliminar Producto", command=self.delete_product)
        self.btn_delete.pack()

        separator = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN)  # Separador #
        separator.pack(fill=tk.X, padx=10, pady=5)

        self.catalog_frame = tk.Frame(self.root)
        self.catalog_frame.pack(padx=10, pady=10)

    def create_product_widgets(self):   # Se crea los widgets para mostrar los productos en el catálogo
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()

        self.product_images = []  # Lista para almacenar las imágenes de los productos

        row = 0
        col = 0

        for idx, product in enumerate(self.products):
            product_widget = tk.Frame(self.catalog_frame, padx=10, pady=10, bd=1, relief=tk.RAISED)
            product_widget.grid(row=row, column=col, padx=10, pady=10)

            product_label = tk.Label(product_widget, text=product["name"], font=("Helvetica", 12, "bold"))
            product_label.pack()

            if product["image"]:
                product_image = Image.open(product["image"])
                product_image = product_image.resize((100, 100), Image.LANCZOS)
                product_image = ImageTk.PhotoImage(product_image)
                self.product_images.append(product_image)  # Se almacena la imagen en la lista

                image_label = tk.Label(product_widget, image=product_image)
                image_label.pack()

            details_label = tk.Label(product_widget, text=f"Código: {product['code']}\nPrecio: {product['price']}\nDescripción: {product['description']}")
            details_label.pack()

            col += 1
            if col > 1:
                col = 0
                row += 1


    def update_catalog(self):  # Se actualiza la visualización del catálogo de productos
        self.create_product_widgets()

    def browse_image(self):  # Abre un cuadro de diálogo para seleccionar una imagen
        filepath = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")])
        if filepath:
            self.image_path = filepath
            self.show_image()

    def show_image(self):  # Muestra la imagen seleccionada en la interfaz
        if hasattr(self, "image_path"):
            image = Image.open(self.image_path)
            image = image.resize((100, 100), Image.LANCZOS)
            self.product_image = ImageTk.PhotoImage(image)

            self.label_image = tk.Label(self.product_frame, image=self.product_image)
            self.label_image.grid(row=4, column=0, columnspan=2, pady=5)


    def add_product(self):   # Agrega un nuevo producto a la lista de productos
        code = self.entry_code.get()
        name = self.entry_name.get()
        description = self.entry_description.get()
        price = self.entry_price.get()

        if hasattr(self, "image_path"):
            product_image = self.image_path
        else:
            product_image = None

        product = {
            "code": code,
            "name": name,
            "description": description,
            "price": price,
            "image": product_image
        }

        self.products.append(product)
        self.create_product_widgets()
        self.clear_fields()

    def clear_fields(self):   # Limpia los campos de entrada y la imagen seleccionada
        self.entry_code.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_description.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        if hasattr(self, "label_image"):
            self.label_image.destroy()
            delattr(self, "label_image")
            delattr(self, "image_path")


    def edit_product(self):   # Abre una ventana para editar los detalles de un producto
        code_to_edit = self.entry_edit_code.get()

        if not code_to_edit:
            messagebox.showinfo("Editar Producto", "Ingresa un código de producto para editar.")
            return

        selected_product = None
        for idx, product in enumerate(self.products):
            if product["code"] == code_to_edit:
                selected_product = product
                self.selected_index = idx  # Guardar el índice del producto seleccionado
                break

        if selected_product is None:
            messagebox.showinfo("Editar Producto", "Producto no encontrado.")
            return

        # Crear una nueva ventana para editar el producto
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Producto")

        self.label_code_edit = tk.Label(edit_window, text="Código:")
        self.label_code_edit.grid(row=0, column=0, sticky="w")

        self.entry_code_edit = tk.Entry(edit_window)
        self.entry_code_edit.grid(row=0, column=1)
        self.entry_code_edit.insert(0, selected_product["code"])

        self.label_name_edit = tk.Label(edit_window, text="Nombre:")
        self.label_name_edit.grid(row=1, column=0, sticky="w")

        self.entry_name_edit = tk.Entry(edit_window)
        self.entry_name_edit.grid(row=1, column=1)
        self.entry_name_edit.insert(0, selected_product["name"])

        self.label_description_edit = tk.Label(edit_window, text="Descripción:")
        self.label_description_edit.grid(row=2, column=0, sticky="w")

        self.entry_description_edit = tk.Entry(edit_window)
        self.entry_description_edit.grid(row=2, column=1)
        self.entry_description_edit.insert(0, selected_product["description"])

        self.label_price_edit = tk.Label(edit_window, text="Precio:")
        self.label_price_edit.grid(row=3, column=0, sticky="w")

        self.entry_price_edit = tk.Entry(edit_window)
        self.entry_price_edit.grid(row=3, column=1)
        self.entry_price_edit.insert(0, selected_product["price"])
 
        self.btn_save_edit = tk.Button(edit_window, text="Guardar Cambios", command=self.save_edit)
        self.btn_save_edit.grid(row=4, column=0, columnspan=2, pady=10)


    def save_edit(self):   # Guarda los cambios realizados en la edición de un producto
        new_name = self.entry_name_edit.get()
        new_description = self.entry_description_edit.get()
        new_price = self.entry_price_edit.get()

        self.products[self.selected_index]["name"] = new_name
        self.products[self.selected_index]["description"] = new_description
        self.products[self.selected_index]["price"] = new_price

        self.update_catalog()

        # Cerrar la ventana de edición
        self.root.focus_set()


    def delete_product(self):   # Elimina un producto de la lista y actualiza la GUI
        code_to_delete = self.entry_delete_code.get()

        if not code_to_delete:
            messagebox.showinfo("Eliminar Producto", "Ingresa un código de producto para eliminar.")
            return

        selected_product = None
        for product in self.products:
            if product["code"] == code_to_delete:
                selected_product = product
                break

        if selected_product is None:
            messagebox.showinfo("Eliminar Producto", "Producto no encontrado.")
            return

        # Mostrar ventana de confirmación
        confirm = messagebox.askyesno("Eliminar Producto", f"¿Estás seguro que deseas eliminar el producto {selected_product['name']}?")

        if confirm:
            self.products.remove(selected_product)
            self.create_product_widgets()  # Actualizar la visualización del catálogo


def main():
    root = tk.Tk()
    app = ProductCatalogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()