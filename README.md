# Schedule Visualizer
## Description
Generates images for timetables in a weekly format for UBC courses.

## Downloading and setting up

1. Click on the green `Code` button on this page and press **Download ZIP**
2. Unzip the file
3. Open Terminal or Command Prompt or similar app
4. Navigate to the folder using the command prompt
    - on Windows the command to navigate there might look like:
    
    `cd C:/Users/yourname/Downloads/schedule-visualizer-main/schedule-visualizer-main`

    - on Mac the command to navigate there might look like:
    
    `cd /Users/yourname/Downloads/schedule-visualizer-main` 

    - *Note that you will likely have a different path*

5. Enter the command `pip install -r requirements.txt`

## Downloading the Excel file from Workday

1. Log into Workday 
2. Navigate to **View My Courses**
3. On the right side, above your courses, you may see the following icons:

    ![image of icons](image-1.png)

    Select the **Export to Excel** icon (the left-most icon, circled in red in the image)

4. Save the Excel file

## Using the program

1. Run `schedule_visualizer.py` in the *schedule-visualizer-main* folder. (Double-clicking on it should run it. If it opens an editor, run the code from the editor)
2. Select the Excel file that you just saved (likely titled *View_My_Courses.xlsx*)
3. The program should generate an image for each future semester that you have courses for. 