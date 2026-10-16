
import tkinter as tk
from tkinter import filedialog
from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

from TelemetryReader import TelemetryReader
from graphics import TelemetryGraph


# Main application window
homeWindow = tk.Tk()

homeWindow.title("iRacing Telemetry")
homeWindow.geometry("1200x800")


# Session and graph state
session = None
incidentList = []
graph = None

highlightedRegion = None


# Control panel
select_items_container = tk.Frame(
    homeWindow,
    bg="white",
    padx=5,
    pady=5
)

select_items_container.pack(
    side=LEFT,
    fill=Y
)


# Graph display area
graph_container = tk.Frame(homeWindow)

graph_container.pack(
    side=RIGHT,
    fill=BOTH,
    expand=True
)


# Matplotlib figure and axes
figure, ax = plt.subplots()


# Embed the Matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(
    figure,
    master=graph_container
)

canvas.draw()

canvas.get_tk_widget().pack(
    side=TOP,
    fill=BOTH,
    expand=True
)


# Graph navigation toolbar
toolbar = NavigationToolbar2Tk(
    canvas,
    graph_container
)

toolbar.update()


def file_button():
    """Load an IBT file and initialize the telemetry session and incident list."""
    global session
    global incidentList
    global graph
    global highlightedRegion

    file_path = filedialog.askopenfilename(
        parent=homeWindow,
        title="Select a File",
        filetypes=[
            ("IBT files", "*.ibt"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        return

    reader = TelemetryReader()

    session = reader.loadFile(file_path)

    fileTitle.config(text=file_path)

    incidentList = session.detectIncidents()

    graph = TelemetryGraph(session)

    incidentListBox.delete(0, END)

    for incident in incidentList:
        incidentListBox.insert(
            END,
            str(incident.toString())
        )

    highlightedRegion = None

    select_graph_type()


def select_graph_type():
    """Display the selected telemetry graph while preserving the current time range."""
    global highlightedRegion

    if graph is None:
        return

    selected = button_selected.get()

    # Save the current time range before replacing the graph.
    keepZoom = len(ax.lines) > 0

    if keepZoom:
        oldXLim = ax.get_xlim()

    if selected == 1:
        graph.graphPedals(ax)

    elif selected == 2:
        graph.graphSteering(ax)

    elif selected == 3:
        graph.graphSlipAngles(ax)

    elif selected == 4:
        graph.graphLateralAccelerationDisparities(ax)

    # Restore the previous time range and rescale the y-axis.
    if keepZoom:
        ax.set_xlim(oldXLim)

        autoscale_y(
            oldXLim[0],
            oldXLim[1]
        )

    highlightedRegion = None

    selection = incidentListBox.curselection()

    if selection:
        highlightGraph(selection)

    figure.tight_layout()

    canvas.draw_idle()


def getTelemetryLines():
    """Return telemetry plot lines, excluding vertical lap markers."""

    telemetryLines = []

    for line in ax.lines:

        xData = line.get_xdata()

        # Lap markers contain fewer data points than telemetry lines.
        if len(xData) > 2:
            telemetryLines.append(line)

    return telemetryLines


def autoscale_y(startTime, endTime):
    """Adjust the y-axis to fit telemetry values within the specified time range."""

    telemetryLines = getTelemetryLines()

    visibleYValues = []

    for line in telemetryLines:

        xData = line.get_xdata()
        yData = line.get_ydata()

        for x, y in zip(xData, yData):

            if startTime <= x <= endTime:
                visibleYValues.append(y)

    if not visibleYValues:
        return

    minY = min(visibleYValues)
    maxY = max(visibleYValues)

    yRange = maxY - minY

    # Add 15% padding, or a fixed amount for constant values.
    if yRange == 0:
        yPadding = 1

    else:
        yPadding = yRange * 0.15

    ax.set_ylim(
        minY - yPadding,
        maxY + yPadding
    )


def highlightGraph(incident_index):
    """Highlight the time range of the selected incident on the graph."""

    global highlightedRegion

    if not incident_index:
        return

    if session is None:
        return

    incident = incidentList[
        incident_index[0]
    ]

    # Remove the previous highlight before displaying a new one.
    if highlightedRegion is not None:

        try:
            highlightedRegion.remove()

        # The previous highlight may have been removed when the axes were cleared.
        except ValueError:
            pass

    highlightedRegion = ax.axvspan(
        incident.startTime,
        incident.endTime,
        color="red",
        alpha=0.25
    )

    canvas.draw_idle()


def focusIncident(incident_index):
    """Zoom into the selected incident and adjust the y-axis to fit its data."""

    if not incident_index:
        return

    if session is None:
        return

    incident = incidentList[
        incident_index[0]
    ]

    # Include two seconds of data before and after the incident.
    xPadding = 2

    startTime = (
        incident.startTime
        - xPadding
    )

    endTime = (
        incident.endTime
        + xPadding
    )

    ax.set_xlim(
        startTime,
        endTime
    )

    autoscale_y(
        startTime,
        endTime
    )

    canvas.draw_idle()


def resetGraph():
    """Restore the full graph view while retaining the selected incident."""
    if graph is None:
        return

    selected = button_selected.get()

    if selected == 1:
        graph.graphPedals(ax)

    elif selected == 2:
        graph.graphSteering(ax)

    elif selected == 3:
        graph.graphSlipAngles(ax)

    elif selected == 4:
        graph.graphLateralAccelerationDisparities(ax)

    global highlightedRegion

    highlightedRegion = None

    selection = incidentListBox.curselection()

    if selection:
        highlightGraph(selection)

    figure.tight_layout()

    canvas.draw_idle()


# Graph selection controls
button_selected = IntVar(
    homeWindow,
    1
)


graph_types = {
    "Pedals": 1,
    "Steering wheel angle": 2,
    "Slip angle": 3,
    "LatAccel Disparities": 4
}


for text, value in graph_types.items():

    Radiobutton(
        select_items_container,
        text=text,
        variable=button_selected,
        value=value,
        indicator=0,
        background="white",
        width=20,
        command=select_graph_type
    ).pack(
        side=TOP,
        ipady=5
    )


# File selection controls
fileTitle = tk.Label(
    select_items_container,
    text="No file selected",
    bg="white",
    wraplength=180
)

fileTitle.pack(
    pady=10
)


selectFileButton = tk.Button(
    select_items_container,
    text="Select .ibt file",
    command=file_button
)

selectFileButton.pack(
    padx=10,
    pady=10
)


resetButton = tk.Button(
    select_items_container,
    text="Reset Graph",
    command=resetGraph
)

resetButton.pack(
    padx=10,
    pady=5
)


# Incident selection list
incidentListBox = tk.Listbox(
    select_items_container,
    height=20,
    width=20
)


# Single-click highlights an incident; double-click zooms into it.
incidentListBox.bind(
    "<<ListboxSelect>>",
    lambda event: highlightGraph(
        incidentListBox.curselection()
    )
)


incidentListBox.bind(
    "<Double-Button-1>",
    lambda event: focusIncident(
        incidentListBox.curselection()
    )
)


incidentListBox.pack(
    side=BOTTOM,
    pady=10
)


# Start the application
homeWindow.mainloop()
