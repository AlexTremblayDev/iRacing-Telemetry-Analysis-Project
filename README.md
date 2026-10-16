# iRacing Telemetry Analysis Project by Alex Tremblay

## Overview

This project is a Python-based telemetry analysis application designed to help sim racers examine their driving performance using telemetry data recorded by iRacing.

The application processes iRacing telemetry files (`.ibt`) and presents driving data through an interactive graphical interface. Its primary purpose is to help identify potential areas for improvement, such as excessive vehicle sliding, braking inconsistencies, and other driving behaviors that may negatively affect lap times.

This project is currently under development, with the long-term goal of creating a more comprehensive and accessible tool for analyzing racing performance.

<img width="1728" height="1085" alt="Screenshot 2026-10-12 at 1 45 46 PM" src="https://github.com/user-attachments/assets/bfeb8f81-0297-409d-9fab-2e60aba7d6ae" />
<img width="1728" height="1086" alt="Screenshot 2026-10-12 at 1 47 49 PM" src="https://github.com/user-attachments/assets/23ded07a-7f92-4cd5-9452-a40a0766418e" />

## Features

- **Telemetry File Analysis:** Reads and processes iRacing `.ibt` telemetry files.
- **Interactive Graphs:** Visualizes telemetry data such as speed, throttle, braking, steering, and other vehicle measurements.
- **Incident Detection:** Identifies potential driving incidents using telemetry measurements.
- **Incident Highlighting:** Highlights detected incidents on graphs for easier examination.
- **Lap Identification:** Displays lap boundaries to help distinguish between individual laps.
- **Graph Navigation:** Allows users to zoom into specific incidents and reset the graph view.
- **Multiple Data Views:** Supports switching between different telemetry measurements.

## Technologies Used

- **Python:** Primary programming language.
- **irsdk:** Used to access and interpret iRacing telemetry data.
- **Pandas:** Used for organizing and processing telemetry datasets.
- **NumPy:** Used for numerical calculations and telemetry analysis.
- **Matplotlib:** Used to visualize telemetry measurements.
- **Tkinter:** Used to develop the graphical user interface.

## How It Works

1. The user selects an iRacing telemetry file (`.ibt`).
2. The application reads and extracts telemetry measurements.
3. The collected data is processed to identify potential driving incidents.
4. The application displays telemetry graphs and detected incidents.
5. Users can select individual incidents to highlight or examine the corresponding telemetry data in greater detail.

The application is intended to assist with interpreting driving performance rather than automatically determine the cause of every incident.

## Project Motivation

My long-term career goal is to work in motorsport as a data analyst or telemetry engineer, helping racing teams understand vehicle performance and improve their competitiveness.

I started this project to develop practical experience with data processing, visualization, and software development while applying those skills to a subject I am passionate about.

Working with telemetry data provides an opportunity to explore how software and data analysis can contribute to real-world motorsport engineering.

## Current Limitations

This project is still in development.

- Incident detection may require further refinement to distinguish between intentional driving behavior and genuine mistakes.
- The application currently assumes some familiarity with racing telemetry and vehicle dynamics.
- Additional testing is needed to evaluate detection accuracy across different vehicles and circuits.

## Planned Improvements

- Improve incident detection accuracy and classification.
- Introduce more detailed lap comparisons.
- Develop additional tools for interpreting vehicle behavior.
- Improve the interface to make telemetry analysis more accessible.
- Expand the available telemetry visualizations.

## Project Status

**In Development**

This project is an ongoing personal learning experience, and its features will continue to evolve as I develop my programming and motorsport data analysis skills.
