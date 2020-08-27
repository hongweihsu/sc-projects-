"""
File: draw_line
Name: Dennis Hsu / 許宏瑋
----------------------
Drawing a motion bird flying above many clouds that you can decide number.
"""

from campy.graphics.gobjects import GOval, GRect, GPolygon, GRoundRect, GArc, GLabel, GCompound
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
import random


DELAY = 300
"""
This program will generate a lot of 'cloud object' and store in the 'cloud_box'.
"""

cloud_box = []
window = GWindow(785, 500)


class Cloud:
    def __init__(self):
        self.list = []

    def breed(self):
        """
        This method create three circle and one rectangle to compose a cloud shape.
        Every time the cloud shape will be displayed in random position of window.
        """
        dx = random.randint(10, window.width - 10)
        dy = random.randint(10, window.height - 10)

        rect = GRect(70, 30)
        rect.color = 'mintcream'
        rect.filled = True
        rect.fill_color = 'mintcream'
        self.list.append(rect)

        for i in range(3):
            circle = GOval(60, 60)
            circle.color = 'mintcream'
            circle.filled = True
            circle.fill_color = 'mintcream'
            self.list.append(circle)

        window.add(self.list[0], window.width + 45 + dx, 55 + dy)
        window.add(self.list[1], window.width + 10 + dx, 25 + dy)
        window.add(self.list[2], window.width + 45 + dx, 0 + dy)
        window.add(self.list[3], window.width + 80 + dx, 25 + dy)


class Bird:
    def __init__(self):
        self.words = ''
        self.talk_block = []
        self.count = 0
        self.eye = GOval(5, 5)
        """
        Here are 3 different pose of bird stored in self.pose, 
        each them contain GObjects, which would be stored in self.shape_box.
        Also notion that keeping rhythm in pose1, pose2, pose3, pose2, ....... 
        """
        self.shape_box = []
        self.POSE_1 = {'head': [(370, 190), (290, 220), (370, 235), (415, 230)],
                       'chest': [(290, 220), (325, 305), (370, 235)],
                       'body': [(290, 220), (135, 190), (220, 270), (325, 305)],
                       'belly': [(220, 270), (175, 340), (225, 345), (325, 305)],
                       'tail': [(175, 340), (95, 360), (155, 400), (225, 345)],
                       'wing': [(290, 220), (255, 160), (100, 55), (135, 190)],
                       'wing_far': [(205, 125), (205, 50), (280, 110), (305, 215), (290, 220), (255, 160)]
                       }
        self.POSE_2 = {'head': [(370, 190), (290, 220), (370, 235), (415, 230)],
                       'chest': [(290, 220), (325, 305), (370, 235)],
                       'body': [(290, 220), (135, 190), (220, 270), (325, 305)],
                       'belly': [(220, 270), (175, 340), (225, 345), (325, 305)],
                       'tail': [(175, 340), (95, 360), (155, 400), (225, 345)],
                       'wing': [(255, 160), (135, 190), (290, 220)],
                       'wing_2': [(255, 160), (135, 190), (95, 300)],
                       'wing_far': [(305, 145), (260, 170), (290, 220), (305, 215), ]
                       }
        self.POSE_3 = {'head': [(370, 190), (290, 220), (370, 235), (415, 230)],
                       'chest': [(290, 220), (325, 305), (370, 235)],
                       'body': [(290, 220), (195, 265), (325, 305)],
                       'belly': [(220, 270), (175, 340), (225, 345), (325, 305)],
                       'tail': [(175, 340), (95, 360), (155, 400), (225, 345)],
                       'wing': [(195, 265), (305, 235), (290, 220)],
                       'wing_2': [(195, 265), (250, 405), (305, 235)],
                       'wing_far': [(350, 267), (325, 305), (360, 355)]
                       }

        self.pose = [self.POSE_1, self.POSE_2, self.POSE_3, self.POSE_2]

    def speak(self):
        """
        This method give one triangle, four round corner and five rectangle to present talk bar,
        self.words will be the content of speak.
        """
        label = GLabel(self.words, 435, 170)
        label.font = 'Verdana-20'

        triangle = GPolygon()
        triangle.add_vertex((label.x+10, label.y))
        triangle.add_vertex((label.x+30, label.y))
        triangle.add_vertex((label.x, label.y+30))

        rect = GRect(label.width, label.height, x=label.x, y=label.y - label.height)
        rect_top = GRect(rect.width, 10, x=rect.x, y=rect.y - 10)
        rect_left = GRect(10, rect.height, x=rect.x - 10, y=rect.y)
        rect_button = GRect(rect.width, 10, x=rect.x, y=rect.y + rect.height)
        rect_right = GRect(10, rect.height, x=rect.x + rect.width, y=rect.y)

        arc_right_top = GArc(40, 40, 0, 90, rect.x - 10 + rect.width, rect.y - 10)
        arc_left_top = GArc(40, 40, 90, 90, rect.x - 10, rect.y - 10)
        arc_left_button = GArc(40, 40, 180, 90, rect.x - 10, rect.y - 10 + rect.height)
        arc_right_button = GArc(40, 40, 270, 90, rect.x - 10 + rect.width, rect.y - 10 + rect.height)

        self.talk_block = [triangle, rect, rect_top, rect_left, rect_button, rect_right, arc_right_top, arc_left_top,
                           arc_left_button,
                           arc_right_button, label]

        for i in self.talk_block:
            i.filled = True
            i.fill_color = 'crimson'
            i.color = 'crimson'
            if i == self.talk_block[-1]:
                i.color = 'azure'
            window.add(i)
        print(label.width, label.height)

    def clear_speak(self):
        """
        Use this method to clear sentence that was spoke,
        preventing a new sentence overlap to old one.
        """
        for i in self.talk_block:
            window.remove(i)

    def chang_pose(self):
        """
        This method will draw a bird, moreover, the type of pose is depended on 'count' number.
        """
        for k in self.pose[self.count]:
            self.link_point(self.pose[self.count][k])
        self.count += 1
        if self.count == len(self.pose):
            self.count = 0

    def link_point(self, point):
        """
        link the point of pose list and make GObject.
        :param point: Every piece of bird is consist of GPolygon shape, which is make up by these points.
        """
        r = [random.randint(225, 255), random.randint(240, 255), random.randint(255, 255)]
        shape = GPolygon()
        shape.color = 'lightgray'
        shape.filled = True
        shape.fill_color = (r[0], r[1], r[2])
        for j in range(len(point)):
            shape.add_vertex(point[j])
        window.add(shape)
        self.shape_box.append(shape)

        self.eye.filled = True
        self.eye.fill_color = 'navy'
        window.add(self.eye, 370, 210)

    def remove_pose(self):
        """
        in case the old pose overlap the new one, it should be removed by this method before new one generated.
        """
        for i in range(len(self.shape_box)):
            window.remove(self.shape_box[i])
        self.shape_box.clear()
        window.remove(self.eye)


