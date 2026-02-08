#1
class Robot:
    def action(self):
        print("Robot is moving")

class CleaningRobot(Robot):
    def action(self):
        print("Robot is vacuuming the floor")

bot = CleaningRobot()
bot.action()

#2
class File:
    def open(self):
        print("Opening a general file")

class ImageFile(File):
    def open(self):
        print("Displaying image in the gallery")

img = ImageFile()
img.open()

#3
class Clock:
    def display_time(self):
        print("Showing time in 24-hour format")

class DigitalClock(Clock):
    def display_time(self):
        print("Showing time in 12-hour format with AM/PM")

my_clock = DigitalClock()
my_clock.display_time()

#4
class Chef:
    def make_specialty(self):
        print("Chef is making a generic dish")

class ItalianChef(Chef):
    def make_specialty(self):
        print("Chef is making Pizza")

chef = ItalianChef()
chef.make_specialty()

#5
class Notification:
    def send(self):
        print("Sending a basic notification")

class EmailNotification(Notification):
    def send(self):
        print("Sending an email with an attachment")

mail = EmailNotification()
mail.send()