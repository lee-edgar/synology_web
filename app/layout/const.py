from enum import Enum
import os


class Menu(str, Enum):
    member = 'view1'
    admin = 'view2'
    summary = 'view3'