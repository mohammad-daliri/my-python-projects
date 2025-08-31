# Python Password Manager

A secure and user-friendly **Password Manager** built using Python. This project allows users to safely store, retrieve, and manage their passwords for various websites and services. It demonstrates practical skills in **encryption, database management, and secure password generation**, making it ideal for portfolio and internship applications.



## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Security Considerations](#security-considerations)
- [Future Improvements](#future-improvements)
- [Author](#author)



## Features

- **User Registration and Login**
  - Register with username and password.
  - Passwords are encrypted using **Fernet symmetric encryption**.

- **Change Account Password**
  - Users can update their account password anytime.
  - Option to generate a **strong random password** automatically.

- **Add and Manage Service Passwords**
  - Add passwords for websites or services.
  - Option to generate **strong secure passwords**.
  - View all saved passwords with decryption.

- **Delete Passwords**
  - Delete any saved password by ID.

- **Command-Line Interface (CLI)**
  - Easy-to-use menu for managing passwords.



## Technologies Used

- **Python 3** – Core programming language
- **SQLite** – Lightweight database for storing users and passwords
- **cryptography (Fernet)** – Encrypting and decrypting sensitive data
- **secrets & string modules** – Generating strong random passwords



## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohammad-daliri/password-manager.git
