import sys
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QUrl, QUrlQuery
from PyQt6.QtGui import QDesktopServices
import webbrowser
import smtplib
import mysql.connector
import re
from PyQt6.QtWidgets import  QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery
from fpdf import FPDF
from PyQt6.QtWidgets import QLabel



global Username
Username = None

class Users:
    @staticmethod
    def register(first_name, last_name, username, email, password, gender):
        # Insert data into MySQL
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
            )
            cursor = connection.cursor()

            # Insert user data into the 'users' table
            query = "INSERT INTO users (first_name, last_name, username, email, password, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (first_name, last_name, username, email, password, gender)
            cursor.execute(query, data)

            connection.commit()
            QtWidgets.QMessageBox.information(None, "Success", "User registration successful.")
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to register user: {str(e)}")
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def validate_fields(first_name, last_name, username, email, password):
        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")
        if not username:
            errors.append("Username is required.")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        if not email:
            errors.append("Email is required.")
        elif not re.match(r"^[a-zA-Z0-9_.+-]{2,}@[a-zA-Z0-9-]{2,}\.[a-zA-Z0-9-.]{2,}$", email):
            errors.append("Email Format is invalid.")
        if not password:
            errors.append("Password is required.")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        elif not re.search(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)", password):
            errors.append("Password must contain at least one uppercase letter, one lowercase letter, and one number.")
        return errors

class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui", self)

        self.pushButton.clicked.connect(self.register)
        

    def register(self):
        first_name = self.lineEdit.text()
        last_name = self.lineEdit_3.text()
        username = self.lineEdit_4.text()
        email = self.lineEdit_5.text()
        password = self.lineEdit_2.text()
        gender = "Male" if self.radioButton_2.isChecked() else "Female"

        # Clear previous error messages
        self.label_4.clear()
        self.label_5.clear()
        self.label_6.clear()
        self.label_7.clear()
        self.label_8.clear()
        # Validate fields
        errors = Users.validate_fields(first_name, last_name, username, email, password)
        if errors:
            for error in errors:
                if "First name" in error:
                    self.label_4.setText(error)
                elif "Last name" in error:
                    self.label_5.setText(error)
                elif "Username" in error:
                    self.label_6.setText(error)
                elif "Email" in error:
                    self.label_7.setText(error)
                elif "Password" in error:
                    self.label_8.setText(error)


        # Insert data into MySQL
        else:
            if Users.register(first_name, last_name, username, email, password, gender):
               

                self.close()
                acceuil1_window = Acceuil1Window()
                acceuil1_window.show()
                acceuil1_window.exec()  


