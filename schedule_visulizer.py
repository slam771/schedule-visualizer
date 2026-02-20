# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 10:38:34 2025
this is a cleaned up version of v6
"""

import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib as mlt
import matplotlib.ticker as ticker
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

def fix_times(columns):
    columns = columns.str.replace('p.m.', 'PM')
    columns = columns.str.replace('a.m.', 'AM')
    
    times = []
    times_hours = []
    times_mins = []
    
    for item in columns:
        if item == None:
            times_hours.append(0)
            times_mins.append(0)
            pass
        else:
            try:
                item = item.strip(' ')
                times_hours.append(datetime.strptime(item, '%I:%M %p').hour)
                times_mins.append(datetime.strptime(item, '%I:%M %p').minute)
                
            except ValueError:
                times_hours.append(0)
                times_mins.append(0)
                pass
            
    for x in range(len(times_mins)):
        times_mins[x] = float(times_mins[x])/60.0
           
    times = [x + y for x, y in zip(times_hours, times_mins)]
    columns = times
    return columns

def show_schedule(df3, savefile, to_save=False):
    weekday_list = 'Mon Tue Wed Thu Fri'.split(' ')

    # Resizes image based on course times
    day_length = df3['End Time'].max() - df3[df3['Start Time']!=0]['Start Time'].min()
    mlt.rcParams['figure.dpi'] = 150
    fig, ax = plt.subplots()
    fig.set_size_inches(5.5, 4.25)
    ax.set_xlim(0, 5)

    # Setting labels for x-axis and y-axis
    ax.set_xlabel('Day')
    ax.set_ylabel('Time')

    plt.gca().invert_yaxis()

    ten_list = []
    for i in range(10, 60, 10):
        ten_list.append(i)

    twentyfour_list = [float(i) for i in range(0, 24)]
    
    # Setting ticks on y-axis
    ax.set_yticks(twentyfour_list)
    
    twentyfour_list = [str(i) + ':00' for i in range(0, 24)]
    ax.set_yticklabels(twentyfour_list, fontsize=10)
    
    # Labelling tickes of y-axis
    ax.set_xticklabels('')

    # Setting graph attribute
    ax.grid(zorder=0)

    for weekday in weekday_list:
        num_classes = len(df3[df3['Weekdays'].str.contains(weekday)].sort_values(by='Start Time'))
        
        for index in range(num_classes):
            course_block = df3[df3['Weekdays'].str.contains(weekday)].sort_values(by='Start Time').iloc[[index]]
            start_time = float(course_block['Start Time'].to_string(index=False, header=False))
            duration = float(course_block['Duration'].to_string(index=False, header=False))

            ccode = course_block['Course Code'].to_string(index=False, header=False)
            bldgs = course_block['Building Short'].to_string(index=False, header=False)
            floor = course_block['Floor'].to_string(index=False, header=False).strip(' ')
            room = course_block['Room'].to_string(index=False, header=False).strip(' ')
            iform = course_block['Instructional Format'].to_string(index=False, header=False)
            
            if day_length <=7.0:
                txt = ccode + '\n' + bldgs + '-Floor ' + floor + '\nRoom: ' \
                    + room + '\n' + iform + ''
            
            else:
                txt = ccode + '\n' + bldgs + ' ' + room
            
            ax.broken_barh([(weekday_list.index(weekday), 1)], (start_time, duration), facecolors ='#aaaaaa', zorder=3, edgecolor ='black', data="abc")      
            ax.text(weekday_list.index(weekday)+0.03, start_time+(0.007*day_length), txt, fontsize=8,
                    linespacing=1.25, verticalalignment='top')

    ax.xaxis.set_minor_locator(ticker.FixedLocator([0.5, 1.5,2.5,3.5,4.5]))
    ax.xaxis.set_minor_formatter(ticker.FixedFormatter(weekday_list))
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top') 
    
    # Referenced from Stack Overflow
    #https://stackoverflow.com/questions/63356249/alternate-grid-background-color-in-matplotlib

    xticks, _ = plt.xticks()
    for y0, y1 in zip(xticks[::2], xticks[1::2]):
        plt.axvspan(y0, y1, color='white', alpha=0.9, zorder=0)
    plt.xticks(xticks)  # force the same xticks again
    ax.set_facecolor('#dddddd')

    plt.figure(figsize=(8.5, 11))
    
    fig.tight_layout()
    
    plt.show()
    if to_save ==True:
        fig.savefig(savefile + '.png', dpi=fig.dpi)
        print('saved')

# Removes extra data on given string in df
def change_string(df, to_delete):
    if df[to_delete].str.contains(':').any():
        df[to_delete] = df[to_delete].str.replace(to_delete + ':', '')
    else:
        df[to_delete] = df[to_delete].str.replace(to_delete, '')


filename = 'View_My_Courses.xlsx'

df = pd.read_excel(filename)

while not 'Course Listing' in df.columns:
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data-less the header row
    df.columns = new_header #set the header row as the df header

df = df[['Course Listing', 'Section', 'Instructional Format', 'Delivery Mode',
         'Meeting Patterns', 'Instructor']]

# Fill na with '|' to prevent errors when splitting with '|' character
df['Meeting Patterns'] = df['Meeting Patterns'].fillna("| "*7)

# Remove duplicate Meeting Patterns
df2 = df['Meeting Patterns'].str.split('\n',expand=True)
df['Meeting Patterns'] = df2[0]

# Split Course Listing into Course Name and Course Code
# Use 'Section' instead of 'Course Listing' to include section name 
df[['Course Code', 'Course Name']] = df['Course Listing'].str.split(' - ', expand=True)

# Split Meeting Patterns into seperate columns
mpat = df['Meeting Patterns'].str.split('|',expand=True)
if len(mpat.columns) == 8:
    df[['dates','Weekdays', 'Times', 'Campus', 'Building', 'Floor', 'Room', 'a']] = df['Meeting Patterns'].str.split('|',expand=True)
    df = df.drop(['a'], axis=1)

elif len(mpat.columns) == 7:
    df[['dates','Weekdays', 'Times', 'Campus', 'Building', 'Floor', 'Room']] = df['Meeting Patterns'].str.split('|',expand=True)

elif len(mpat.columns) == 4:
    df[['dates','Weekdays', 'Times', 'Campus']] = df['Meeting Patterns'].str.split('|',expand=True)


if df['Campus'].str.contains('-').any():
    df[['Building', 'Floor', 'Room']] = df['Campus'].str.split('-',expand=True)
    

# split times using ' - ' into 'start time' and 'end time'
df[['Start Time', 'End Time']] = df['Times'].str.split(' - ', expand=True)


# drop unneccessary columns
df = df.loc[:, df.columns.notna()]
df[['Start Date', 'End Date']] = df['dates'].str.split(' - ', expand=True)
df = df.drop(['Campus', 'Meeting Patterns'], axis=1)
df = df.drop(['Course Listing', 'Section'], axis=1)

# create a list of buildings' short titles
p = re.compile('[A-Z]{3,4}(?<!UBC)')
building_short = []

for item in df['Building']:
    try:
        building_short.append(p.search(item).group())
    except:
        building_short.append('')
    
df['Building Short'] = building_short

change_string(df, 'Room')
change_string(df, 'Floor')


# Insert the following column in the front for readability
# Referenced from StackOverflow
#https://stackoverflow.com/questions/25122099/move-column-by-name-to-front-of-table-in-pandas
cols = list(df)
cols.insert(0, cols.pop(cols.index('Course Code')))
cols.insert(0, cols.pop(cols.index('Course Name')))
cols.insert(9, cols.pop(cols.index('Building Short')))

df = df.loc[:, cols]

# make a new Dataframe with only necessary information
df2 = df[['Course Code', 'Instructional Format', 'Building Short', 'Floor', 'Room', 'Start Date', 'Weekdays', 'Start Time', 'End Time']]

# Convert times into hours
df2['Start Time'] = fix_times(df2['Start Time'])
df2['End Time'] = fix_times(df2['End Time'])

# Figure out how long each class is
df2['Duration'] = df2['End Time'].astype(float) - df2['Start Time'].astype(float)

dfs = []

# Separate schedules by starting month
for i in ('9', '1', '5', '7'):
    i = '-0' + i + '-'
    c = df2[df2['Start Date'].apply(str).str.contains(i)]
    if not c.empty:    
        dfs.append(c)

to_save = input('Save images? [y/n]: ')
if to_save.lower() == 'y':
    to_save=True
else:
    to_save = False

for index in range(len(dfs)):
    show_schedule(dfs[index], 'Schedule ' + str(index+1), to_save)

