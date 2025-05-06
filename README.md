# Industrial Digitization Project – Cloud Integration

This project was developed as part of the **Industrial Digitization** class and demonstrates how a PC can interface with the cloud using industrial communication protocols.

## 🧩 Overview

The main goal of this project is to connect a local industrial setup to the **AWS IoT Core** cloud service, enabling the collection, visualization, and storage of environmental data such as **temperature** and **humidity**.

<p align="left">
    <img src="https://skillicons.dev/icons?i=linux,aws,raspberrypi,py"/>
</p>

## 🔧 System Architecture

- **STM32 Microcontroller**: Reads temperature and humidity data from Si7021 sensor.
- **Raspberry Pi 4B**: Acts as a communication bridge between the STM32 and the PC.
- **PC**: Simulates an OPC-UA server that receives data from the Raspberry Pi.
- **AWS IoT Core**: Receives, stores, and displays the data from the PC.

## 📡 Communication Flow

1. STM32 collects sensor data.
2. Data is transmitted to the Raspberry Pi via **MODBUS**.
3. Raspberry Pi sends data to the PC using **OPC-UA** protocol.
4. The PC pushes the data to **AWS IoT Core** for cloud storage and visualization.

## 💻 Technologies Used

- **Python** (PC-side implementation)
- **OPC-UA** protocol (local communication)
- **AWS IoT Core** (cloud platform)
- **Raspberry Pi OS/Linux**
- **STM32 Microcontroller**