class Acceuil2Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi("acceuil2.ui", self)


        self.pushButton_add.clicked.connect(self.show_page1)
        self.pushButton_rm.clicked.connect(self.show_page2)
        self.pushButton_up.clicked.connect(self.show_page3)
        self.pushButton_di.clicked.connect(self.show_page4)
        self.pushButton_tr.clicked.connect(self.show_page5)
        self.pushButton_addc.clicked.connect(self.insert_car_data)
        self.pushButton_r.clicked.connect(self.remove_car)
        self.pushButton_u.clicked.connect(self.update_car)
        self.pushButton_di.clicked.connect(self.display_car)
        self.pushButton_p.clicked.connect(self.search_car)
        self.pushButton_tra.clicked.connect(self.update_status)
 

    def update_status(self):
        
        receipt = self.lineEdit_tr.text()
        status = "accepted" if self.radioButton_tr1.isChecked() else "refused"

        
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Project"
        )
        cursor = db.cursor()

       
        cursor.execute("SELECT * FROM Rental WHERE receipt = %s", (receipt,))
        result = cursor.fetchone()

        if result: # If a row with the entered receipt number is found
           
            cursor.execute("UPDATE Rental SET status = %s WHERE receipt = %s", (status, receipt))
            db.commit()
            if status == "accepted":
                # Get the car ID from the rental
                car_id = result[1]

                
                cursor.execute("UPDATE Car SET availability = 0 WHERE id = %s", (car_id,))
                db.commit()


            QtWidgets.QMessageBox.information(self, "Success", f"Rental with receipt number {receipt} has been updated in the database.")
            self.label_err.clear()
            self.lineEdit_tr.clear()
        else:
            self.label_err.setText("Receipt number not found, please try again") # Display error message

        cursor.close()
        db.close()

    def show_page5(self):
        self.stackedWidget.setCurrentIndex(4)  
                
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
        )

        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Rental")
        result = cursor.fetchall()

        # find the tableWidget object in the UI
        table = self.findChild(QTableWidget, "tableWidget_tr")
        table.setRowCount(len(result))
        table.setColumnCount(len(result[0]))


        for i, row in enumerate(result):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                table.setItem(i, j, item)

        self.tableWidget_tr.verticalHeader().setVisible(False)

        db.close()

    
    def update_car(self):
        Id = self.lineEdit_7.text()
        brand = self.lineEdit_8.text()
        model = self.lineEdit_10.text()
        year = self.lineEdit_9.text()
        fuel = self.lineEdit_11.text()
        price = self.lineEdit_12.text()

       
        transmission = "Automatic" if self.radioButton.isChecked() else "Manual"
            
        reply = QtWidgets.QMessageBox.question(self, "Confirmation", f"Are you sure you want to update car with ID {Id}?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="Project"
                )
                cursor = connection.cursor()

                query = "UPDATE car SET brand = %s, model = %s, year = %s, fuel = %s, price = %s, transmission = %s WHERE Id = %s"
                data = (brand, model, year, fuel, price, transmission, Id)
                cursor.execute(query, data)
                connection.commit()

                QtWidgets.QMessageBox.information(self, "Success", f"Car with ID {Id} has been updated in the database.")
                
                
                self.lineEdit_7.clear()
                self.lineEdit_8.clear()
                self.lineEdit_10.clear()
                self.lineEdit_9.clear()
                self.lineEdit_11.clear()
                self.lineEdit_12.clear()
                self.radioButton.setChecked(False)
                self.radioButton_2.setChecked(False)

            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Failed to update car data: {str(e)}")
            finally:
                cursor.close()
                connection.close()
        else:
            # If the user cancels, do nothing
            pass


    
    def search_car(self):
        
        Id = self.lineEdit_7.text()
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
            )
            cursor = connection.cursor()

            # Select car data from the 'car' table
            query = "SELECT brand, model, year, fuel, price, transmission FROM car WHERE Id = %s"
            data = (Id,)
            cursor.execute(query, data)
            result = cursor.fetchone()
            if result:
                brand, model, year, fuel, price, transmission = result
                self.lineEdit_8.setText(brand)
                self.lineEdit_10.setText(model)
                self.lineEdit_9.setText(str(year))
                self.lineEdit_11.setText(fuel)
                self.lineEdit_12.setText(str(price))

                # Check the radio button based on the transmission value
                if transmission == "Automatic":
                    self.radioButton_3.setChecked(True)
                elif transmission == "Manual":
                    self.radioButton_4.setChecked(True)

                
                self.lineEdit_8.show() 
                self.lineEdit_10.show()
                self.lineEdit_9.show() 
                self.lineEdit_11.show() 
                self.lineEdit_12.show() 
                self.radioButton_3.show() 
                self.radioButton_4.show() 
                self.pushButton_u.show() 
                self.label_8.show()

                # Hide the ID field and search button, disable the ID field for editing
                self.lineEdit_7.setEnabled(False)
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "Car data not found.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to fetch car data: {str(e)}")
        finally:
            cursor.close()
            connection.close()


    def display_car(self):
        
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
        )

        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM car")
        result = cursor.fetchall()

        
        table = self.findChild(QTableWidget, "tableWidget")
        table.setRowCount(len(result))
        table.setColumnCount(len(result[0]))


        for i, row in enumerate(result):
            for j, col in enumerate(row):
                item = QTableWidgetItem(str(col))
                table.setItem(i, j, item)

        self.tableWidget.verticalHeader().setVisible(False)

        db.close()
    

        
            
            
    def insert_car_data(self):
        brand = self.lineEdit.text()
        model = self.lineEdit_4.text()
        year = self.lineEdit_3.text()
        fuel = self.lineEdit_2.text()
        price = self.lineEdit_5.text()
        if self.radioButton.isChecked():
            transmission = "Automatic"
        else:
            transmission = "Manual"

        if not brand or not model or not year or not fuel or not price:
            self.label002.setText("Please fill in all fields.")
            return

       
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
            )
            cursor = connection.cursor()

            
            query = "INSERT INTO car (brand, model, year, fuel, price, transmission) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (brand, model, year, fuel, price, transmission)
            cursor.execute(query, data)

            connection.commit()
            QtWidgets.QMessageBox.information(None, "Success", "Car data inserted successfully.")
            self.lineEdit.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_3.setText("")
            self.lineEdit_2.setText("")
            self.lineEdit_5.setText("")
            self.label002.setText("")

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Failed to insert car data: {str(e)}")
        finally:
            cursor.close()
            connection.close()
        
    
    def show_page1(self):
        self.stackedWidget.setCurrentIndex(0)  
    def show_page2(self):
        self.stackedWidget.setCurrentIndex(1)  
    def show_page3(self):
        self.stackedWidget.setCurrentIndex(2)  
                
        self.lineEdit_8.hide() 
        self.lineEdit_10.hide() 
        self.lineEdit_9.hide() 
        self.lineEdit_11.hide() 
        self.lineEdit_12.hide() 
        self.radioButton_4.hide() 
        self.radioButton_3.hide() 
        self.pushButton_u.hide() 
        self.label_8.hide()


        # Show the necessary fields for updating a car
        self.lineEdit_7.show() 
        self.pushButton_p.show()
        self.lineEdit_7.setEnabled(True) 
    def show_page4(self):
        self.stackedWidget.setCurrentIndex(3)  

    def remove_car(self):
        car_id = self.lineEdit_6.text()

        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='',  
            database='Project'  
        )
        cursor = connection.cursor()

        
        cursor.execute("SELECT * FROM car WHERE id=%s", (car_id,))
        car = cursor.fetchone()

        if car is not None:
            reply = QtWidgets.QMessageBox.question(self, "Confirmation", f"Are you sure you want to delete car with ID {car_id}?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)


            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            
                cursor.execute("DELETE FROM car WHERE id=%s", (car_id,))
                connection.commit()
                QtWidgets.QMessageBox.information(self, "Success", f"Car with ID {car_id} has been removed from the database.")
                self.label003.clear()
                self.lineEdit_6.clear()
                
            
        else:
            
            self.label003.setText(f"Car with ID {car_id} not found in the database.")
        
        
        cursor.close()
        connection.close()

class Acceuil1Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi("acceuil1.ui", self)
        self.pushButton_rent.clicked.connect(self.show_page22)
        self.pushButton_gal.clicked.connect(self.show_page11)
        self.pushButton_tra.clicked.connect(self.show_page33)
        # Create a new widget to hold the car containers
        self.scrollAreaWidget = QtWidgets.QScrollArea(self)
        self.scrollAreaWidget.setWidgetResizable(True)
        self.scrollAreaWidget.setObjectName("scrollAreaWidget")
        self.scrollAreaWidgetContents = QtWidgets.QWidget(self.scrollAreaWidget)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidget.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContentsLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContentsLayout.setObjectName("scrollAreaWidgetContentsLayout")
        self.pushButton.clicked.connect(self.on_rent_button_clicked)

 
    def show_page11(self):
        self.stackedWidget2.setCurrentIndex(0)
        self.load_cars()

    def show_page22(self):
       
        self.stackedWidget2.setCurrentIndex(1)
        
    def show_page33(self):
     
        self.stackedWidget2.setCurrentIndex(2)
       
  
        
        label_usr = self.findChild(QLabel, "label_usr")



        
        label_usr.setText(f"Dear {Username}, check your rental status here!")
        
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
        )

        
        cursor = db.cursor()
        cursor.execute("SELECT brand, model, days, date, price, status FROM Rental WHERE username = %s", (Username,))
        results = cursor.fetchall()

        
        table = self.findChild(QTableWidget, "tableWidget_tra")
        self.tableWidget_tra.setRowCount(0)

       
        for row_number, row_data in enumerate(results):
            self.tableWidget_tra.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_tra.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.tableWidget_tra.verticalHeader().setVisible(False)
        cursor.close()
        db.close()
        
    def on_rent_button_clicked(self):
       
        Id = self.lineEdit_1.text()
        days = self.lineEdit_2.text()
        date = self.dateEdit.date().toString("yyyy-MM-dd")

        # Check if car id exists in car table
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Project"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM car WHERE id = %s", (Id,))
        car_exists = cursor.fetchone()[0]

        if car_exists == 0:
           
            self.label_err.setText("Car ID does not exist")
        else:

            cursor.execute("SELECT availability, brand, model, price FROM car WHERE Id = %s", (Id,))
            result = cursor.fetchone()
            availability = result[0]
            brand = result[1]
            model = result[2]
            price = result[3]


            if availability == 0:
                # Car not available, show error message
                self.label_err.setText("Sorry! Car not available")
            else:
                reply = QtWidgets.QMessageBox.question(self, "Confirmation", f"Are you sure you want to rent the car with ID {Id}?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                        
                    cursor.execute("INSERT INTO rental (Id, brand, model, days,date, price, Username ) VALUES (%s, %s, %s, %s, %s, %s,%s)", (Id,brand,model, days, date, price,Username))
                    connection.commit()
                            # Generate PDF receipt
                    pdf = FPDF()
                    pdf.add_page()

                    
                    pdf.set_font("Arial", size=18, style='B')
                    pdf.cell(0, 20, "Receipt", border=0, ln=1, align='C')

                   
                    pdf.set_font("Arial", size=12)
                    pdf.cell(0, 10, txt=f"Thank you for renting the {brand} {model} with ID {Id}!", border=0, ln=1)
                    pdf.cell(0, 10, txt="Your rental request has been received and will be reviewed within 1-2 business days.", border=0, ln=1)
                    pdf.cell(0, 10, txt=f"Days rented: {days}", border=0, ln=1)
                    pdf.cell(0, 10, txt=f"Date rented: {date}", border=0, ln=1)

                    pdf.cell(0, 20, txt="Rental Information", border=1, ln=1, align='C')
                    pdf.cell(30, 10, "ID", border=1)
                    pdf.cell(40, 10, "Brand", border=1)
                    pdf.cell(40, 10, "Model", border=1)
                    pdf.cell(20, 10, "Days", border=1)
                    pdf.cell(30, 10, "Date", border=1)
                    pdf.cell(30, 10, "Price", border=1)
                    pdf.ln()
                    pdf.cell(30, 10, str(Id), border=1)
                    pdf.cell(40, 10, brand, border=1)
                    pdf.cell(40, 10, model, border=1)
                    pdf.cell(20, 10, str(days), border=1)
                    pdf.cell(30, 10, str(date), border=1)
                    pdf.cell(30, 10, str(price), border=1)

                    
                    pdf.ln()
                    pdf.cell(0, 10, txt="                                                                                                  Best Wishes,", border=0, ln=1)
                    pdf.cell(0, 10, txt="                                                                                                 Asma CHKIRIDA", border=0, ln=1)
               


                    pdf.line(5, 5, 205, 5) 
                    pdf.line(5, 5, 5, 290) 
                    pdf.line(205, 5, 205, 290) 
                    pdf.line(5, 290, 205, 290) 
                    
                    # Save PDF receipt with unique file name based on rental ID
                    pdf_file_name = f"receipt_{Id}.pdf"
                    pdf.output(pdf_file_name)
                        
                    QtWidgets.QMessageBox.information(self, "Success", f"Car with ID {Id} has been added to rental database.")
                    cursor.close()
                    connection.close()
                    self.lineEdit_1.clear()
                    self.lineEdit_2.clear()
                else:
                    self.lineEdit_1.clear()
                    self.lineEdit_2.clear()
                    pass
                




    def load_cars(self):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="Project"
        )
        cursor = connection.cursor()

        # Fetch all cars from the database
        cursor.execute("SELECT id, brand, model, year, fuel, price, availability, transmission, image_path FROM car")
        cars = cursor.fetchall()


        while self.scrollAreaWidgetContentsLayout.count() > 0:
            item = self.scrollAreaWidgetContentsLayout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

   
        filter_widget = QtWidgets.QWidget()
        filter_widget.setFixedHeight(100)
        filter_layout = QtWidgets.QHBoxLayout(filter_widget)

        filter_label = QtWidgets.QLabel("Filter:")
        filter_layout.addWidget(filter_label)

        filter_combobox = QtWidgets.QComboBox()
        filter_combobox.addItems(["All","Brand", "Model", "Year", "Fuel", "Price", "Transmission","Available"])
        filter_layout.addWidget(filter_combobox)
        filter_combobox.setStyleSheet("  background-color: rgba(133, 26, 20, 0.9); border: 1px solid black; padding: 2px 8px; border-radius: 4px; color: white;")

        filter_lineedit = QtWidgets.QLineEdit()
        filter_layout.addWidget(filter_lineedit)

        filter_button = QtWidgets.QPushButton("Search")
        filter_button.setStyleSheet("    background-color: rgba(133, 26, 20, 0.9); border: none; color: white;  padding: 8px; border-radius: 4px;")
        filter_button.clicked.connect(lambda: self.filter_cars(cars, filter_combobox.currentText(), filter_lineedit.text()))
        filter_layout.addWidget(filter_button)

        self.scrollAreaWidgetContentsLayout.addWidget(filter_widget)

        # Create a widget for each car and add it to the scroll area widget contents layout
        for car in cars:
            # Create a widget with two labels
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white; border: 1px solid #ccc; padding: 10px;")
            widget.setFixedWidth(400)  
            widget_layout = QtWidgets.QHBoxLayout(widget)
            image_label = QtWidgets.QLabel(widget)
            info_label = QtWidgets.QLabel(widget)
            widget_layout.addWidget(image_label)
            widget_layout.addWidget(info_label)

            image_label.setStyleSheet("background-color: #eee; border: 1px solid #ccc; padding: 10px; margin-right: 10px;")
            info_label.setStyleSheet("font-size: 12px; font-weight : bold; line-height: 1.2; color: maroon !important;")

            image_path = car[-1]

            pixmap = QtGui.QPixmap(image_path).scaledToHeight(280).scaledToWidth(200)
            image_label.setPixmap(pixmap)

            info = f"<b>.</b>Id: {car[0]}<br><b>.</b> {car[1]}<br><b>.</b> {car[2]}<br><b>.</b> {car[3]}<br><b>.</b> Fuel: {car[4]}<br><b>.</b> {car[5]}$ per day<br><b>.</b> {car[7]}"
            info_label.setText(f"<span style='font-weight: bold; color: black;'>{info}</span>")
            self.scrollAreaWidgetContentsLayout.addWidget(widget)

        
        self.scrollAreaWidget.setWidget(self.scrollAreaWidgetContents)

        
        if self.stackedWidget2.widget(0).layout() is None:
           
            layout = QtWidgets.QVBoxLayout(self.stackedWidget2.widget(0))
            layout.setContentsMargins(0, 0, 0, 0)
        else:
           
            layout = self.stackedWidget2.widget(0).layout()

       
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)


        layout.addWidget(self.scrollAreaWidget)

    def filter_cars(self, cars, filter_type, filter_text):
       
        filtered_cars = []
        
       
        filter_text = filter_text.lower()
        
       
        for car in cars:
            if filter_type == "All":
               
                filtered_cars.append(car)
            elif filter_type == "Brand":
                
                if car[1].lower().startswith(filter_text):
                    filtered_cars.append(car)
            elif filter_type == "Model":
               
                if car[2].lower().startswith(filter_text):
                    filtered_cars.append(car)
            elif filter_type == "Year":
                
                if str(car[3]).startswith(filter_text):
                    filtered_cars.append(car)
            elif filter_type == "Fuel":
              
                if car[4].lower().startswith(filter_text):
                    filtered_cars.append(car)
            elif filter_type == "Price":
             
                if float(car[5]) <= float(filter_text):
                    filtered_cars.append(car)
            elif filter_type == "Transmission":
                
                if car[7].lower().startswith(filter_text):
                    filtered_cars.append(car)
       
            elif filter_type == "Available":
                if int(car[6]) == 1: 
                    filtered_cars.append(car)
        
        # Clear the current layout from the scroll area widget contents layout
        while self.scrollAreaWidgetContentsLayout.count() > 1:
            item = self.scrollAreaWidgetContentsLayout.takeAt(1)
            widget = item.widget()
            widget.deleteLater()
        
        for car in filtered_cars:
            
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white; border: 1px solid #ccc; padding: 10px;")
            widget.setFixedWidth(400)  
            widget_layout = QtWidgets.QHBoxLayout(widget)
            image_label = QtWidgets.QLabel(widget)
            info_label = QtWidgets.QLabel(widget)
            widget_layout.addWidget(image_label)
            widget_layout.addWidget(info_label)
            image_label.setStyleSheet("background-color: #eee; border: 1px solid #ccc; padding: 10px; margin-right: 10px;")
            info_label.setStyleSheet("font-size: 12px; font-weight : bold; line-height: 1.2; color: maroon !important;")
           
            image_path = car[-1]
            pixmap = QtGui.QPixmap(image_path).scaledToHeight(221).scaledToWidth(141)
            image_label.setPixmap(pixmap)

            
            info = f"<br><b>.</b>Id: {car[0]}<b>.</b> {car[1]}<br><b>.</b> {car[2]}<br><b>.</b> {car[3]}<br><b>.</b> Fuel: {car[4]}<br><b>.</b> {car[5]}$ per day<br><b>.</b> {car[7]}"
            info_label.setText(f"<span style='font-weight: bold; color: black;'>{info}</span>")
            self.scrollAreaWidgetContentsLayout.addWidget(widget)

            self.scrollAreaWidgetContentsLayout.addWidget(widget)

       
        self.scrollAreaWidget.setWidget(self.scrollAreaWidgetContents)

        
        if self.stackedWidget2.widget(0).layout() is None:
            
            layout = QtWidgets.QVBoxLayout(self.stackedWidget2.widget(0))
            layout.setContentsMargins(0, 0, 0, 0)
        else:
            
            layout = self.stackedWidget2.widget(0).layout()

        
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)




