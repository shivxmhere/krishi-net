# Krishi-Net Mobile App Setup Guide

This is the React Native (Expo) mobile application for Krishi-Net, providing real-time crop disease detection for farmers.

## Prerequisites

1.  **Node.js** installed on your machine.
2.  **Expo Go** app installed on your physical Android/iOS device.
3.  **Backend Running**: Ensure the Krishi-Net backend is running (typically on port 8001).

## Getting Started

1.  **Navigate to the mobile directory**:
    ```bash
    cd mobile
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    ```

3.  **Configure API URL**:
    - Open `app.json`.
    - Update `extra.apiUrl` to your machine's **Local IP Address** (e.g., `http://192.168.1.5:8001`).
    - *Note: `10.0.2.2` only works for Android Emulators.*

4.  **Start the app**:
    ```bash
    npx expo start
    ```

5.  **Run on Device**:
    - Use the QR code displayed in the terminal to open the app in **Expo Go**.

## Key Features

-   **JWT Auth**: Secure login and registration.
-   **AI Camera**: Real-time image capture with leaf-alignment guide.
-   **Deep Insights**: Instant analysis with severity levels and treatment steps.
-   **Persistence**: Automatically stays logged in after first sign-in.

---

## Technical Stack

-   **Framework**: Expo / React Native
-   **Navigation**: React Navigation (Stack)
-   **Auth**: React Context API + AsyncStorage
-   **HTTP Client**: Axios with interceptors
-   **Hardware**: Expo Camera
