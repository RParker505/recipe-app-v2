# Imports for charting functions
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Function to handle low-level image handling
def get_graph():
   #create a BytesIO buffer for the image
   buffer = BytesIO()         

   #create a plot with a bytesIO object as a file-like object. Set format to png
   plt.savefig(buffer, format='png')

   #set cursor to the beginning of the stream
   buffer.seek(0)

   #retrieve the content of the file
   image_png=buffer.getvalue()

   #encode the bytes-like object
   graph=base64.b64encode(image_png)

   #decode to get the string as output
   graph=graph.decode('utf-8')

   #free up the memory of buffer
   buffer.close()

   #return the image/graph
   return graph

#chart_type: user input o type of chart,
#data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')

   #specify figure size
   fig=plt.figure(figsize=(6,3))

   #select chart_type based on user input from the form
   if chart_type == '#1':
       #plot bar chart between name on x-axis and cooking time on y-axis
       plt.bar(data['name'], data['cooking_time'])
       plt.xlabel('Recipe Name')  # X-axis label
       plt.ylabel('Cooking Time (minutes)')  # Y-axis label
       plt.title('Cooking Time by Recipe')  # Chart title

   elif chart_type == '#2':
       # Group by difficulty level and calculate the count
       difficulty_counts = data['difficulty'].value_counts()

       # Calculate percentages for each difficulty level
       percentages = difficulty_counts / difficulty_counts.sum() * 100

       # Create labels with percentage values
       labels = [f'{level}: {percentage:.1f}%' for level, percentage in zip(difficulty_counts.index, percentages)]

       # Plot pie chart
       plt.pie(percentages, labels=labels, autopct='%1.1f%%', startangle=90)
       plt.title('Recipe Difficulty Breakdown')

   elif chart_type == '#3':
       #plot line chart based on recipe name on x-axis and cooking time on y-axis
       plt.plot(data['name'], data['cooking_time'])
       plt.xlabel('Recipe Name')  # X-axis label
       plt.ylabel('Cooking Time (minutes)')  # Y-axis label
       plt.title('Cooking Time by Recipe')  # Chart title

   else:
       print ('unknown chart type')

   #specify layout details
   plt.tight_layout()

   #render the graph to file
   chart =get_graph() 
   return chart  