class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("welcome.ui", self)
        self.pushButton.clicked.connect(self.login)
        self.pushButton_3.clicked.connect(self.open_discord)
        self.pushButton_2.clicked.connect(self.open_linkedin)
        self.pushButton_4.clicked.connect(self.open_github)
        self.pushButton_5.clicked.connect(self.open_email)
        self.pushButton_6.clicked.connect(self.open_register_ui)


    

    def login(self):
        global Username
        
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="Project"
            )
        cursor = db.cursor()

        if username == "admin" and password == "asMA2002*":
            self.close()
            acceuil2_window = Acceuil2Window()
            acceuil2_window.show()
            acceuil2_window.exec()
        else:



           
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()

            if result: 
                
                Username = result[0]
                self.close()
                acceuil1_window = Acceuil1Window()
                acceuil1_window.show()
                acceuil1_window.exec()  
            else:
                self.label_error.setText("Incorrect username or password") 

            cursor.close()
            db.close()


    def open_discord(self):
        webbrowser.open('https://discordapp.com/users/1557')

    def open_linkedin(self):
        webbrowser.open('https://www.linkedin.com/in/asma-chkirida-070332200/')

    def open_github(self):
        webbrowser.open('https://github.com/asmachkirida')

    def open_email(self):
        email = 'itsasmachk@gmail.com'
        url = QUrl('mailto:' + email)
        query = QUrlQuery()
        url.setQuery(query.query())
        QDesktopServices.openUrl(url)
 
    def open_register_ui(self):
        self.accept()  # Close the current dialog
        register_window = RegisterWindow()
        register_window.show()
        register_window.exec()  # Show the new dialog with event loop

 
        


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()