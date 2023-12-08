# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
from papirus import PapirusComposite
from make_eink_screen_content import make_content
import json, sys

def soft_update_display(line_data_location: str):
    # open the file at line_data_location and parse it as json into a dict
    with open(line_data_location, 'r') as file:
        current_line_data = json.load(file)
    
    try:
        eink_content = make_content(current_line_data)
        eink_content.WriteAll()
    except Exception as e:
        print("Something went wrong with the display update:")
        print(e)

    
if __name__ == "__main__":
    soft_update_display(sys.argv[1])