def main():
    """
    The 'time' number is exploited to control while loop in this function.
    """
    time = 0
    set_background()
    draw_cloud(10)
    bird = Bird()
    sentence_count = 0
    sentence = ['Hellooooooooo, every one.', 'Wow, It\'s a nice day!', 'I wanna learn something NEW.',
                'Is this class SC101?', 'Hmm......, so', 'How can I master in Py?', 'Aha, Let me ask Jerry!',
                '😍😍😁😁🤪🤪']

    while True:
        time += 1
        if time < len(sentence)*20 + 1 and time % 20 == 0:

            bird.clear_speak()
            bird.words = sentence[sentence_count]
            print(time, sentence[sentence_count])
            bird.speak()
            sentence_count += 1

        elif time == len(sentence)*20 + 1:
            time = 0
            sentence_count = 0
        else:
            move_cloud()
            bird.chang_pose()
            pause(DELAY - 175)
            bird.remove_pose()


def set_background():
    background = GRect(window.width, window.height)
    background.filled = True
    background.fill_color = 'lavender'
    window.color = 'lavender'
    window.add(background, 0, 0)


def draw_cloud(cloud_number):
    """ This value 'cloud_number' decides how many cloud object were created in the beginning."""
    for i in range(cloud_number):
        cloud = Cloud()
        cloud_box.append(cloud)


def move_cloud():
    """
    When calling this function, every cloud object will start making GObject, otherwise, moving left.
    Once the cloud moving out of left boundary, those GObject created by the cloud will be removed.
    Then, if GObject list (cloud_box[i].list) is empty, cloud object will generate new one.
    """
    for i in range(len(cloud_box)):
        if len(cloud_box[i].list) == 0:
            cloud_box[i].breed()

        for j in cloud_box[i].list:
            j.move(-10, 0)

        if cloud_box[i].list[-1].x < -60:
            for k in cloud_box[i].list:
                window.remove(k)
            cloud_box[i].list.clear()


if __name__ == '__main__':
    main()
