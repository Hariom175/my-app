import kivy
import qrcode
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
import os.path

class QRGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super(QRGenerator, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.cols = 2

        # Create input fields
        self.name_label = Label(text='Name')
        self.name_input = TextInput(multiline=False)
        self.roll_label = Label(text='Roll No.')
        self.roll_input = TextInput(multiline=False)
        self.class_label = Label(text='Class')
        self.class_input = TextInput(multiline=False)
        self.phone_label = Label(text='Phone No.')
        self.phone_input = TextInput(multiline=False)

        # Create QR code image
        self.qr_image = Image()

        # Create result label
        self.result_label = Label(text='', size_hint_y=None, height=30)

        # Create buttons
        self.generate_btn = Button(text='Generate QR')
        self.generate_btn.bind(on_press=self.generate_qr)
        self.clear_btn = Button(text='Clear')
        self.clear_btn.bind(on_press=self.clear_fields)

        # Add widgets to grid layout
        self.add_widget(self.name_label)
        self.add_widget(self.name_input)
        self.add_widget(self.roll_label)
        self.add_widget(self.roll_input)
        self.add_widget(self.class_label)
        self.add_widget(self.class_input)
        self.add_widget(self.phone_label)
        self.add_widget(self.phone_input)
        self.add_widget(self.qr_image)
        self.add_widget(self.result_label)
        self.add_widget(self.generate_btn)
        self.add_widget(self.clear_btn)

    def generate_qr(self, instance):
        # Get input values
        name = self.name_input.text
        roll_no = self.roll_input.text
        class_ = self.class_input.text
        phone_no = self.phone_input.text

        # Check if all fields are filled
        if name == "" or roll_no == "" or class_ == "" or phone_no == "":
            self.result_label.text = "All fields are required!!!!"
            return

        # Generate QR code data
        qr_data = f"Name: {name}\nRoll No.: {roll_no}\nClass: {class_}\nPhone No: {phone_no}"

        # Check if data has already been generated
        file_path = f"{name}_{roll_no}.png"
        if os.path.exists(file_path):
            
            self.result_label.text = "QR code already generated for this data."
            return

        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Save QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((150, 150))  # Resize image
        img.save(file_path)

        # Update QR code image
        self.qr_image.source = file_path
        self.qr_image.reload()

        # Update result label
        self.result_label.text = "QR code created successfully!"

    def clear_fields(self, instance):
        # Clear all input fields
        self.name_input.text = ""
        self.roll_input.text = ""
        self.class_input.text = ""
        self.phone_input.text = ""
        self.qr_image.source = ""

class MyApp(App):
    def build(self):
        box_layout = BoxLayout(orientation='vertical')
        qr_generator = QRGenerator()
        box_layout.add_widget(qr_generator)
        return box_layout

if __name__ == '__main__':
    MyApp().run()
